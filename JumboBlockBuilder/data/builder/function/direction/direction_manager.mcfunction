data modify storage builder temp set from storage builder queue

execute store result score $stairs count run data get storage builder direction[7]
execute store result score $bottom count run data get storage builder direction[0]
execute store result score $east count run data get storage builder direction[1]
execute store result score $west count run data get storage builder direction[2]
execute store result score $top count run data get storage builder direction[3]
execute store result score $north count run data get storage builder direction[4]
execute store result score $south count run data get storage builder direction[5]
execute store result score $fill count run data get storage builder direction[6]

execute if score $stairs count matches 0 anchored feet run function builder:direction/cube
execute if score $stairs count matches 1 anchored feet run function builder:direction/stairs

function builder:direction/reset