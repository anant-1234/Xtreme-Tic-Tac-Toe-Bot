# Xtreme-Tic-Tac-Toe-Bot
Xtreme Tic Tac Toe Bot made using Adversarial Search Techniques.
# Report Bot Assignment
## Team 16
## AI - BOT
## HEURISTIC
The heuristic takes into account various factors:
1. Winning on a small board is given weight (wt = 1500).
2. Winning on big boards is given weight (wt = 2500).
3. Blocking on big boards (wt = 1700).
4. Blocking on small boards (wt = 1200).
5. Having a pattern oo* on big boards (wt = 900)
6. Having a pattern oo* on small boards (wt = 700)
The above weights are added in the heuristic value for ‘o’ who is the maximizer and subtracted for ‘x’ who is the minimizer.
## Discount Factor 
We have also used the concept of Discount factor in cases of the above mentioned factors. We iterate in reverse fashion and multiply the weights for each by a certain discount factor (different for different weights). The intuition behind this is that the rewards at lower depths are less significant than short term rewards (rewards at immediate move). 
## Defence flag
In the situations where we get a second turn we switch our strategy to defensive mode. In cases where there is a tie in heuristic of different leaves, this helps to choose the move where blocking is given slightly more weight than attacking.
## Analysis of Games Played
The detailed analysis is present in the file Report.pdf
