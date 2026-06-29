# General changes

## Honey Tree Wait
Removed the waiting time of 6 hours after the honey tree is slather with honey. Now the encounter will be available immidiately and for the next 24 hours.  
The change was made to remove evil time wasting.  


## Egg Hatching
Reduced the number of steps required to hatch an egg. In the original game each egg cycle required 255 steps. Now it required only 40. This translates into a reduction of about 6.375 times the original amount of steps requirement.  
For example hatching an egg with low cycle requirement (i.e. pitchu, cleffa, togepi) needs 400 steps. Hatching an egg with high requirement (i.e. dratini, munchlax, lapras) needs 1600 steps.  
The change was made to remove as much as possible the grinding related to eggs hatching. The idea is that by lowering the number of steps, more players would prefer to passively hatch eggs during normal gameplay instead of wasting 20 minutes zooming around on their bikes. 

## Map Obstacles Changes
Removed some obstacles from the following maps:
- Orebourgh Gate b1f
- Mt Coronet 1f south
- Mt Coronet 2f
- Mt Coronet Outside 
- Mt Coronet 1f North Room 1
- Mt Coronet Tunnel Room
- Mt Coronet b1f
- Ravanged Path
- Route 210
- Route 211
- Route 212
- Route 213
- Route 214
- Route 222  
  
The idea was to remove any obstacle it's not required by the story/logic and that is not part of a somewhat interesting puzzle.  
The change was made to removed repetitive and time wasting task.

## Changed battle escape formula
In the original game the flee chances are calculated based on the pokemon speed. If your pokemon has a speed equal or greater than the wild pokemon, the flee is guaranteed. If it's lower the probability is calculates as 50% * (your speed) / (wild mon speed) plus 11% for every escape attempt.  
So, if your pokemon has 40 speed and opponent has 50, in your first attemp to flee your chances are 40%. On your second attemp are 51%, on your third are 62% and so on..  
Now the formula was changes as follows: 100% * (your speed) / (wild mon speed) plus 6% for every escape attempt.  
Moreover, was fixed a variable overflow bug in the formula.  
The change was made to make the probability scale linearly with the speed. In the original game if the pokemon were speed tide you could always flee, if you had 1 point less than your opponent you start from 50% escape probability. Now, if your pokemon is 90% speed of the opponent's you start from 90% probability of escaping.  
