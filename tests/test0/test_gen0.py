import logging
from pathlib import Path
import sys
import tempfile

from rybak import Renderer
from compare import cmp_dirs

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
)


def test_gen():
    with tempfile.TemporaryDirectory() as tmp:
        test_root = Path(__file__).parent
        target_root = Path(tmp)
        Renderer(
            test_root / 'template',
            target_root,
            Path(),
            Path(),
        ).render(dict(
            tmpl_dir='target_dir',
            tmpl_file1='file.txt',
            tmpl_file2='file.txt',
            tmpl_file3='subdir/file.txt',
            content1='foo',
            content2='bar',
            content3='baz',
        ))

        cmp_dirs(test_root/'output', target_root)
