import logging
from pathlib import Path
import sys
import tempfile

import jinja2

from compare import cmp_dirs
from rybak import render
from rybak.jinja import JinjaRenderer

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
)


def test_gen():
    with tempfile.TemporaryDirectory() as tmp:
        test_root = Path(__file__).parent
        target_root = Path(tmp)
        render(
            test_root/'template' ,
            target_root,
            JinjaRenderer(jinja2.Environment(loader=jinja2.loaders.FileSystemLoader(test_root/'template'))),
            dict(
                tmpl_dir='target_dir',
                tmpl_file1='file1.txt',
                tmpl_file2='file2.txt',
                tmpl_file3='subdir/file3.txt',
                content1='foo',
                content2='bar',
                content3='baz',
            ),
            excluded=(
                Path('__pycache__'),
            ),
            remove_suffixes=('.jinja',),
        )

        cmp_dirs(test_root / 'output', target_root)
