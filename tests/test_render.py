import pathlib
from typing import Optional

import jinja2

import rybak
import rybak.jinja

from .compare import dir_content

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
    logs: set[tuple[Optional[str], str]] = set()

    class ReportingEventSink(rybak.EventSink):
        def writing_file(self, template: pathlib.PurePath, target: pathlib.PurePath) -> None:
            logs.add((template.as_posix(), target.as_posix()))

        def unlinking_file(self, target: pathlib.PurePath) -> None:
            logs.add((None, target.as_posix()))

    (tmp_path / 'stale_file.txt').write_text('test file')

    template_root = pathlib.Path(__file__).parent / 'test_e2e' / 'templates' / 'jinja' / 'simple'

    rybak.TreeTemplate(
        rybak.jinja.JinjaAdapter(loader=jinja2.FileSystemLoader(template_root)),
        remove_suffixes=['.jinja'],
    ).render(
        data,
        tmp_path,
        event_sink=ReportingEventSink(),
        remove_stale=True,
    )

    assert logs == {
        (None, 'stale_file.txt'),
        ('{{tmpl_file1}}', 'file1.txt'),
        ('{{tmpl_file3}}', 'subdir/file3.txt'),
        ('{{tmpl_dir}}/excluded_file.txt', 'target_dir/excluded_file.txt'),
        ('{{tmpl_dir}}/suffixed.txt.jinja', 'target_dir/suffixed.txt'),
        ('{{tmpl_dir}}/{{tmpl_file2}}', 'target_dir/file2.txt'),
    }


def test_remove_stale(tmp_path: pathlib.Path):
    root = pathlib.Path(__file__).parent / 'test_e2e'
    template_root = root / 'templates' / 'jinja' / 'simple'

    (tmp_path / 'stale_file.txt').write_text('test file')
    stale_dir = tmp_path / 'stale_dir'
    stale_dir.mkdir()
    (stale_dir / 'stale_file.txt').write_text('another test file')

    rybak.TreeTemplate(
        rybak.jinja.JinjaAdapter(loader=jinja2.FileSystemLoader(template_root)),
        exclude_extend=['{{tmpl_dir}}/excluded_file.txt'],
        remove_suffixes=['.jinja'],
    ).render(
        data,
        tmp_path,
        remove_stale=True,
    )

    assert dir_content(tmp_path) == dir_content(root / 'output' / 'simple')


def test_no_remove_stale(tmp_path: pathlib.Path):
    root = pathlib.Path(__file__).parent / 'test_e2e'
    template_root = root / 'templates' / 'jinja' / 'simple'

    (tmp_path / 'stale_file.txt').write_text('test file')
    stale_dir = tmp_path / 'stale_dir'
    stale_dir.mkdir()
    (stale_dir / 'stale_file.txt').write_text('another test file')

    rybak.TreeTemplate(
        rybak.jinja.JinjaAdapter(loader=jinja2.FileSystemLoader(template_root)),
        exclude_extend=['{{tmpl_dir}}/excluded_file.txt'],
        remove_suffixes=['.jinja'],
    ).render(
        data,
        tmp_path,
        remove_stale=False,
    )

    assert set(dir_content(tmp_path)) == {
        ('file1.txt', 'foo'),
        ('stale_dir', None),
        ('stale_dir/stale_file.txt', 'another test file'),
        ('stale_file.txt', 'test file'),
        ('subdir', None),
        ('subdir/file3.txt', 'baz'),
        ('target_dir', None),
        ('target_dir/file2.txt', 'bar'),
        ('target_dir/suffixed.txt', 'test suffix removal\n'),
    }
