import random
from typing import List

intro = """NOTE: Press Ctrl + C to quit the game at any time.
Choose your character wisely. Each fighter has its own moves and stats!
To learn more, study the code here: https://goo.gl/5t8Re9 \n """

print(intro)


class Fighter():
    """Chooses fighter."""
    def __init__(self, name: str, hp: int, attack: int, defense: int, speed:
                 int, moves: List[str], max_hp: str):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = moves
        self.max_hp = max_hp

    def available_moves(self):
        """Returns a list of available moves."""
        return self.moves


class Game():
    """Runs the game."""
    def __init__(self):
        self.fighters = None
        self.player = None
        self.opponent = None
        self.turn_num = 0
        self.gameover = False
        self.create_fighters()

    def create_fighters(self):
        bread = Fighter("Bread", 200, 15, 10, 7, ["Hook Punch", "Replenish"],
                        200)
        oprah = Fighter("Oprah", 130, 12, 15, 6, ["Hyper Kick", "Super Heal"],
                        130)
        chris = Fighter("Chris", 140, 20, 8, 12, ["Curb Stomp", "Ramen Feast"],
                        140)
        dj_jmessic_arson = Fighter("DJ JMessicArson", 170, 12, 12, 15,
                                   ["Ninja Star Smash", "Freestyle Rap"], 170)
        self.fighters = [bread, oprah, chris, dj_jmessic_arson]

    def start(self):
        self.select_player_char()
        self.select_opponent_char()
        self.run()

    def select_player_char(self):
        for k, fighter in enumerate(self.fighters):
            print("%d: %s" % (k + 1, fighter.name))
        while True:
            try:
                choice = int(input("Choose your fighter: "))
            except ValueError:
                print("Input has to be a number.")
                continue
            if choice in range(1, len(self.fighters) + 1):
                self.player = self.fighters[choice - 1]
                print("You chose %s." % self.player.name)
                return
            print("Invalid choice. Try again.")

    def select_opponent_char(self):
        """Select opponent character."""
        while True:
            self.opponent = random.choice(self.fighters)
            if self.opponent != self.player:
                break
        print("Opponent chooses %s." % self.opponent.name)

    def run(self):
        """Main game loop."""
        while not self.gameover:
            self.print_status()
            self.turn()

    def turn(self):
        """Simulate one turn."""
        self.turn_num += 1
        print("Turn %d" % self.turn_num)
        print("=======")
        # select moves
        player_choice = self.get_player_choice()
        opponent_choice = self.get_opponent_choice()
        # test move selection
        print("You chose %s" % player_choice)
        print("Opponent chooses %s" % opponent_choice)
        # run moves
        if self.player.speed > self.opponent.speed:
            first = 1
        elif self.player.speed < self.opponent.speed:
            first = 2
        else:
            first = random.choice([1, 2])
        if first == 1:
            # player goes first
            self.use(self.player, player_choice, self.opponent)
            self.use(self.opponent, opponent_choice, self.player)
        else:
            # opponent goes first
            self.use(self.opponent, opponent_choice, self.player)
            self.use(self.player, player_choice, self.opponent)

    def get_player_choice(self):
        """Gets the user's choice."""
        available_moves = self.player.available_moves()
        for k, move in enumerate(available_moves):
            print("%d: %s" % (k + 1, move))
        while True:
            try:
                choice = int(input("Enter move: "))
            except ValueError:
                print("Input has to be a number.")
                continue
            if choice in range(1, len(available_moves) + 1):
                return available_moves[choice - 1]
            print("Invalid choice. Try again.")

    def get_opponent_choice(self):
        """Insert sick AI here."""
        return random.choice(self.opponent.available_moves())

    def check_gameover(self):
        if (self.player.hp <= 0 and self.opponent.hp <= 0 and
                self.player.speed > self.opponent.speed):  # player wins
            self.end(winner=1)
        elif (self.player.hp <= 0 and self.opponent.hp <= 0 and
                self.player.speed < self.opponent.speed):  # opponent wins
            self.end(winner=2)
        elif self.opponent.hp <= 0:  # player wins
            self.end(winner=3)
        elif self.player.hp <= 0:  # opponent wins
            self.end(winner=4)

    def end(self, winner: int):
        self.gameover = True
        if winner == 1 or 3:
            print("You win! Congrats. {}".format(self.opponent.hp))
        elif winner == 2 or 4:
            print("You lose. Rip.")

    def print_status(self):
        print("You have %d hp left" % self.player.hp)
        print("Opponent has %d hp left" % self.opponent.hp)

    def use(self, source, move: str, target=None):

        hp_list = [1.2, 1.1, .9]
        hk_list = [1.1, .9, .8]
        cs_list = [1.0, .8, .7]
        rep_list = [1.1, 1.0, .5, .3]
        sh_list = [1.1, 1.0, .8]
        nsm_list = [5.0, 2.0, 1.0]

        if move == "Hook Punch":
            hp_list = [1.2, 1.1, 1]
            if self.player.hp < 50:
                target.hp -= (60 * 1.6 * random.choice(hk_list) *
                              self.player.attack / self.opponent.defense)
            else:
                target.hp -= (60 * random.choice(hk_list) *
                              self.player.attack / self.opponent.defense)
        elif move == "Hyper Kick":
            target.hp -= (80 * random.choice(hp_list) *
                          self.player.attack / self.opponent.defense)
        elif move == "Replenish":
            if source.hp + 100 * random.choice(rep_list) > source.max_hp:
                source.hp = source.max_hp
            else:
                source.hp += 100
        elif move == "Super Heal":
            if source.hp + 80 * random.choice(sh_list) > source.max_hp:
                source.hp = source.max_hp
            else:
                source.hp += 80 * random.choice(sh_list)
        elif move == "Curb Stomp":
            target.hp -= (80 * random.choice(cs_list) * self.player.attack /
                          self.opponent.defense)
        elif move == "Ramen Feast":
            if source.hp < 30 and source.hp > 10:
                source.hp = source.max_hp
            elif source.hp + 75 > source.max_hp:
                source.hp = source.max_hp
            else:
                source.hp += 75
        elif move == "Ninja Star Smash":
            target.hp -= 40 * random.choice(nsm_list)
        elif move == "Freestyle Rap":
            target.hp = target.hp / 2
        self.check_gameover()


if __name__ == "__main__":
    game = Game()
    game.start()
