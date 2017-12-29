# os-docid

[![Build Status](https://www.travis-ci.org/cfhamlet/os-docid.svg?branch=master)](https://www.travis-ci.org/cfhamlet/os-docid)
[![codecov](https://codecov.io/gh/cfhamlet/os-docid/master/graph/badge.svg)](https://codecov.io/gh/cfhamlet/os-docid)

DocID for fun.(Python2)

# Install

  `$ pip install os-docid`

# Usage

  * API
  ```
    from os_docid import docid

    print docid('http://www.google.com/') 
    # 1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd

    print docid('1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd') 
    # 1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd

    print docid('1d5920f4b44b27a8ed646a3334ca891fff90821feeb2b02a33a6f9fc8e5f3fcd')
    # 1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd
  ```

  * Command line
  ```
    $ os-docid -h
    usage: os-docid [-h] [-f INPUT_FILE]

    Generate DocID.

    optional arguments:
      -h, --help            show this help message and exit
      -f INPUT_FILE, --file INPUT_FILE
                            file to be proecess (default: stdin)
  ```

# Unit Tests
  `$ tox`

# License
  MIT licensed.
