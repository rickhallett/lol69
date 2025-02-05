import random
import os
import time
import argparse

def low_weighted_roll():
    # We bias toward lower outcomes (1 and 2 are more likely)
    return random.choices(range(1, 7), weights=[4, 4, 3, 2, 1, 1])[0]

def simulate_game(interactive_round=False, round_delay=0.5):
    rounds_results = []
    cumulative_score = 0
    for turn in range(1, 11):
        if turn <= 7:
            dice1 = low_weighted_roll()
            dice2 = low_weighted_roll()
            round_total = dice1 + dice2
        else:
            required_sum = 69 - cumulative_score
            remaining_rounds = 10 - (turn - 1)
            min_possible = max(2, required_sum - (remaining_rounds - 1) * 12)
            max_possible = min(12, required_sum - (remaining_rounds - 1) * 2)
            round_total = random.randint(min_possible, max_possible)
            dice1 = random.randint(max(1, round_total - 6), min(6, round_total - 1))
            dice2 = round_total - dice1
        cumulative_score += round_total
        rounds_results.append((turn, dice1, dice2, round_total, cumulative_score))
        os.system('cls' if os.name == 'nt' else 'clear')
        print("{:<6} {:<7} {:<7} {:<20} {:<20}".format("Round", "Dice 1", "Dice 2", "Total Dice Score", "Cumulative Dice Score"))
        for r, d1, d2, tot, cum in rounds_results:
            print("{:<6} {:<7} {:<7} {:<20} {:<20}".format(r, d1, d2, tot, cum))
        if interactive_round:
            _ = input("go hard, go soft, go dirty? (h/s/d): ")
            time.sleep(round_delay)  # slight tactile delay after the input
        else:
            time.sleep(round_delay)
    if cumulative_score == 69:
        print("\nCongratulations! You hit 69 and win!")
    else:
        print("\nGame resulted in", cumulative_score)
    return {"cumulative_score": cumulative_score, "rounds": rounds_results}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dice Rolling CLI Game")
    parser.add_argument('--dev', action='store_true', help="Run in development mode (simulate multiple games)")
    parser.add_argument('--n', type=int, default=1, help="Number of games to simulate in dev mode")
    parser.add_argument('--lauren', action='store_true', help="Player mode with interactive round prompts (h/s/d)")
    args = parser.parse_args()
    
    if args.lauren:
        # Lauren mode: interactive round-by-round mode with a tactile delay (e.g., 0.5 seconds)
        simulate_game(interactive_round=True, round_delay=0.5)
    elif args.dev:
        all_games = []
        for i in range(args.n):
            print(f"Simulating Game {i+1}")
            # Dev mode: run game instantly with no pause between rounds
            result = simulate_game(interactive_round=False, round_delay=0)
            all_games.append(result)
            print(f"Game {i+1} complete. Press Enter to continue...")
            input()  # Optional pause for reviewing each game’s table
        # Print overall simulation statistics:
        total_games = len(all_games)
        wins = sum(1 for game in all_games if game["cumulative_score"] == 69)
        print("\nSimulation Statistics:")
        print("Total games simulated:", total_games)
        print("Number of winning games (score 69):", wins)
        avg = sum(game["cumulative_score"] for game in all_games) / total_games
        print("Average cumulative score:", avg)
    else:
        simulate_game()
