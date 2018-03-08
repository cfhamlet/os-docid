# os-docid

[![Build Status](https://www.travis-ci.org/cfhamlet/os-docid.svg?branch=master)](https://www.travis-ci.org/cfhamlet/os-docid)
[![codecov](https://codecov.io/gh/cfhamlet/os-docid/branch/master/graph/badge.svg)](https://codecov.io/gh/cfhamlet/os-docid)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/os-docid.svg)](https://pypi.python.org/pypi/os-docid)
[![PyPI](https://img.shields.io/pypi/v/os-docid.svg)](https://pypi.python.org/pypi/os-docid)

DocID for fun.

# Install

  `$ pip install os-docid`

# Usage

  * API
  ```
  >>> from os_docid import docid
  
  >>> docid('http://www.google.com/')
  1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd
  
  >>> docid('1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd')
  1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd
  
  >>> docid('1d5920f4b44b27a8ed646a3334ca891fff90821feeb2b02a33a6f9fc8e5f3fcd')
  1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd
  
  >>> docid('abc')  
  NotImplementedError: Not supported data format
  ```

  * Command line
  ```
    $ os-docid -h
    usage: os-docid [-h] [-f INPUT_FILE] [-o {a,o}]

    Generate DocID.

    optional arguments:
      -h, --help            show this help message and exit
      -f INPUT_FILE, --file INPUT_FILE
                            file to be process (default: stdin)
      -o {a,o}, --output {a,o}
                            output format (default: [o]nly docid)
  ```

# Unit Tests
  `$ tox`

# License
  MIT licensed.
