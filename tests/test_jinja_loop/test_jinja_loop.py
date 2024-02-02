from pathlib import Path
import tempfile

import jinja2
import jinja2.loaders

from compare import cmp_dirs
from rybak import render
from rybak.jinja import JinjaRenderer


def test_gen():
    with tempfile.TemporaryDirectory() as tmp:
        test_root = Path(__file__).parent
        target_root = Path(tmp)
        render(
            test_root / 'template',
            target_root,
            JinjaRenderer(jinja2.Environment(loader=jinja2.loaders.FileSystemLoader(test_root / 'template'))),
            dict(
                animals={
                    'cat': 'meows',
                    'dog': 'barks',
                    '':'is silent',
                }
            ),
            remove_suffixes=('.jinja',)
        )
        cmp_dirs(test_root / 'output', target_root)
