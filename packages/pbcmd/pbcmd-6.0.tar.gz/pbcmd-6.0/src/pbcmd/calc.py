"""Simple calculator.

Implemeted as a Python expression evaluator.
"""

from math import *
from pandas import to_datetime as date, to_timedelta as timedelta

today = date("today")
now = date("now")

import click

def p2odds(p):
    return p / (1 - p)

def odds2p(o):
    return o / (1 + o)


@click.command()
@click.argument("expression")
def calc(expression):
    """Compute simple expressions."""

    print(eval(expression))


if __name__ == "__main__":
    calc()
