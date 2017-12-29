import os
import sys
import pytest
import shlex
import subprocess
from os_docid.cmdline import execute


def call(cmdline, env=None, **kwargs):
    if env is None:
        env = os.environ.copy()
    if env.get('COVERAGE', None) is not None:
        env['COVERAGE_PROCESS_START'] = os.path.abspath('.coveragerc')

    cmd = 'python -u %s %s' % (os.path.abspath(__file__), cmdline)
    proc = subprocess.Popen(shlex.split(cmd),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            cwd=os.getcwd(),
                            env=env,
                            **kwargs)
    stdout, stderr = proc.communicate()
    return stdout, stderr


def test_cmdline(tmpdir):
    f = tmpdir.join('testfile')
    f.write('http://www.google.com/')
    cmdline = '-f %s' % f.strpath
    stdout, stderr = call(cmdline)
    assert '1d5920f4b44b27a8-ed646a3334ca891f-ff90821feeb2b02a33a6f9fc8e5f3fcd' in stdout


if __name__ == "__main__":
    sys.path.insert(0, os.getcwd())
    if os.getenv('COVERAGE_PROCESS_START'):
        import coverage
        coverage.process_startup()
    execute()
