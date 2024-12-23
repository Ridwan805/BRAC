import random 

def AB_pruning(depth, is_schorpion_turn, child, alpha, beta, max_depth, branching_factor, llist=None):
    if depth == max_depth and llist is not None:
        # Return leaf node value for task 2
        return llist[child]
        
    # Return static values for task 1
    if depth == max_depth:
        return random.choice([1,-1])
        # return random.randint(-1,1)

    if is_schorpion_turn == 0:#Maximizing Player
        max_v = float('-inf')
        for i in range(branching_factor):
            nvalue = AB_pruning(depth + 1, 1, child * 2 + i, alpha, beta, max_depth, branching_factor, llist)
            max_v = max(nvalue, max_v)
            alpha = max(alpha, nvalue)
            if beta <= alpha:
                break
        return max_v
    else:# Minimizing Player
        min_v = float('inf')
        for i in range(branching_factor):
            nvalue = AB_pruning(depth + 1, 0, child * 2 + i, alpha, beta, max_depth, branching_factor, llist)
            min_v = min(nvalue, min_v)
            beta = min(beta, nvalue)
            if beta <= alpha:
                break
        return min_v
    
print('Task 1')
#Task 1
def MainGame(player = random.randint(0,1)):
    max_depth = 5
    total_round = 3
    played_rounds = 0
    winning_scores = {'Scorpion' :0, 'Subzero': 0}
    round_winner = []
    starting = player
    for i in range(total_round):
        alpha = float('-inf')
        beta = float('inf')
        winner = AB_pruning(0, starting == 0, 0, alpha, beta, max_depth, 2)
        if winner == 1:
            round_winner.append('Subzero')
            winning_scores['Subzero'] += 1
            played_rounds += 1  
            if winning_scores['Subzero'] == 2:
                break
        else:
            round_winner.append('Scorpion')
            winning_scores['Scorpion'] += 1
            played_rounds += 1  
            if winning_scores['Scorpion'] == 2:
                break
        starting = not starting
        
    
    
    if winning_scores['Scorpion'] > winning_scores['Subzero']:
        print('Game Winner: Scorpion')
    else:
        print('Game Winner: Subzero')    
    print(f'Total Rounds Played: {played_rounds}')
    for i in range(len(round_winner)):
        print(f'Winner of Round {i+1} is {round_winner[i]}')

MainGame()

print()
print('Task 2')
#Task 2
def pgame(c,llist,depth,branching):
    LeftDarkMagic = max(llist[:4]) - c 
    RightDarkMagic = max(llist[4:]) - c
    if LeftDarkMagic > RightDarkMagic:
        darkmagic = LeftDarkMagic
        subtree = 'Left'
    else:
        darkmagic = RightDarkMagic
        subtree = "Right"
    alpha = float('-inf')
    beta = float('inf')
    noDarkMagic = AB_pruning(0, 0, 0, alpha, beta,depth,branching, llist)

    if darkmagic > noDarkMagic:
        return print(f"The new minimax value is {darkmagic}. Pacman goes {subtree} and uses dark magic")
    else:
        return print(f"The minimax value is {noDarkMagic}. Pacman does not use dark magic")
    
leaf = [3, 6, 2, 3, 7, 1, 2, 0]
pgame(2, leaf, 3, 2)