A project to find and rank the top superspreaders of misinformation on Twitter using the [FIB-index](./fib_index.md).

This site makes up the official documentation of everything that is needed to know about the project.

- Source code: [https://github.com/mr-devs/top-fibers](https://github.com/mr-devs/top-fibers)
- Documentation code: [https://github.com/mr-devs/top-fibers/tree/main/docs](https://github.com/mr-devs/top-fibers/tree/main/docs)

### Contents
- [Setting up the project](./setup/setup.md)
    - [Setting up an environment](./setup/environment.md)
    - [Local package install (required)](./setup/package_install.md)
- [Understand how the code works](./code/overview.md)
- [Input data](./data.md)
- [FIB-index](./fib_index.md)
- [Updating this documentation](./documentation.md)


{%- assign date_format = site.minima.date_format | default: '%b %-d, %Y' -%}
{%- if page.last_modified_at -%}
    Last updated: {%- page.last_modified_at | date: date_format -%}
{%- else -%}
    Last updated: {%- page.date | date: date_format -%}
{%- endif -%}