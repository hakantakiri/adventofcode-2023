# 🎄 Solutions Advent of Code 2023 🎄

> https://adventofcode.com/2023

# Relevant notes

- Day 5 part 2 required to process chunks of ranges of numbers instead of individual numbers. Drawing intersections of ranges was very useful.
- Day 10 part 2 required a way to determinate sides and 180 degrees turn edges, can be improved based on day 18 solution with shoelace theorem and its adaptation.
- Day 12 part 2 required specific recursion and DP. Learned about @functools and lru_cache, but implemented my own "cache" using a regular dictionary.
- Day 18, learned about shoelace theorem and adapted to work for cubes instead of coordinates, this adaptation turned out to be almost exactly as another theorem I learned latter called Pick's theorem which uses vertices, my adaptation uses sides.

### 🛠️ Needs improvement

- Day 19 🔴 (WIP part 2: Process chunks instead of numbers)
- Day 23 🟢 (Can improve: p_1 collapse to nodes, p_2 assign weights to nodes)
- Day 24 🔴 (left part 2)
- Day 25 🔴 (left part 2, needs to solve all other challenges)
