"""
This example shows how tables look with ASCII characters and then again with
Unicode characters. See figures/eg_table.png.
"""

import numpy as np
import itrm

x = [[-1.00,          -0.0000123456789, -0.000123456789, "abcdefghij"],
    [ -0.00123456789, -0.0123456789,    -0.123456789,    "abcdefghi"],
    [ -1.23456789,    -12.3456789,      -123.456789,     "abcdefgh"],
    [ -1234.56789,    -12345.6789,      -123456.789,     "abcdefg"],
    [ -1234567.89,    -12345678.9,      -123456789.0,    "abcdef"],
    [ -1234567890.0,  -12345678900.0,   -123456789000.0, "abcde"]]
names = ['apples', 'bananas', 'pears', 'oranges', 'grapes', 'cherries']
headers = ['Set 1', 'Set 2', 'Set 3', 'Set 4']
itrm.table(x, left=names, head=headers, width=6, uni=False)
print()
itrm.table(x, left=names, head=headers, width=24, uni=True)
