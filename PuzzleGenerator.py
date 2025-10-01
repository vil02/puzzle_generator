import random

def generate_puzzle():
    # Hidden number between 1 and 100
    hidden_number = random.randint(1, 100)
    
    # Clues for the user
    clues = [
        f"The number is {'even' if hidden_number % 2 == 0 else 'odd'}.",
        f"The number is {'divisible by 3' if hidden_number % 3 == 0 else 'not divisible by 3'}.",
        f"The number is {'greater than 50' if hidden_number > 50 else '50 or less'}.",
        f"The sum of its digits is {sum(int(digit) for digit in str(hidden_number))}."
    ]
    
    # Shuffle clues for randomness
    random.shuffle(clues)
    
    return hidden_number, clues

def play_puzzle():
    hidden_number, clues = generate_puzzle()
    print("Welcome to the Number Puzzle!")
    print("Here are your clues:")
    for clue in clues:
        print("-", clue)
    
    attempts = 0
    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1
            if guess == hidden_number:
                print(f"Congratulations! You found the number in {attempts} attempts.")
                break
            elif guess < hidden_number:
                print("Too low!")
            else:
                print("Too high!")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    play_puzzle()
