import tempfile
from pathlib import Path

import jinja2
import jinja2.loaders
from rybak import render
from rybak.jinja import JinjaAdapter

from tests.compare import cmp_dirs


def test_gen():
    with tempfile.TemporaryDirectory() as tmp:
        test_root = Path(__file__).parent
        target_root = Path(tmp)
        render(
            test_root / 'template',
            target_root,
            JinjaAdapter(loader=jinja2.loaders.FileSystemLoader(test_root / 'template')),
            dict(
                animals={
                    'cat': 'meows',
                    'dog': 'barks',
                    '': 'is silent',
                }
            ),
            remove_suffixes=('.jinja',),
        )
        cmp_dirs(test_root / 'output', target_root)
