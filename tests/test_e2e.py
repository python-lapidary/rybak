import logging
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class E2eTestData(NamedTuple):
    test_name: str
    data: Mapping[str, Any]
    error: Optional[bool] = False


e2e_test_data: Iterable[E2eTestData] = [
    E2eTestData(
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
    E2eTestData(
        'loop',
        dict(
            animals={
                'cat': 'meows',
                'dog': 'barks',
                '': 'is silent',
            }
        ),
    ),
    E2eTestData(
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
    E2eTestData(
        'loop_nested',
        {},
        error=True,
    ),
    E2eTestData(
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
    (*adapter, *param_set, exclusions[adapter[0]]) for adapter, param_set in product(adapters.items(), e2e_test_data)
]


@pytest.mark.parametrize('adapter_name,adapter,test_name,data,error,exclude', adapter_test_data)
def test_render(
    adapter_name: str,
    adapter: Callable[[Path], RendererAdapter],
    test_name: str,
    data: Mapping,
    error: bool,
    exclude: Iterable[str],
    tmp_path: Path,
) -> None:
    if adapter_name == 'mako' and sys.platform == 'win32':
        pytest.skip('Mako has problem with line endings on windows')

    root = Path(__file__).parent / 'test_e2e'
    target_path = tmp_path / f'{adapter_name}_{test_name}'
    target_path.mkdir()

    def fn():
        render(
            adapter(root / 'templates' / adapter_name / test_name),
            data,
            target_path,
            exclude_extend=exclude,
            remove_suffixes=['.jinja', '.mako'],
            report_cb=lambda _, target: logger.debug('Render to file %s', target),
        )

    if error:
        with pytest.raises(RenderError):
            fn()
    else:
        fn()
        cmp_dirs(root / 'output' / test_name, target_path)
