"""Read a parquet file and print out as CSV on stdout."""

import sys

import click
import pandas as pd

@click.command()
@click.argument("file", type=click.Path(exists=True, file_okay=True, dir_okay=False))
def pqcat(file):
    """Read a parquet file and print out as csv on stdout."""
    df = pd.read_parquet(file, engine="pyarrow")
    df.to_csv(sys.stdout, index=False)


if __name__ == "__main__":
    pqcat()
