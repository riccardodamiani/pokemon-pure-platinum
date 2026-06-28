# Encounters

## Changed encounter rates
Encounter rates for the following maps were changed:
| Map | Type | Original Rate| New Rate |
| :--- | :---: | :---: | :---: |
| Mt Coronet 4f, room 3 | Land | 15 | 10 |
| Mt Coronet 5f | Land | 15 | 10 |
| Mt Coronet 6f | Land | 15 | 10 |
| Route 206 | Land | 30 | 20 |
| Turnback cave | Land | 15 | 7 |
| Victory Road | Land | 15 | 10 |  
  
The changes were made for the following reasons:  
- made the route less annoying to go throught (route 206 or turnback cave)
- make them consistent with the rest of the game (Victory Road and Mt Coronet's)

## Encounter mechanics
In the original game every movement can trigger an encounter even when no actual step is taken (for example if you turn around on yourself).  
In the modded game the encounter is possible only when a full step is taken. This change will averall reduce the encounter rates on every map since turns are not considered for encounters anymore. The change is noticable expecially in cave puzzles since they generally require a lot of changing of directions.  
  

## Bicycle encounter change
The encounters are calculated as follows:
- first, a random roll is performed, and if the value is greater than the `flatEncounterRate`, no encounter will happen;
- then, a second random roll is compared with the local map encounter rate. If this succeeds, the encounter is guaranteed.
  
The `flatEncounterRate` starts at 40%, but it can be higher when riding a bicycle (+30%), walking in tall grass (+30%), and in some other cases.

So, when you move through grass while riding a bike, the `flatEncounterRate` increases from 40% to 70%, which is almost double the encounter rate you have by foot.
  
In the modded game, the bike flat encounter modifier was changed from the original +30% to -10%. This means that while riding a bike, you have about 25% less chance of encountering a Pokémon than when walking.

This change was made for the following reasons:
- many cave puzzles require moving with the bike, which in the original game caused a lot of unnecessary encounters;
- the bike is already penalized enough by its clunkiness in the game (especially in caves and tight areas). There is no need to penalize it further;
- if anything, a noisy bike would scare Pokémon away rather than attract them.
  
  
