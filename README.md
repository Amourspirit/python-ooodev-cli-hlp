# Sphinx CLI Help

## Introduction

This project is a template for creating a command line interface for a Sphinx project.

Once a Sphinx project is built, the `objects.inv` file contains a list of all the objects in the project.

This project converts the `objects.inv` created by [Sphinx Docs](https://www.sphinx-doc.org) into a command line interface that allows for quick searching and launching the online help from the command line.


This project is designed as a template.
Using this template for your own project means that you can create and publish CLI package for any Sphinx project with very little configuration and No coding necessary.

## Getting Started

Create your own project by click the `Use this template` on GitHub.

### The `pyproject.toml` file

Edit the `pyproject.toml` file and change the following:

See the [Configure](https://github.com/Amourspirit/python-sphinx-cli-help/wiki/config.json) in the Wiki for more information

```toml
[custom.metadata]
pkg_out_name = "my_custom_help"
entry_point_name = "my-help"
build_dir = "build"
build_readme="sphinx_cli_help/README.md"
build_license=""

[tool.poetry]
name = "custom-sphinx-help"
version = "0.1.0"
description = "Command Line Help for my Custom Sphinx Project"
authors = ["Author Name <author@email.com>"]
license = "MIT"
readme = "README.md"
```

### The `config.json` file

The file is found in the `sphinx_cli_help` folder.

There are many configuration options available in the `config.json` file.
See the [config.json](https://github.com/Amourspirit/python-sphinx-cli-help/wiki/config.json) in the Wiki for more information.

To get started just change the `url_prefix` to the URL of your Sphinx project. and the `name` to the name of your project. Keep then name short and simple as it is used in the command line search options.

```json
{
  "url_prefix": [
        {
            "index": 0,
            "url": "https://python-ooo-dev-tools.readthedocs.io/en/latest/",
            "name": "OooDev"
        }
    ]
}
```

### Database

Under the hood a SQLite database is used to store the data parsed from `objects.inv` file.

See the [Import](https://github.com/Amourspirit/python-sphinx-cli-help/wiki/Import) in the Wiki for more information.

To create the Database for your Sphinx project, run the following command:

```bash
python -m app data init -i
```

To import a `objects.inv` file into a database, run the following command:

```bash
python -m app data update -u https://www.example.com/objects.inv
```

Run the following command to see the options for the `update` command:

```bash
python -m app data update -h
```

### Searching

To search the database, run the following command:

Note: The `cli-hlp` command name will change when your project is built.
It is set by the `entry_point_name` in the `pyproject.toml` file.

```bash
cli-hlp hlp -s "search term"
```

Will give a result something like this:

```text
$ cli-hlp hlp -s Write.append
Namespace(command='hlp', search=['Write.append'], leading=True, trailing=True, case_sensitive=False, limit=10, exclude=None, role='any')

Choose an option (default 1):
[0],  Cancel (or press q followed by enter)
[1],  ooodev.office.write.Write.append                                 - method     - py
[2],  ooodev.office.write.Write.append_date_time                       - method     - py
[3],  ooodev.office.write.Write.append_line                            - method     - py
[4],  ooodev.office.write.Write.append_para                            - method     - py
```

There are many options available for the `hlp` command.

Run the following command to see the options for the `hlp` command:

```bash
cli-hlp hlp -h
```


In this example, the `Write.append` method was found in the `ooodev.office.write` module.
A list of matching results is displayed and the user is asked to choose an option.

Choosing `2` and pressing enter will display the URL and open it in default browser:

 ```text
 2
https://python-ooo-dev-tools.readthedocs.io/en/latest/src/office/write.html#ooodev.office.write.Write.append_date_time
 ```

Read the [Wiki](https://github.com/Amourspirit/python-sphinx-cli-help/wiki) for the rest.

## LICENSE

This project is Licensed under the MIT License.

```text
The MIT License (MIT)

Copyright 2023 :Barry-Thomas-Paul: Moss

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
