Rybak
===

Project generator library based on [Mako Templates](https://www.makotemplates.org/).

Goals:
- generate projects based on a user-provided template and data,
- keep track and remove files that aren't produced by the template, but accept path patterns to keep,
- allow for multiple files to be generated from a single template file,
- support but don't require templates to be git or other DCVS repositories.

Non-goals:
- command line interface,
- prompting users for template data.