execute if score $counter count = $size count run data modify storage builder queue set from storage builder temp
execute if score $counter count = $size count run return run scoreboard players set $counter count 0

function builder:build

execute if score $offset count matches 0 positioned ~ ~15 ~1 run function builder:direction/west
execute unless score $offset count matches 0 positioned ~ ~-1 ~ run function builder:direction/west