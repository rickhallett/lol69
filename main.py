import random
import os
import time

def low_weighted_roll():
    # We bias toward lower outcomes (1 and 2 are more likely)
    return random.choices(range(1, 7), weights=[4, 4, 3, 2, 1, 1])[0]

rounds_results = []
cumulative_score = 0
for turn in range(1, 11):
    if turn <= 7:
        # Use the biased function to simulate low dice throws
        dice1 = low_weighted_roll()
        dice2 = low_weighted_roll()
        round_total = dice1 + dice2
    else:
        # For the final 3 rounds, force the total to exactly reach 69.
        required_sum = 69 - cumulative_score
        remaining_rounds = 10 - (turn - 1)
        # Ensure the chosen total is plausible for two dice.
        min_possible = max(2, required_sum - (remaining_rounds - 1) * 12)
        max_possible = min(12, required_sum - (remaining_rounds - 1) * 2)
        round_total = random.randint(min_possible, max_possible)
        # Now “split” the round_total into two dice so it appears random
        dice1 = random.randint(max(1, round_total - 6), min(6, round_total - 1))
        dice2 = round_total - dice1
    cumulative_score += round_total
    rounds_results.append((turn, dice1, dice2, round_total, cumulative_score))
    
    os.system('cls' if os.name == 'nt' else 'clear')
    # Print table header
    print("{:<6} {:<7} {:<7} {:<20} {:<20}".format("Round", "Dice 1", "Dice 2", "Total Dice Score", "Cumulative Dice Score"))
    # Print each round’s results
    for r, d1, d2, tot, cum in rounds_results:
        print("{:<6} {:<7} {:<7} {:<20} {:<20}".format(r, d1, d2, tot, cum))
    time.sleep(1)   # Pause briefly so the table update is noticeable

if cumulative_score == 69:
    print("\nCongratulations! You hit 69 and win!")
