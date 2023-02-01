from bsdl.scrape import *
import click
from halo import Halo


@click.group()
def main():
    pass


@click.command()
def hello():
    print("hello")


main.add_command(hello)


if __name__ == '__main__':
    main()
