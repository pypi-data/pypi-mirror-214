import random

mosse_per_vincere = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
last_human_move = None
last_bot_move = None
most_winning_moves = {'rock': 0, 'paper': 0, 'scissors': 0}
last_won = False
def intro():
    print("This is RPSbot, a Python bot for playing Rock-Paper-Scissors.")
    print("If you want to play, you just have to write 'rock', 'paper' or 'scissors' when asked.")
    print("The bot's moves are calculated before your input, so it couldn't just make the right move to win after seeing your move.")

def play_a_turn():
    bot_move = calc_next_move()
    return whoWins(input("Type your move: ").lower(), bot_move)

def whoWins(player_move, bot_move):
    global last_human_move
    global last_bot_move
    global last_won
    last_human_move = player_move
    last_bot_move = bot_move
    print("My move: "+bot_move)
    if player_move == bot_move:
        print("Tie! Let's do it again.")
        play_a_turn()
    elif mosse_per_vincere[player_move] == bot_move:
        print("I won.")
        most_winning_moves[bot_move] += 1
        last_won = True
    else:
        print("You won.")
        last_won = False

def calc_next_move():
    if last_human_move == None:
        return 'paper'
    if random.randrange(0,3) == 0:
        inv_map = {v: k for k, v in most_winning_moves.items()}
        return inv_map[max(inv_map.keys())]
    else:
        if not last_won:
            return mosse_per_vincere[last_human_move]
        else:
            return mosse_per_vincere[last_bot_move]

def main():
    intro()
    while True:
        play_a_turn()

if __name__ == '__main__':
    main()