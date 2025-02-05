import random
import os
import time
import argparse

# Add these new classes
class Dice:
    @staticmethod
    def low_weighted_roll():
        # Returns a low weighted dice roll (biased toward low numbers)
        return random.choices(range(1, 7), weights=[4, 4, 3, 2, 1, 1])[0]

    @staticmethod
    def two_dice_forced(round_total):
        # Splits the forced round total into two plausible dice values
        dice1 = random.randint(max(1, round_total - 6), min(6, round_total - 1))
        dice2 = round_total - dice1
        return dice1, dice2


class ConsolePrinter:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
        
    @staticmethod
    def print_table(rounds_results):
        print("{:<6} {:<7} {:<7} {:<20} {:<20}".format(
            "Round", "Dice 1", "Dice 2", "Total Dice Score", "Cumulative Dice Score"))
        for r, d1, d2, tot, cum in rounds_results:
            print("{:<6} {:<7} {:<7} {:<20} {:<20}".format(r, d1, d2, tot, cum))


class DiceGame:
    def __init__(self, interactive=False, round_delay=0.5, total_rounds=10, target_score=69):
        self.interactive = interactive
        self.round_delay = round_delay
        self.total_rounds = total_rounds
        self.target_score = target_score
        self.rounds_results = []
        self.cumulative_score = 0

    def play_round(self, turn):
        if turn <= 7:
            dice1 = Dice.low_weighted_roll()
            dice2 = Dice.low_weighted_roll()
            round_total = dice1 + dice2
        else:
            required_sum = self.target_score - self.cumulative_score
            remaining_rounds = self.total_rounds - (turn - 1)
            min_possible = max(2, required_sum - (remaining_rounds - 1) * 12)
            max_possible = min(12, required_sum - (remaining_rounds - 1) * 2)
            round_total = random.randint(min_possible, max_possible)
            dice1, dice2 = Dice.two_dice_forced(round_total)
        self.cumulative_score += round_total
        self.rounds_results.append((turn, dice1, dice2, round_total, self.cumulative_score))

    def run(self):
        for turn in range(1, self.total_rounds + 1):
            self.play_round(turn)
            ConsolePrinter.clear()
            ConsolePrinter.print_table(self.rounds_results)
            if self.interactive and turn < self.total_rounds:
                _ = input("go hard, go soft, go dirty? (h/s/d): ")
                time.sleep(self.round_delay)
            elif not self.interactive:
                time.sleep(self.round_delay)
        if self.cumulative_score == self.target_score:
            print("\nCongratulations! You hit {} and win!".format(self.target_score))
        else:
            print("\nGame resulted in", self.cumulative_score)
        return {"cumulative_score": self.cumulative_score, "rounds": self.rounds_results}

class GameSimulator:
    def __init__(self, num_games, interactive=False, round_delay=0.0):
        self.num_games = num_games
        self.interactive = interactive
        self.round_delay = round_delay
        self.games = []

    def run(self):
        for i in range(self.num_games):
            print(f"Simulating Game {i+1}")
            game = DiceGame(interactive=self.interactive, round_delay=self.round_delay)
            result = game.run()
            self.games.append(result)
            if self.interactive:
                print(f"Game {i+1} complete. Press Enter to continue...")
                input()
        self.print_statistics()

    def print_statistics(self):
        total_games = len(self.games)
        wins = sum(1 for game in self.games if game["cumulative_score"] == 69)
        print("\nSimulation Statistics:")
        print("Total games simulated:", total_games)
        print("Number of winning games (score 69):", wins)
        avg = sum(game["cumulative_score"] for game in self.games) / total_games
        print("Average cumulative score:", avg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dice Rolling CLI Game")
    parser.add_argument('--dev', action='store_true', 
                        help="Run in development mode: simulate multiple games instantly")
    parser.add_argument('--n', type=int, default=1, 
                        help="Number of games to simulate in dev mode")
    parser.add_argument('--lauren', action='store_true', 
                        help="Player mode with interactive round prompts (h/s/d)")
    args = parser.parse_args()

    if args.lauren:
        # Lauren mode: interactive game with a tactile delay (0.5 seconds)
        game = DiceGame(interactive=True, round_delay=0.5)
        game.run()
    elif args.dev:
        simulator = GameSimulator(num_games=args.n, interactive=False, round_delay=0)
        simulator.run()
    else:
        # Default mode uses one game, non-interactive with a standard delay
        game = DiceGame()
        game.run()
