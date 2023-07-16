#!/usr/bin/env python
# coding: utf-8
import webbrowser
import sys

def main() -> int:
    # print(sys.argv[1])
    webbrowser.open(sys.argv[1])
    return 0

if __name__ == '__main__':
    SystemExit(main())