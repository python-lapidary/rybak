import tempfile
import unittest
from pathlib import Path

from compare import cmp_dirs
from rybak import render
from rybak.tornado import TornadoAdapter


class Test0(unittest.TestCase):
    def test_gen(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_root = Path(__file__).parent
            target_root = Path(tmp)
            render(
                test_root / 'template',
                target_root,
                TornadoAdapter,
                dict(
                    animals=dict(
                        cats=dict(
                            Loki='black, white, red',
                            Judo='black, white',
                        ),
                        dogs=dict(
                            Pluto='golden',
                            Goofy='black',
                        )
                    ))
            )
            cmp_dirs(test_root / 'output', target_root)


    def test_error_missing_value(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(NameError):
            test_root = Path(__file__).parent
            target_root = Path(tmp)
            render(
                test_root / 'template',
                target_root,
                TornadoAdapter,
                {},
            )
