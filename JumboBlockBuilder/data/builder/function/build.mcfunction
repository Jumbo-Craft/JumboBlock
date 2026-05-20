scoreboard players set $offset count 0

function builder:setblock with storage builder queue[0]
data remove storage builder queue[0]

scoreboard players add $counter count 1
scoreboard players operation $offset count = $counter count
scoreboard players operation $offset count %= $width count
