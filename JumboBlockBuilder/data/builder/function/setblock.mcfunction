$setblock ~ ~ ~ $(id)
execute if block ~ ~ ~ #builder:falling_block if block ~ ~-1 ~ #builder:air run setblock ~ ~-1 ~ barrier
execute if block ~ ~ ~ structure_void if block ~ ~1 ~ #builder:falling_block run setblock ~ ~ ~ barrier