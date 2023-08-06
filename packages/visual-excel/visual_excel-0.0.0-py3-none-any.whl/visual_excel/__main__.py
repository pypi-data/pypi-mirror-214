"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Visual Excel."""


if __name__ == "__main__":
    main(prog_name="visual-excel")  # pragma: no cover
