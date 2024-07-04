# Tic-Tac-Toe-MCTS
Playing Tic-Tac-Toe game against system using Monte Carlo Tree Search.

## Description:
User vs System based Tic-Tac-Toe game, where system makes decision using MCTS.

### Monte Carlo Tree Search (MCTS)
> It is a heuristic driven search algorithm for decision processes, most notably employed in the 
system that plays board games like *Chess*, *Go*, *Shogi*, *Tic-tac-toe* etc.

> It's a probabilistic and search algorithm that combines ***Classic tree search*** implemenatation alongside ***Reinforcement Learning*** principles.

> It's most often used to perform game simulations based on **Game Tree**.

This algorithm primarily works in four phases.
1. **Selection**

   This phase selects the particular move from all the possible moves which has a maximum value of **UCT(Upper Confidence Bound applied to Trees)** based on *UCB1* formula.
   > This UCT formula tries to balance the *Exploitation* and *Exploration* in tree search.

2. **Expansion**

   This phase expands node from selected move and start looking one level deeper. The node it got expanded from becomes parent and its children become the possible next moves.

3. **Rollout**

   It is also known as **Simulation**. This phase simulates the game from the selected child node from Selection phase and continue the game by making random choices until we reach the terminal state.

4. **Backpropagation**

   This phase backpropagate and update the result found in Simulation phase way through till the root node.

## References:
1. [YouTube](https://youtube.com/playlist?list=PLLfIBXQeu3aanwI5pYz6QyzYtnBEgcsZ8&si=nP2gh1awko8INjL2).
2. [Github](https://github.com/pbsinclair42/MCTS).

## Contains:
* tic-tac-toe.py - Game file
* mcts.py - MCTS algorithm.
   
