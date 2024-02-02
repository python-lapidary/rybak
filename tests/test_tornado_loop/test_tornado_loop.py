import tempfile
from pathlib import Path

from compare import cmp_dirs
from rybak import render
from rybak.tornado import TornadoAdapter


def test_gen():
    with tempfile.TemporaryDirectory() as tmp:
        test_root = Path(__file__).parent
        target_root = Path(tmp)
        render(
            test_root / 'template',
            target_root,
            TornadoAdapter,
            dict(
                animals=dict(
                    cat='meows',
                    dog='barks'
                )
            )
        )
        cmp_dirs(test_root / 'output', target_root)
