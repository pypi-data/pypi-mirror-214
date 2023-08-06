import click

from albhed import AlBhed


@click.command()
@click.option(
    "-r", "--revert", is_flag=True, default=False, help="Revert the translation"
)
@click.argument("string", nargs=-1)
def cli(revert: bool, string: str) -> None:
    """
    Converts Any Text to Al Bhed
    """
    t = AlBhed(" ".join(string))
    if revert:
        print(t.revert())
    else:
        print(t.translate())


if __name__ == "__main__":
    cli()
