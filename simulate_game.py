import itertools
from Pick import Pick, PickMove, PickState
from alpha_beta_algorithm import alphaBetaAlgorithm


def simulate_game(depth_1, depth_2):
    game = Pick(n=4)
    move_num = 1
    MaxPlayer = True
    while game.state.is_finished() == False:
        print('\nruch nr: ', move_num)
        print(game) 
        first_player_char = game.first_player.char
        current_player_char = game.state._current_player.char
        depth = depth_2 if current_player_char == first_player_char else depth_1

        whose_move = True if game.state._current_player.char == game.first_player.char else False
        value, move = alphaBetaAlgorithm(game.state, depth, float("-inf"), float("inf"), True)

        game.make_move(move)

        move_num+=1
   
    if game.state.get_winner():
        print("\n\n\n#### KONIEC GRY - Wygrany: ",game.state.get_winner().char, " ####")
        print(game)

        winner_char = game.state.get_winner().char
        winner_nums = game.state.current_player_numbers if game.state._current_player.char == winner_char else game.state.other_player_numbers
        combs = list(itertools.combinations(winner_nums, 4))
        sums = [sum(comb) for comb in combs]
        winning_comb = list(combs[sums.index(34)])
        winning_comb.sort()
        
        print("wygrywająca kombinacja: ", winning_comb)
        return winner_char
      
    else:
        print("\n\n\n#### KONIEC GRY  -  REMIS ####")
        print(game)
        return "R"
   
        
def main():
    
    num_of_1_plyer_wins = 0
    num_of_2_plyer_wins = 0
    num_of_draws = 0

    for i in range(30):
        char = simulate_game(4,1)

        if char == "1":
            num_of_1_plyer_wins += 1
        elif char == "2":
            num_of_2_plyer_wins += 1
        elif char == "R":
            num_of_draws += 1
        print("wygrane_1: ", num_of_1_plyer_wins, " wygrane_2: ", num_of_2_plyer_wins, " remisy: ", num_of_draws)
    




if __name__ == "__main__":
    main()
