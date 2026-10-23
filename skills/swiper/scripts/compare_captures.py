#!/usr/bin/env python3
"""Pixel-compare one registered SRC/REP capture pair; stdlib only.

Reports mismatch fraction, differing-region bounding box and densest grid cells as JSON.
The number feeds the tolerance policy in scope.md; it never proves pairing or fidelity.
"""
import argparse
import json
from pathlib import Path
import struct
import sys
import zlib

DISCLAIMER = 'Pixel metric only; not state/phase pairing, semantics, motion, or fidelity.'
SIGNATURE = b'\x89PNG\r\n\x1a\n'
CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}  # PNG color type -> samples per pixel


class CaptureError(ValueError):
    pass


def _unfilter(kind, line, prev, bpp):
    if kind == 0:
        return
    if kind == 1:
        for i in range(bpp, len(line)):
            line[i] = (line[i] + line[i - bpp]) & 255
    elif kind == 2:
        for i in range(len(line)):
            line[i] = (line[i] + prev[i]) & 255
    elif kind == 3:
        for i in range(len(line)):
            left = line[i - bpp] if i >= bpp else 0
            line[i] = (line[i] + ((left + prev[i]) >> 1)) & 255
    elif kind == 4:
        for i in range(len(line)):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            p = a + b - c
            pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
            line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
    else:
        raise CaptureError(f'unknown PNG filter type {kind}')


def _to_rgba(line, color, width, palette, trns):
    out = bytearray(width * 4)
    if color == 6:
        return line
    if color == 2:
        for channel in range(3):
            out[channel::4] = line[channel::3]
        out[3::4] = b'\xff' * width
    elif color in (0, 4):
        step = 1 if color == 0 else 2
        gray = line[0::step]
        out[0::4] = out[1::4] = out[2::4] = gray
        out[3::4] = line[1::2] if color == 4 else b'\xff' * width
    else:
        for x, index in enumerate(line):
            if 3 * index + 3 > len(palette):
                raise CaptureError(f'palette index {index} out of range')
            out[4 * x:4 * x + 3] = palette[3 * index:3 * index + 3]
            out[4 * x + 3] = trns[index] if index < len(trns) else 255
    return out


def read_png(path):
    """Return (width, height, rows) with each row as RGBA bytes."""
    data = Path(path).read_bytes()
    if not data.startswith(SIGNATURE):
        raise CaptureError(f'{path}: not PNG bytes (JPEG renamed .png is invalid evidence)')
    header, palette, trns, idat, pos = None, b'', b'', [], 8
    while pos + 8 <= len(data):
        length, kind = struct.unpack('>I4s', data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b'IHDR':
            if len(body) != 13:
                raise CaptureError(f'{path}: malformed IHDR')
            header = struct.unpack('>IIBBBBB', body)
        elif kind == b'PLTE':
            palette = body
        elif kind == b'tRNS':
            trns = body
        elif kind == b'IDAT':
            idat.append(body)
        elif kind == b'IEND':
            break
    if header is None:
        raise CaptureError(f'{path}: missing IHDR')
    width, height, depth, color, _, _, interlace = header
    if depth != 8 or color not in CHANNELS or interlace:
        raise CaptureError(f'{path}: unsupported PNG (bit depth {depth}, color type {color}, '
                           f'interlace {interlace}); capture 8-bit non-interlaced PNG')
    bpp = CHANNELS[color]
    stride = width * bpp
    try:
        raw = zlib.decompress(b''.join(idat))
    except zlib.error as exc:
        raise CaptureError(f'{path}: corrupt image data ({exc})') from exc
    if len(raw) < height * (stride + 1):
        raise CaptureError(f'{path}: truncated image data')
    rows, prev = [], bytearray(stride)
    for y in range(height):
        start = y * (stride + 1)
        line = bytearray(raw[start + 1:start + 1 + stride])
        _unfilter(raw[start], line, prev, bpp)
        rows.append(bytes(_to_rgba(line, color, width, palette, trns)))
        prev = line
    return width, height, rows


def write_png(path, width, height, rgb_rows):
    """Write 8-bit RGB rows (bytes of width*3) as a PNG."""
    def chunk(kind, body):
        return (struct.pack('>I', len(body)) + kind + body
                + struct.pack('>I', zlib.crc32(kind + body) & 0xffffffff))
    raw = b''.join(b'\x00' + bytes(row) for row in rgb_rows)
    Path(path).write_bytes(SIGNATURE + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
                           + chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b''))


def _parse_mask(text):
    try:
        x, y, w, h = (int(part) for part in text.split(','))
    except ValueError:
        raise argparse.ArgumentTypeError(f'mask {text!r} must be x,y,width,height') from None
    if min(x, y) < 0 or min(w, h) <= 0:
        raise argparse.ArgumentTypeError(f'mask {text!r} needs non-negative origin and positive size')
    return x, y, w, h


def _masked_spans(y, width, masks):
    spans = sorted((max(0, x), min(width, x + w)) for x, my, w, h in masks if my <= y < my + h)
    merged = []
    for start, end in spans:
        if start >= end:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def compare(source, replica, channel_tolerance=0, masks=(), cell=32, diff_path=None, top=8):
    sw, sh, src = read_png(source)
    rw, rh, rep = read_png(replica)
    if (sw, sh) != (rw, rh):
        raise CaptureError(f'not comparable: source {sw}x{sh} vs replica {rw}x{rh}; '
                           'capture both sides at the same registered viewport profile')
    differing, masked_total, cells = 0, 0, {}
    left, top_y, right, bottom = sw, sh, -1, -1
    diff_rows = [] if diff_path else None
    for y in range(sh):
        a, b = src[y], rep[y]
        spans = _masked_spans(y, sw, masks)
        masked_total += sum(end - start for start, end in spans)
        out = bytearray(sw * 3) if diff_path else None
        if out is not None:
            for x in range(sw):
                i = 4 * x
                faded = 192 + (a[i] * 299 + a[i + 1] * 587 + a[i + 2] * 114) // 4000
                out[3 * x:3 * x + 3] = bytes((faded, faded, faded))
        if a != b:
            pa, pb = memoryview(a).cast('I'), memoryview(b).cast('I')
            for x in range(sw):
                if pa[x] == pb[x] or any(start <= x < end for start, end in spans):
                    continue
                i = 4 * x
                if max(abs(a[i + k] - b[i + k]) for k in range(4)) <= channel_tolerance:
                    continue
                differing += 1
                left, right = min(left, x), max(right, x)
                top_y, bottom = min(top_y, y), max(bottom, y)
                key = (x // cell, y // cell)
                cells[key] = cells.get(key, 0) + 1
                if out is not None:
                    out[3 * x:3 * x + 3] = b'\xff\x00\x00'
        if out is not None:
            for start, end in spans:
                out[3 * start:3 * end] = b'\x50\x50\xc8' * (end - start)
            diff_rows.append(out)
    if diff_path:
        write_png(diff_path, sw, sh, diff_rows)
    compared = sw * sh - masked_total
    hot = sorted(cells.items(), key=lambda item: (-item[1], item[0][1], item[0][0]))[:top]
    return {
        'source': str(source), 'replica': str(replica), 'width': sw, 'height': sh,
        'channelTolerance': channel_tolerance,
        'masks': [dict(zip(('x', 'y', 'width', 'height'), m)) for m in masks],
        'comparedPixels': compared, 'differingPixels': differing,
        'mismatchFraction': round(differing / compared, 6) if compared else None,
        'boundingBox': None if right < 0 else
        {'x': left, 'y': top_y, 'width': right - left + 1, 'height': bottom - top_y + 1},
        'hotCells': [{'x': cx * cell, 'y': cy * cell, 'size': cell, 'differingPixels': n}
                     for (cx, cy), n in hot],
        'diff': str(diff_path) if diff_path else None,
        'disclaimer': DISCLAIMER,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('source', help='SRC capture PNG')
    parser.add_argument('replica', help='paired REP capture PNG')
    parser.add_argument('--channel-tolerance', type=int, default=0, metavar='N',
                        help='ignore pixels whose max RGBA channel delta is <= N (0-255)')
    parser.add_argument('--mask', type=_parse_mask, action='append', default=[], metavar='X,Y,W,H',
                        help='exclude a region recorded with its reason in scope.md; repeatable')
    parser.add_argument('--max-fraction', type=float, metavar='F',
                        help='exit 1 when mismatchFraction exceeds the scope.md threshold F')
    parser.add_argument('--cell', type=int, default=32, help='hot-cell grid size in pixels')
    parser.add_argument('--diff', metavar='PNG', help='write a diff image: red = differing, blue = masked')
    args = parser.parse_args(argv)
    if not 0 <= args.channel_tolerance <= 255 or args.cell <= 0:
        parser.error('--channel-tolerance must be 0-255 and --cell positive')
    try:
        result = compare(args.source, args.replica, args.channel_tolerance, args.mask, args.cell, args.diff)
    except (OSError, CaptureError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    exceeded = args.max_fraction is not None and (result['mismatchFraction'] or 0) > args.max_fraction
    result['maxFraction'] = args.max_fraction
    result['withinMaxFraction'] = None if args.max_fraction is None else not exceeded
    print(json.dumps(result, indent=2))
    return 1 if exceeded else 0


if __name__ == '__main__':
    sys.exit(main())
