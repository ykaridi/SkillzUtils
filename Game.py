import json
from Constants import *


class Game(object):
    def __init__(self, json_str, link):
        self.data = json.loads(json_str)
        self.link = link

    def get_winner(self):
        winners = self.data["winnerNames"]
        if len(winners) != 1:
            return "Tie"
        else:
            return winners[0]

    def get_score(self):
        score = self.data["score"]
        return str(score[0]) + "-" + str(score[1])

    def get_length(self):
        return self.data["gameLength"]

    def get_players(self):
        return self.data["playerNames"]

    def get_link(self):
        return self.link
