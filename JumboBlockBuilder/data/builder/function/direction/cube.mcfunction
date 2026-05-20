execute if score $fill count matches 1 anchored feet positioned ~ ~ ~ run function builder:direction/fill with storage builder queue[0]
execute if score $bottom count matches 1 anchored feet positioned ~ ~ ~15 run function builder:direction/bottom
execute if score $east count matches 1 anchored feet positioned ~15 ~15 ~15 run function builder:direction/east
execute if score $west count matches 1 anchored feet positioned ~ ~15 ~ run function builder:direction/west
execute if score $top count matches 1 anchored feet positioned ~ ~15 ~ run function builder:direction/top
execute if score $north count matches 1 anchored feet positioned ~15 ~15 ~ run function builder:direction/north
execute if score $south count matches 1 anchored feet positioned ~ ~15 ~15 run function builder:direction/south
