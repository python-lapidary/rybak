import tempfile
import unittest
from pathlib import Path

import jinja2
import jinja2.loaders
from compare import cmp_dirs
from rybak import render
from rybak.jinja import JinjaAdapter


class Test0(unittest.TestCase):
    def test_gen(self):
        with tempfile.TemporaryDirectory() as tmp:
            test_root = Path(__file__).parent
            target_root = Path(tmp)
            render(
                test_root / 'template',
                target_root,
                JinjaAdapter(loader=jinja2.loaders.FileSystemLoader(test_root / 'template')),
                dict(
                    animals=dict(
                        cats=dict(
                            Loki='black, white, red',
                            Judo='black, white',
                        ),
                        dogs=dict(
                            Pluto='golden',
                            Goofy='black',
                        ),
                    )
                ),
            )
            cmp_dirs(test_root / 'output', target_root)

    def test_error_missing_value(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(jinja2.UndefinedError):
            test_root = Path(__file__).parent
            target_root = Path(tmp)
            render(
                test_root / 'template',
                target_root,
                JinjaAdapter(loader=jinja2.loaders.FileSystemLoader(test_root / 'templates')),
                {},
            )
