from puzzle_generator import create

# Generate a puzzle with base16 encoding to reduce output size
puzzle = create(encoding="base16")
print(puzzle)
