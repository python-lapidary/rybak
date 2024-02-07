from itertools import product
from pathlib import Path
from typing import Any, Iterable, Mapping, NamedTuple, Optional

import pytest
from rybak import RenderError, render
from rybak.jinja import JinjaAdapter
from rybak.mako import MakoAdapter
from rybak.tornado import TornadoAdapter

from tests.compare import cmp_dirs


class TestData(NamedTuple):
    test_name: str
    data: Mapping[str, Any]
    error: Optional[bool] = False


jinja_test_data: Iterable[TestData] = [
    TestData(
        'simple',
        dict(
            tmpl_dir='target_dir',
            tmpl_file1='file1.txt',
            tmpl_file2='file2.txt',
            tmpl_file3='subdir/file3.txt',
            content1='foo',
            content2='bar',
            content3='baz',
            empty_directory_name='',
            empty_file_name='',
        ),
    ),
    TestData(
        'loop',
        dict(
            animals={
                'cat': 'meows',
                'dog': 'barks',
                '': 'is silent',
            }
        ),
    ),
    TestData(
        'loop_nested',
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
    ),
    TestData(
        'loop_nested',
        {},
        error=True,
    ),
    TestData(
        'missing_file',
        {},
        error=True,
    ),
]

adapters = {
    'jinja': JinjaAdapter,
    'mako': MakoAdapter,
    'tornado': TornadoAdapter,
}

exclusions = {
    'jinja': ['{{tmpl_dir}}/excluded_file.txt'],
    'mako': ['${tmpl_dir}/excluded_file.txt'],
    'tornado': ['{{tmpl_dir}}/excluded_file.txt'],
}

adapter_test_data = [
    (adapter, *param_set, exclusions[adapter]) for adapter, param_set in product(adapters.keys(), jinja_test_data)
]


@pytest.mark.parametrize('renderer,test_name,data,error,excluded', adapter_test_data)
def test_render(renderer: str, test_name: str, data: Mapping, error: bool, excluded: Iterable, tmp_path: Path) -> None:
    root = Path(__file__).parent / 'test_render'
    target_path = tmp_path / f'{renderer}_{test_name}'
    target_path.mkdir()

    def fn():
        render(
            root / 'templates' / renderer / test_name,
            target_path,
            adapters[renderer],
            data,
            excluded=[Path(item) for item in excluded] + [Path('__pycache__')],
            remove_suffixes=['.jinja', '.mako'],
        )

    if error:
        with pytest.raises(RenderError):
            fn()
    else:
        fn()
        cmp_dirs(root / 'output' / test_name, target_path)
