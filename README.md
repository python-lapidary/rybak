# Rybak

Project generator library.

Goals:

- generate projects based on a user-provided template and data,
- keep track and remove files that aren't produced by the template, but accept path patterns to keep,
- allow for multiple files to be generated from a single template file,
- support but don't require templates to be git or other DCVS repositories.

Non-goals:

- command line interface,
- prompting users for template data.

## Synopsis

Rybak (y is pronounced as in pick or sit) is an extension of template engines, which instead of rendering a single file or string, renders a whole directory.

In a way it's similar to [Cookiecutter](https://pypi.org/project/cookiecutter/) or [Copier](https://pypi.org/project/copier/), but while these programs are designed specifically for generating
software projects, rybak is a library for generating any directory tree structure.

Rybak template is a directory consisting of template files.
[Jinja](https://pypi.org/project/jinja2/),
[Mako](https://pypi.org/project/mako/)
and [Tornado](https://pypi.org/project/tornado/)
are supported, thou a single project can only use a single template engine.

Similarly to Cookiecutter and Copier, Rybak is template-driven, i.e. the contents of the template directory decides how the model data is used.

## Usage

```python
from pathlib import Path
from rybak import render
from rybak.jinja import JinjaRenderer
from jinja2 import Environment

render(
    Path('template_root'),
    Path('target_root'),
    JinjaRenderer(Environment()),
    {'likes': {
        'Alice': 'Bob',
        'Bob': 'Charlie',
        'Charlie': 'cats',
    }},
)
```

- `template_root`:
  is the directory containing template files, in this case Jinja templates. Templates can be used in file content, file names and directory names.

- `model`:
  is the data structure used by the template. You can use here whatever the template accepts.

### Single template multiple data

Template files can be applied to collections of items.
In order to do so, a special function is made available, `loop_over` that iterates over a passed collection. The function can only be used in templates in file names.

`loop_over` returns the element of the collection, so that it can be used to render name.

model:

```python
names = [
    'Alice',
    'Bob',
    'Charlie',
]
```

file name:
`{{loop_over(names)}}`
would produce three files: Alice, Bob and Charlie.

The current item is also available during rendering the file contents, as model variable `item`.

Of course, we might want different value in the file name and its content. For that we can manipulate the `loop_over`s result:

model:

```python
likes = {
    'Alice': 'Bob',
    'Bob': 'Charlie',
    'Charlie': 'cats',
}
```

file name: `{{loop_over(likes.items())[0]}}`

file content: `{{item[1]}}`

`loop_over(likes.items())` produces a key-value tuple for each file, and `[0]` accesses the key.

Similarly, `{{items}}` would produce the same key-value pair, and [1] accesses the value.

Alternatively, the model could be a list of complex objects:

model:

```python
likes = [
    {'name': 'Alice', 'likes': 'Bob'},
    {'name': 'Bob', 'likes': 'Charlie'},
    {'name': 'Charlie', 'likes': 'cats'},
]
```

In this case the file name template simplifies to `{{loop_over(likes).name}}` and the content template to `{{item.likes}}`.

## Installation

Rybak templates can work with either of Jinja, Mako or Torado; so typically you need to install Rybak and one of those libraries.

installing `rybak[jinja]`, `rybak[mako]` or `rybak[tornado]` will handle this.
