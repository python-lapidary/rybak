import pathlib

import jinja2
import rybak
import rybak.jinja
from compare import dir_content

data = dict(
    tmpl_dir='target_dir',
    tmpl_file1='file1.txt',
    tmpl_file2='file2.txt',
    tmpl_file3='subdir/file3.txt',
    content1='foo',
    content2='bar',
    content3='baz',
    empty_directory_name='',
    empty_file_name='',
)


def test_callback(tmp_path: pathlib.Path):
    logs = set()

    def report_fb(source: pathlib.PurePath, target: pathlib.Path) -> None:
        logs.add((source, target))

    template_root = pathlib.Path(__file__).parent / 'test_e2e' / 'templates' / 'jinja' / 'simple'

    rybak.render(
        rybak.jinja.JinjaAdapter(loader=jinja2.FileSystemLoader(template_root)),
        data,
        tmp_path,
        remove_suffixes=['.jinja'],
        report_cb=report_fb,
    )

    assert logs == {
        (pathlib.PurePath('{{tmpl_file1}}'), pathlib.Path('file1.txt')),
        (pathlib.PurePath('{{tmpl_file3}}'), pathlib.Path('subdir/file3.txt')),
        (pathlib.PurePath('{{tmpl_dir}}/excluded_file.txt'), pathlib.Path('target_dir/excluded_file.txt')),
        (pathlib.PurePath('{{tmpl_dir}}/suffixed.txt.jinja'), pathlib.Path('target_dir/suffixed.txt')),
        (pathlib.PurePath('{{tmpl_dir}}/{{tmpl_file2}}'), pathlib.Path('target_dir/file2.txt')),
    }


def test_remove_stale(tmp_path: pathlib.Path):
    root = pathlib.Path(__file__).parent / 'test_e2e'
    template_root = root / 'templates' / 'jinja' / 'simple'

    (tmp_path / 'stale_file.txt').write_text('test file')
    stale_dir = tmp_path / 'stale_dir'
    stale_dir.mkdir()
    (stale_dir / 'stale_file.txt').write_text('another test file')

    rybak.render(
        rybak.jinja.JinjaAdapter(loader=jinja2.FileSystemLoader(template_root)),
        data,
        tmp_path,
        exclude_extend=['{{tmpl_dir}}/excluded_file.txt'],
        remove_suffixes=['.jinja'],
        remove_stale=True,
    )

    assert dir_content(root / 'output' / 'simple') == dir_content(tmp_path)


def test_no_remove_stale(tmp_path: pathlib.Path):
    root = pathlib.Path(__file__).parent / 'test_e2e'
    template_root = root / 'templates' / 'jinja' / 'simple'

    (tmp_path / 'stale_file.txt').write_text('test file')
    stale_dir = tmp_path / 'stale_dir'
    stale_dir.mkdir()
    (stale_dir / 'stale_file.txt').write_text('another test file')

    rybak.render(
        rybak.jinja.JinjaAdapter(loader=jinja2.FileSystemLoader(template_root)),
        data,
        tmp_path,
        exclude_extend=['{{tmpl_dir}}/excluded_file.txt'],
        remove_suffixes=['.jinja'],
        remove_stale=False,
    )

    assert dir_content(root / 'output' / 'simple') != dir_content(tmp_path)
