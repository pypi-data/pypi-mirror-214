# mkdocs-pages-j2-today

This plugin builds `.pages` files from `.pages.j2` files, using Jinja2 to render the templates.

```text
title: Page Title
nav:
    - Welcome: index.md
{%- for i in range(1,3) %}
    - My Page {{ i }}: p{{ i }}.md
{%- endfor %}
```
