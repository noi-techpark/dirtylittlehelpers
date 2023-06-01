# SPDX-FileCopyrightText: NOI Techpark <digital@noi.bz.it>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from sys import stdout

RED   = "\033[1;31m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"

def out(line):
    stdout.write(str(line))

def clr(color):
    out(color)
    
def red():
    clr(RED)

def green():
    clr(GREEN)
    
def reset():
    clr(RESET)

def outclr(line, color):
    clr(color)
    out(line)
    reset()

def outred(line):
    outclr(line, RED)

def outgreen(line):
    outclr(line, GREEN)
    
def outdiff(difftxt, show_equal_ignored = False):
    for line in difftxt.splitlines(True):
        if line[0] == '-':
            outred(line)
        elif line[0] == '+':
            outgreen(line)
        elif line[0] in ['i', ' ']:
            if show_equal_ignored:
                out(line)
        else:
            out(line)
