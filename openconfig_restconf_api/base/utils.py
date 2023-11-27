#!/usr/bin/env python3

import subprocess


def rc_cmd(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    """Run command, get return code
    On success:
        * rc + stdout:
    On fail:
        * rc + stderr
    % rc_cmd('uname')
    (0, 'Linux\n')
    % rc_cmd('ip link show dev eth99')
    (1, 'Device "eth99" does not exist.\n')
    """
    command = command.split()
    response = subprocess.run(command, stdout=stdout, stderr=stderr, encoding='utf-8')
    rc = response.returncode
    if rc == 0:
        return rc, response.stdout
    return rc, response.stderr
