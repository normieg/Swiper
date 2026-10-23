import importlib.util
import io
from contextlib import redirect_stderr, redirect_stdout
import json
from pathlib import Path
import random
import struct
import tempfile
import unittest
import zlib


SCRIPT = Path(__file__).parents[1] / 'scripts' / 'compare_captures.py'
spec = importlib.util.spec_from_file_location('compare_captures', SCRIPT)
compare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare)


def paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else b if pb <= pc else c


def encode(path, width, rows, color=2, filters=(0,), palette=b'', trns=b''):
    """Independent encoder applying the given PNG filter type per row."""
    bpp = {0: 1, 2: 3, 3: 1, 6: 4}[color]
    raw, prev = bytearray(), bytes(width * bpp)
    for y, row in enumerate(rows):
        kind = filters[y % len(filters)]
        raw.append(kind)
        for i, value in enumerate(row):
            a = row[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            raw.append((value - (0, a, b, (a + b) >> 1, paeth(a, b, c))[kind]) & 255)
        prev = row

    def chunk(kind, body):
        return struct.pack('>I', len(body)) + kind + body + struct.pack('>I', zlib.crc32(kind + body))
    data = compare.SIGNATURE + chunk(b'IHDR', struct.pack('>IIBBBBB', width, len(rows), 8, color, 0, 0, 0))
    if palette:
        data += chunk(b'PLTE', palette)
    if trns:
        data += chunk(b'tRNS', trns)
    Path(path).write_bytes(data + chunk(b'IDAT', zlib.compress(bytes(raw))) + chunk(b'IEND', b''))


def solid(width, height, rgb=(240, 240, 240)):
    return [bytes(rgb) * width for _ in range(height)]


class CompareCapturesTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)

    def tearDown(self):
        self.dir.cleanup()

    def png(self, name, rows, width=None, **options):
        path = self.root / name
        encode(path, width or len(rows[0]) // 3, rows, **options)
        return path

    def run_main(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = compare.main([str(arg) for arg in args])
        return code, out.getvalue(), err.getvalue()

    def test_decodes_every_filter_type_and_color_type(self):
        rng = random.Random(7)
        width, height = 9, 10
        rgba = [bytes(rng.randrange(256) for _ in range(width * 4)) for _ in range(height)]
        rgb = [bytes(b for i, b in enumerate(row) if i % 4 != 3) for row in rgba]
        gray = [row[0::3] for row in rgb]
        palette = bytes(rng.randrange(256) for _ in range(12))
        indexed = [bytes(rng.randrange(4) for _ in range(width)) for _ in range(height)]
        cases = {
            'rgba': (rgba, dict(color=6), rgba),
            'rgb': (rgb, dict(color=2), [bytes(sum(([*r[i:i + 3], 255] for i in range(0, len(r), 3)), []))
                                         for r in rgb]),
            'gray': (gray, dict(color=0), [bytes(sum(([g, g, g, 255] for g in r), [])) for r in gray]),
            'palette': (indexed, dict(color=3, palette=palette, trns=b'\x10'),
                        [bytes(sum(([*palette[3 * i:3 * i + 3], 16 if i == 0 else 255] for i in r), []))
                         for r in indexed]),
        }
        for name, (rows, options, expected) in cases.items():
            with self.subTest(name):
                path = self.root / f'{name}.png'
                encode(path, width, rows, filters=(0, 1, 2, 3, 4), **options)
                self.assertEqual(compare.read_png(path), (width, height, expected))

    def test_identical_captures_have_no_difference(self):
        rows = solid(40, 30)
        result = compare.compare(self.png('a.png', rows), self.png('b.png', rows))
        self.assertEqual((result['differingPixels'], result['mismatchFraction']), (0, 0.0))
        self.assertIsNone(result['boundingBox'])
        self.assertEqual(result['hotCells'], [])

    def test_locates_region_and_honors_channel_tolerance(self):
        source = solid(64, 48)
        replica = [bytearray(row) for row in solid(64, 48)]
        for y in range(10, 14):
            for x in range(40, 50):
                replica[y][3 * x:3 * x + 3] = b'\x00\x00\x00'
        replica[0][0:3] = bytes((245, 240, 240))  # 5-level antialias-sized delta
        result = compare.compare(self.png('s.png', source), self.png('r.png', [bytes(r) for r in replica]))
        self.assertEqual(result['differingPixels'], 41)
        self.assertEqual(result['boundingBox'], {'x': 0, 'y': 0, 'width': 50, 'height': 14})
        self.assertEqual(result['hotCells'][0], {'x': 32, 'y': 0, 'size': 32, 'differingPixels': 40})
        tolerant = compare.compare(self.root / 's.png', self.root / 'r.png', channel_tolerance=5)
        self.assertEqual(tolerant['differingPixels'], 40)
        self.assertEqual(tolerant['boundingBox'], {'x': 40, 'y': 10, 'width': 10, 'height': 4})
        self.assertAlmostEqual(tolerant['mismatchFraction'], round(40 / (64 * 48), 6))

    def test_masks_exclude_pixels_and_diff_image_marks_regions(self):
        source = solid(20, 10)
        replica = [bytearray(row) for row in solid(20, 10)]
        replica[2][3 * 5:3 * 5 + 3] = b'\x00\x00\x00'     # masked difference
        replica[8][3 * 15:3 * 15 + 3] = b'\x00\x00\x00'   # real difference
        diff = self.root / 'diff.png'
        result = compare.compare(self.png('s.png', source), self.png('r.png', [bytes(r) for r in replica]),
                                 masks=[(4, 1, 4, 3), (6, 2, 4, 1)], diff_path=diff)
        self.assertEqual(result['comparedPixels'], 200 - 14)  # 12 + 4 masked, 2 overlapping
        self.assertEqual(result['differingPixels'], 1)
        self.assertEqual(result['boundingBox'], {'x': 15, 'y': 8, 'width': 1, 'height': 1})
        _, _, rows = compare.read_png(diff)
        self.assertEqual(rows[8][4 * 15:4 * 15 + 3], b'\xff\x00\x00')
        self.assertEqual(rows[2][4 * 5:4 * 5 + 3], b'\x50\x50\xc8')
        self.assertNotIn(b'\xff\x00\x00', rows[2])

    def test_rejects_dimension_mismatch_and_non_png(self):
        small, large = self.png('s.png', solid(10, 10)), self.png('l.png', solid(10, 12))
        code, out, err = self.run_main(small, large)
        self.assertEqual((code, out), (2, ''))
        self.assertIn('not comparable: source 10x10 vs replica 10x12', err)
        jpeg = self.root / 'renamed.png'
        jpeg.write_bytes(b'\xff\xd8\xff\xe0' + bytes(32))
        code, _, err = self.run_main(small, jpeg)
        self.assertEqual(code, 2)
        self.assertIn('not PNG bytes', err)

    def test_max_fraction_sets_exit_code(self):
        source = solid(10, 10)
        replica = [bytearray(row) for row in solid(10, 10)]
        replica[0][0:6] = bytes(6)
        s, r = self.png('s.png', source), self.png('r.png', [bytes(row) for row in replica])
        code, out, _ = self.run_main(s, r, '--max-fraction', '0.01')
        self.assertEqual(code, 1)
        self.assertEqual((json.loads(out)['mismatchFraction'], json.loads(out)['withinMaxFraction']),
                         (0.02, False))
        code, out, _ = self.run_main(s, r, '--max-fraction', '0.02')
        self.assertEqual((code, json.loads(out)['withinMaxFraction']), (0, True))


if __name__ == '__main__':
    unittest.main()
