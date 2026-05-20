scoreboard objectives add count dummy

scoreboard players set $counter count 0
scoreboard players set $offset count 0
scoreboard players set $width count 16
scoreboard players set $height count 16

scoreboard players operation $size count = $width count
scoreboard players operation $size count *= $height count