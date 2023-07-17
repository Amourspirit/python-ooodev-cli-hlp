# OooDev CLI Help

[OOO Development Tools](https://python-ooo-dev-tools.readthedocs.io/en/latest/index.html) (OooDev) is a framework for working with the LibeOffice API in Python.

This package provides a command line interface (CLI) for OooDev.

## Usage

Search for a phrase in the CLI help. The search will display matches.
Entering a number to that match followed by enter will open the help link in you default browser.

```bash
$ odh hlp -s "Write.Append"

Choose an option (default 1):
[0],  Cancel (or press q followed by enter)
[1],  ooodev.office.write.Write.append                                 - method     - py
[2],  ooodev.office.write.Write.append_date_time                       - method     - py
[3],  ooodev.office.write.Write.append_line                            - method     - py
[4],  ooodev.office.write.Write.append_para                            - method     - py
```

This project is templated from [python-sphinx-cli-help](https://github.com/Amourspirit/python-sphinx-cli-help). See the [wiki search](https://github.com/Amourspirit/python-sphinx-cli-help/wiki/Searching) for extended searching options.
