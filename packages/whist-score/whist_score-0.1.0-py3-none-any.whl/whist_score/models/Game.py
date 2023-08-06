from typing import Union
import json
import sys
import os
from colorama import Fore, Style
from whist_score.models.Player import Player
from whist_score.models.Message import Message
from whist_score.models.RoundTypes import (
    BaseMiserieClass,
    Abondance,
    VragenEnMeegaan,
    Solo,
    GroteMiserie,
    KleineMiserie,
    GroteMiserieOpTafel,
    Troel,
    Piccolo,
)

from whist_score.constants import (
    SAVE_FOLDER,
    CONFIG_FOLDER,
    GAME_TYPES_FILE_NAME,
    VRAGEN_EN_MEEGAAN,
    SOLO,
    ABONDANCE,
    GROTE_SOLO_SLIM,
    KLEINE_SOLO_SLIM,
)
from whist_score.utils import read_json
from tabulate import tabulate


message = Message()


class Game:
    def __init__(
        self,
        current_round: int = 1,
        players: list = [None, None, None, None],
        scoresheet: list = [],
        current_game_id: Union[None, int] = None,
    ):
        self.current_round = current_round
        self.players = players
        self.scoresheet = scoresheet
        self.current_game_id = current_game_id

    def display_points(self):
        print()
        message.message(
            tabulate(
                self.scoresheet,
                headers=[player.name for player in self.players],
                tablefmt="fancy_grid",
                showindex=[x + 1 for x in range(len(self.scoresheet))],
            )
        )
        print()

    def add_record_to_scoresheet(self) -> None:
        self.scoresheet.append(
            (
                self.players[0].score,
                self.players[1].score,
                self.players[2].score,
                self.players[3].score,
            )
        )

    def remove_record_from_scoresheet(self) -> None:
        del self.scoresheet[-1]

    def update_record(self, record_id: int, new_values: list) -> None:
        for index, item in enumerate(new_values):
            if isinstance(item, int):
                self.scoresheet[record_id][index] = new_values[index]

    def menu(self):
        while True:
            message.header("Menu")
            message.options(option="N", message="Next round")
            message.options(option="S", message="Nave game")
            message.options(option="D", message="Display scoresheet")
            message.options(option="R", message="Remove last record from scoresheet")
            message.options(option="M", message="Modify score")
            message.options(option="Q", message="Quit")
            message.footer()
            message.message("Choose your next action from the menu:")
            answer = message.input()
            match answer:
                case "n":
                    break
                case "s":
                    self.save()
                case "q":
                    self.exit()
                case "d":
                    self.display_points()
                case "r":
                    self.remove_record()
                case "m":
                    if len(self.scoresheet) == 0:
                        message.error(
                            message="No score record(s) available to modify.",
                        )
                        continue
                    self.modify_scoresheet()
                case _:
                    message.error(message="Command not recognized.")
                    continue

    def exit(self):
        while True:
            message.message("Are you sure you wish to exit? (y/N)")
            quitting = message.input()
            match quitting:
                case "n" | "":
                    break
                case "y":
                    sys.exit(0)
                case _:
                    message.error("Command not recognized.")
                    continue

    def remove_record(self):
        while True:
            self.display_points()
            message.message(
                f"Record {len(self.scoresheet)} will be removed. Are you sure? (y/N)"
            )
            removing = message.input()
            match removing:
                case "n" | "":
                    break
                case "y":
                    try:
                        self.remove_record_from_scoresheet()
                    except IndexError:
                        message.error(
                            "Unable to remove last record from scoresheet: the scorelist seems to be empty."
                        )
                    except Exception as e:
                        message.error(
                            f"An error occurred while trying to remove last record from scoresheet: {e}"
                        )
                    self.display_points()
                    break
                case _:
                    message.error("Command not recognized.")
                    continue

    def modify_scoresheet(self):
        while True:
            self.display_points()
            message.message("Please select the record to modify (q to return to menu):")
            removing = message.input()
            try:
                if removing == "q":
                    return
                if int(removing) not in range(1, len(self.scoresheet) + 1):
                    raise ValueError()
                break
            except ValueError:
                message.error("Please select a valid number.")
                continue
            except Exception as e:
                message.error(f"An unexpected error occurred: {e}")
                continue
        while True:
            message.message(
                "Please provide new points for this record, all seperated by a space. If you do not want to change a specific value, put x instead of the new value:"
            )
            new_values = input("> ").strip()
            try:
                new_values = new_values.split()
                if len(new_values) != 4:
                    raise ValueError()
                for index, item in enumerate(new_values):
                    try:
                        new_values[index] = int(item)
                    except ValueError:
                        new_values[index] = "x"
                    except Exception as e:
                        message.error(f"An unexpected error occurred: {e}")
                        continue
                self.update_record(record_id=int(removing) - 1, new_values=new_values)
                message.success("Successfully updated record.")
                self.display_points()
                break
            except ValueError:
                message.error("Please insert 4 valid numbers.")
                continue
            except Exception as e:
                message.error(f"An unexpected error occurred: {e}")
                continue

    def save(self):
        payload = {
            "current_round": self.current_round,
            "scoresheet": self.scoresheet,
            "players": [player.name for player in self.players],
        }
        while True:
            message.message("Give a name for the file (leave empty to cancel):")
            answer = message.input(lower=False)
            if answer == "":
                message.error("Saving game cancelled.")
                break
            try:
                with open(f"{SAVE_FOLDER}{answer}.json", "w") as f:
                    json.dump(payload, f, indent=2)
                message.success(f"Successfully saved to {SAVE_FOLDER}{answer}.json")
                break
            except Exception as e:
                message.error(f"An unexpected error occurred: {e}")
                continue

    def new_game(self):
        while True:
            message.message(
                "Please insert the names of the 4 players, all separated by a space:"
            )
            players = message.input().split()
            try:
                if len(players) != 4:
                    raise ValueError()
                break
            except ValueError:
                message.error("Please provide exactly 4 player names.")
                continue
            except Exception as e:
                message.error(f"Error while fetching players: {e}\n\nPlease try again.")
                continue
        players = [Player(name=player_name) for player_name in players]
        print()
        for i, player in enumerate(players):
            message.message(f"Player {i+1}: {player.name}")
        print()
        self.players = players
        self.new_round()

    def load_game(self):
        while True:
            try:
                json_files = [
                    pos_json
                    for pos_json in os.listdir(SAVE_FOLDER)
                    if pos_json.endswith(".json")
                ]
                if len(json_files) == 0:
                    message.error("No valid save files detected.")
                    return
                print()
                for index, name in enumerate(json_files):
                    message.options(
                        option=index,
                        message=f"\t{name}",
                        remove_first_letter_of_message=False,
                    )
                message.message("Please select a game to load (q to return):")
                answer = message.input()
                if answer == "q":
                    return
                try:
                    answer = int(answer)
                    if answer not in range(len(json_files)):
                        raise ValueError("Please select a valid number.")
                except ValueError:
                    message.error("Please provide a valid number.")
                    continue
                with open(f"{SAVE_FOLDER}{json_files[answer]}", "r") as f:
                    payload = json.load(f)
                break
            except Exception as e:
                message.error(f"An unexpected error occurred while loading game: {e}")
                continue
        players = []
        for index, item in enumerate(payload["players"]):
            player_score = (
                0
                if len(payload["scoresheet"]) == 0
                else payload["scoresheet"][-1][index]
            )
            players.append(Player(name=item, score=player_score))
        self.current_round = payload["current_round"]
        self.scoresheet = payload["scoresheet"]
        self.players = players
        self.new_round()

    def new_round(self):
        while True:
            self.display_points()
            self.menu()
            print()
            message.success("Starting new round...")
            print()
            current_game_type = choose_game_type()
            current_game = choose_players(
                game=self, current_game_type=current_game_type
            )
            if not current_game:
                continue

            if issubclass(type(current_game), BaseMiserieClass):
                current_game.complete()
                current_game.assign_points()
            else:
                while True:
                    answer = input("How many tricks were achieved? ").strip()
                    try:
                        answer = int(answer)
                        if answer not in range(0, 14):
                            continue
                        break
                    except ValueError:
                        message.error("Please provide a number.")
                    except Exception as e:
                        message.error(f"An unexpected error occurred: {e}")
                        continue
                current_game.assign_points(tricks_achieved=answer)
            self.add_record_to_scoresheet()
            self.current_round += 1


def choose_game_type() -> dict:
    message.header("Game Types")
    game_types = read_json(f"{CONFIG_FOLDER}{GAME_TYPES_FILE_NAME}")
    for index, item in enumerate(game_types):
        message.options(
            option=index,
            message=f"\t{item['name']}",
            remove_first_letter_of_message=False,
        )
    message.footer()
    while True:
        message.message("Select new game:")
        game_number = message.input()
        try:
            game_number = int(game_number)
        except ValueError:
            message.error("Please provide a number.")
        except Exception as e:
            message.error(f"An unexpected error occurred: {e}")
            continue
        if game_number in range(len(game_types)):
            valid = False
            while True:
                message.message(
                    f"Chosen game: {Fore.BLUE}{game_types[game_number]['name']}{Style.RESET_ALL}. Is this correct? (Y/n):"
                )
                validity = message.input()
                match validity:
                    case "y" | "":
                        valid = True
                        break
                    case "n":
                        valid = False
                        break
                    case _:
                        continue
            if valid:
                break
        else:
            message.error("Please provide a valid number.")
            continue
    return game_types[game_number]


def choose_players(game: Game, current_game_type: dict) -> Union[None, object]:
    while True:
        print()
        message.header("Choose players")
        for index, value in enumerate(game.players):
            message.options(
                option=f"{index + 1}",
                message=f"\t{value.name}",
                remove_first_letter_of_message=False,
            )
        print()
        message.options(
            option="Q", message="\tQuit new round", remove_first_letter_of_message=False
        )
        message.footer()
        message.message(
            f"Who is playing {Fore.BLUE}{current_game_type['name']}{Style.RESET_ALL}? If more players, please separate with a space:"
        )
        players = message.input()
        if players == "q":
            return
        try:
            playing_players = players.split()
            for index, player in enumerate(playing_players):
                playing_players[index] = game.players[int(player) - 1]
            other_players = [x for x in game.players if x not in playing_players]
        except ValueError:
            message.error(
                "Please provide one or more valid numbers, separated by a space if necessary."
            )
            continue
        except Exception as e:
            message.error(f"An unexpected error occurred: {e}")
            continue
        try:
            match current_game_type["type"]:
                case "Solo":
                    if len(playing_players) != 1:
                        message.error(f"Please select 1 player for a game of {SOLO}.")
                        continue
                    current_game = Solo(
                        number_of_tricks=current_game_type["number_of_tricks"],
                        playing_players=playing_players,
                        other_players=other_players,
                    )
                case "Vragen en Meegaan":
                    if len(playing_players) != 2:
                        message.error(
                            f"Please select 2 players for a game of {VRAGEN_EN_MEEGAAN}"
                        )
                        continue
                    current_game = VragenEnMeegaan(
                        number_of_tricks=current_game_type["number_of_tricks"],
                        playing_players=playing_players,
                        other_players=other_players,
                    )
                case "Abondance":
                    if len(playing_players) != 1:
                        message.error(
                            f"Please select 1 player for a game of {ABONDANCE}/{KLEINE_SOLO_SLIM}/{GROTE_SOLO_SLIM}."
                        )
                        continue
                    current_game = Abondance(
                        number_of_tricks=current_game_type["number_of_tricks"],
                        playing_players=playing_players,
                        other_players=other_players,
                    )
                case "Miserie":
                    match current_game_type["name"]:
                        case "Kleine Miserie":
                            current_game = KleineMiserie(
                                playing_players=playing_players,
                                other_players=other_players,
                            )
                        case "Grote Miserie":
                            current_game = GroteMiserie(
                                playing_players=playing_players,
                                other_players=other_players,
                            )
                        case "Piccolo":
                            current_game = Piccolo(
                                playing_players=playing_players,
                                other_players=other_players,
                            )
                        case "Grote Miserie op tafel":
                            current_game = GroteMiserieOpTafel(
                                playing_players=playing_players,
                                other_players=other_players,
                            )
                case "Troel":
                    if len(playing_players) != 2:
                        message.error("Please select 2 players for a game of Troel.")
                        continue
                    while True:
                        message.message("Did you keep the current trump? (Y/n): ")
                        answer = message.input()
                        match answer:
                            case "y" | "":
                                number_of_tricks = current_game_type[
                                    "number_of_tricks"
                                ]["trump_kept"]
                                current_game = Troel(
                                    number_of_tricks=number_of_tricks,
                                    playing_players=playing_players,
                                    other_players=other_players,
                                    trump_changed=False,
                                )
                                break
                            case "n":
                                number_of_tricks = current_game_type[
                                    "number_of_tricks"
                                ]["trump_changed"]
                                current_game = Troel(
                                    number_of_tricks=number_of_tricks,
                                    playing_players=playing_players,
                                    other_players=other_players,
                                    trump_changed=True,
                                )
                                break
                case _:
                    message.error("Please provide a valid value.")
                    continue
            break
        except ValueError as e:
            message.error(f"{e}")
        except Exception as e:
            message.error(f"An unexpected error occurred: {e}")
    return current_game
