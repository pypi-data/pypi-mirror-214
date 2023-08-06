import click
from whist_score.views.games import new_game, load_game, settings
from whist_score.models.Message import Message
import importlib.metadata

message = Message()

distribution = importlib.metadata.distribution("whist_score")
version = distribution.version
url = distribution.metadata.get("home-page")


@click.command()
@click.option("--players", help="Names of 4 players, seperated by a semicolon (;)")
@click.version_option(version=version)
def main(players=None):
    if players:
        players = players.strip().split(";")
        if len(players) != 4:
            message.error("Please define 4 players, separated by a semicolon (;).")
            return
    version = distribution.version
    message.banner(version=version, url=url)
    while True:
        message.options(option="N", message="New game")
        message.options(option="L", message="Load game")
        # message.options(option="S", message="Settings")
        # choice = input("> ").strip().lower()
        choice = message.input()
        match choice:
            case "n":
                new_game(players=players)
                break
            case "l":
                load_game()
                break
            # case "s":
            #     settings()
            #     break
            case _:
                message.error("Please provide a valid option.")


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option()
@click.pass_context
def version():
    pass


if __name__ == "__main__":
    main()
