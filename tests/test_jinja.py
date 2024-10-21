import pytest
from jinja2 import Environment, FileSystemLoader

from rybak.jinja import JinjaAdapter


def test_jinja_init_keep_newlines():
    env = Environment(loader=FileSystemLoader('-path-'))
    adapter = JinjaAdapter(env)

    assert adapter._env.keep_trailing_newline is True


def test_jinja_init_keep_newlines_false():
    env = Environment(loader=FileSystemLoader('-path-'))
    adapter = JinjaAdapter(env, keep_trailing_newline=False)

    assert adapter._env.keep_trailing_newline is False


def test_jinja_loader():
    loader = FileSystemLoader('-path-')
    adapter = JinjaAdapter(loader=loader)

    assert adapter._env.loader == loader


def test_jinja_env_loader_error():
    with pytest.raises(ValueError):
        JinjaAdapter(environment=Environment(), loader=FileSystemLoader('-path-'))


def test_jinja_no_env_loader_error():
    with pytest.raises(ValueError):
        JinjaAdapter()
