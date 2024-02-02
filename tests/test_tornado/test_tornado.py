import logging
import sys
import tempfile
from pathlib import Path

from compare import cmp_dirs
from rybak import render
from rybak.tornado import TornadoAdapter

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
            test_root / 'template',
            target_root,
            TornadoAdapter,
            dict(
                tmpl_dir='target_dir',
                tmpl_file1='file1.txt',
                tmpl_file2='file2.txt',
                tmpl_file3='subdir/file3.txt',
                content1='foo',
                content2='bar',
                content3='baz',
            )
        )

        cmp_dirs(test_root / 'output', target_root)
