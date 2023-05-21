# 2048_game
2048 game implementation in Python using pygame module.

About 80% of the code I used is not mine, but written by LeMasterTech (https://github.com/plemaster01/Python2048).
I used his implementation as base but completed the missing logic, as in his implementation the game would end when
every single tile had a value in it, which doesn't necessarly mean it's game over if there are still tiles mergeable,
so I fixed that. Additionally I changed how the tile, in which the new value will spawn every move, is picked, to make it 
more performant.

