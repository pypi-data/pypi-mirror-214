from whist_score.models.Player import Player
from whist_score.models.Game import Game
from whist_score.models.Message import Message

from whist_score.constants import ROOT_SETTINGS, POINT_SYSTEM_SETTINGS

message = Message()


def new_game(players: str):
    if not players:
        message.message(
            "Please provide the names of the 4 players, separated by a space."
        )
        while True:
            players = message.input(lower=False).split()
            try:
                if len(players) != 4:
                    raise ValueError()
                break
            except ValueError:
                message.error("Please provide exactly 4 player names.")
            except Exception as e:
                message.error(
                    f"An unexpected error occurred while parsing player names: {e}\n\nPlease try again."
                )
                players = None
    else:
        players = players.strip().split(";")
    players = [Player(name=player_name) for player_name in players]
    print()
    for i, player in enumerate(players):
        message.success(f"Player {i+1}: {player.name}")
    print()
    game = Game(players=players)
    game.new_round()


def load_game():
    game = Game()
    game.load_game()


def settings():
    print()
    message.header("Settings")
    while True:
        for index, value in enumerate(ROOT_SETTINGS):
            message.options(
                f"{index}",
                message=f"\t{value[index].get('name')}",
                remove_first_letter_of_message=False,
            )
        print()
        message.options(
            option="Q", message="\tQuit", remove_first_letter_of_message=False
        )
        answer = message.input()
        match answer:
            case "0":
                print()
                message.header("Point System")
                for index, value in enumerate(
                    POINT_SYSTEM_SETTINGS[int(answer)].get("options")
                ):
                    message.options(
                        option=f"{index}",
                        message=f"\t{value}",
                        remove_first_letter_of_message=False,
                    )
                point_system = message.input()
            case _:
                message.error("Please provide a valid number.")
