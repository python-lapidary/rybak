import sys
from itertools import product
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, NamedTuple, Optional

import jinja2
import pytest
from rybak import RenderError, render
from rybak.adapter import RendererAdapter
from rybak.jinja import JinjaAdapter
from rybak.mako import MakoAdapter

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
    'jinja': lambda template_root: JinjaAdapter(loader=jinja2.FileSystemLoader(template_root)),
    'mako': MakoAdapter,
}

exclusions = {
    'jinja': ['{{tmpl_dir}}/excluded_file.txt'],
    'mako': ['${tmpl_dir}/excluded_file.txt'],
}

adapter_test_data = [
    (*adapter, *param_set, exclusions[adapter[0]]) for adapter, param_set in product(adapters.items(), jinja_test_data)
]


@pytest.mark.parametrize('adapter_name,adapter,test_name,data,error,excluded', adapter_test_data)
def test_render(
    adapter_name: str,
    adapter: Callable[[Path], RendererAdapter],
    test_name: str,
    data: Mapping,
    error: bool,
    excluded: Iterable,
    tmp_path: Path,
) -> None:
    if adapter_name == 'mako' and sys.platform == 'win32':
        pytest.skip('Mako has problem with line endings on windows')

    root = Path(__file__).parent / 'test_render'
    target_path = tmp_path / f'{adapter_name}_{test_name}'
    target_path.mkdir()

    def fn():
        render(
            adapter(root / 'templates' / adapter_name / test_name),
            data,
            target_path,
            excluded=[Path(item) for item in excluded] + [Path('__pycache__')],
            remove_suffixes=['.jinja', '.mako'],
        )

    if error:
        with pytest.raises(RenderError):
            fn()
    else:
        fn()
        cmp_dirs(root / 'output' / test_name, target_path)
