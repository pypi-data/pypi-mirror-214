from whist_score.utils import read_json, write_json
from dataclasses import dataclass


def adjust_points():
    pass


@dataclass
class PointsSystemDataclass:
    def __init__(self, player, other_players) -> None:
        self.player = player
        self.other_players = other_players


@dataclass
class MiseriePointsSystemDataclass:
    def __init__(
        self, punten_geslaagd, punten_niet_geslaagd, punten_anderen_niet_geslaagd
    ) -> None:
        self.punten_geslaagd = punten_geslaagd
        self.punten_niet_geslaagd = punten_niet_geslaagd
        self.punten_anderen_niet_geslaagd = punten_anderen_niet_geslaagd
