import click
import logging

from click_default_group import DefaultGroup
from dfsync.pycode import (
    generate_function,
    generate_docstring,
    generate_pytest,
    generate_analysis,
    generate_search_expansion,
)

logging.basicConfig(level=logging.DEBUG)


@click.group(cls=DefaultGroup, default="analyze", default_if_no_args=False)
def main():
    pass


@main.command(name="analyze")
@click.argument("source", nargs=-1)
def analyze(source):
    analyze_source(*source)


@main.command(name="tests")
@click.argument("source", nargs=-1)
def tests(source):
    tests = generate_pytest(*source)
    print(tests)


@main.command(name="func")
@click.argument("source", nargs=-1)
def function(source):
    code = generate_function(*source)
    print(code)


@main.command(name="docs")
@click.argument("source", nargs=-1)
def docstring(source):
    code = generate_docstring(*source)
    print(code)


@main.command(name="index")
@click.argument("source", nargs=-1)
def index(source):
    code = generate_search_expansion(*source)
    print(code)


if __name__ == "__main__":
    main()
