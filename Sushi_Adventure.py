# Choose Your Own Adventure: SUSHI ADVENTURE
# This is a story-based word game where the player becomes a sushi apprentice
# and creates their own sushi roll through a series of interactive decisions.

# How to play:
# 1. The player will make 4 decisions: rice, filling, topping, and preparation style.
# 2. At the end, their sushi will be visually displayed.

# ------------------------------
# Use ANSI color sequences to format the text, and the final sushi's visual.
# The formatting is reset with additional ANSI sequencing.

# Define the colors for text styling.
colors = {
    "CYAN": "\033[96m",
    "MAGENTA": "\033[95m",
    "ORANGE": "\033[38;5;208m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "RESET": "\033[0m"
}
# Define a bold text style for headers and highlights.
BOLD = "\033[1m"

# ------------------------------
# Define sushi ingredient options and visuals.
# Each ingredient type has a list of names, a list of visual “patterns,”
# and a list of corresponding colors for later visual representation.

# Rice options.
riceNames = ["White Rice", "Brown Rice", "Black Rice"]
ricePatterns = ["ooo", "***", "###"]
riceColors = ["GREEN", "YELLOW", "RED"]

# Filling options.
fillingNames = ["Salmon", "Tuna", "Tempura Shrimp", "Cucumber", "Eel"]
fillingPatterns = ["~~~", "===", "+++", "|||", "---"]
fillingColors = ["ORANGE", "RED", "YELLOW", "GREEN", "MAGENTA"]

# Topping options.
toppingNames = ["Avocado", "Spicy Mayo", "Sesame Seeds", "Eel Sauce", "None"]
toppingPatterns = ["...", "***", "^^^", ":::", ""]
toppingColors = ["GREEN", "RED", "YELLOW", "ORANGE", "RESET"]

# Sushi preparation style options.
prepNames = ["Traditional Roll", "Hand Roll"]
prepShapes = ["round", "cone"]

# ------------------------------
# Initialize game state variables(store player name and choices made during the game).
playerName = ""
riceChoice = 0
fillingChoice = 0
toppingChoice = 0
prepChoice = 0

# Define the header's style.
def displayHeader(title):
    print(f" \n{colors['CYAN']}{BOLD}--- {title} ---{colors['RESET']}\n")

# Define main game function.
def main():
    global playerName, riceChoice, fillingChoice, toppingChoice, prepChoice
    
    # Game introduction.
    displayHeader("WELCOME TO SUSHI ADVENTUR!")
    print("You are a sushi apprentice looking to master your sushi-making.\n"
          "Here, you'll make four key decisions: choosing your rice, fillings, "
          "topping, and style, to create your very own delicious sushi roll.\n"
          "Let's make something delicious together!\n")
    
    # Ask for player’s name.
    playerName = input("What is your chef name? ").strip()
    # If player doesn't type a name, default to "chef".
    if playerName == "":
        playerName = "chef"
    
    print(f"\n{colors['MAGENTA']} Welcome, {playerName}! Let's begin!{colors['RESET']}\n")
    
    # STEP 1: Rice selection.
    displayHeader("STEP 1: Choose Your Rice")
    print()
    
    # Display all rice options using a for loop.
    for i in range(len(riceNames)):
        print(f" [{i+1}] {riceNames[i]}")
    
    # Validate player input using a loop and boolean operators.
    while True:
        choice = input("\nSelect your rice (1, 2, or 3): ").strip()
        if choice.isdigit() and int(choice) >= 1 and int(choice) <= 3:
            riceChoice = int(choice) - 1
            break
        else:
            print("  Please enter 1, 2, or 3.")
    
    print(f"\n{colors['MAGENTA']}You chose {riceNames[riceChoice]}!{colors['RESET']}")
    
    # STEP 2: Filling selection.
    displayHeader("STEP 2: Choose Your Filling")
    print()
    
    for i in range(len(fillingNames)):
        print(f" [{i+1}] {fillingNames[i]}")
    
    while True:
        choice = input("\nSelect your filling (1, 2, 3, 4, or 5): ").strip()
        if choice.isdigit() and int(choice) >= 1 and int(choice) <= 5:
            fillingChoice = int(choice) - 1
            break
        else:
            print("  Please enter a number between 1 and 5.")
    
    print(f"\n{colors['MAGENTA']}You chose {fillingNames[fillingChoice]}!{colors['RESET']}")
    
    # STEP 3: Topping selection.
    displayHeader("STEP 3: Choose Your Topping")
    print()
    
    for i in range(len(toppingNames)):
        print(f" [{i+1}] {toppingNames[i]}")

    while True:
        choice = input("\nSelect your topping (1, 2, 3, 4, or 5): ").strip()
        if choice.isdigit() and int(choice) >= 1 and int(choice) <= 5:
            toppingChoice = int(choice) - 1
            break
        else:
            print("  Please enter a number between 1 and 5.")
    
    # Display result with condition.
    if toppingChoice == 4:
        print(f"\n{colors['MAGENTA']}Classic choice, keeping it simple!{colors['RESET']}")
    else:
        print(f"\n{colors['MAGENTA']}You chose {toppingNames[toppingChoice]}!{colors['RESET']}")
    
    # STEP 4: Preparation style selection.
    displayHeader("STEP 4: Choose Your Style")
    print()
    
    # Use for loop to display preparation options
    for i in range(len(prepNames)):
        print(f" [{i+1}] {prepNames[i]}")
    
    while True:
        choice = input("\nSelect your style (1 or 2): ").strip()
        if choice.isdigit() and int(choice) >= 1 and int(choice) <= 2:
            prepChoice = int(choice) - 1
            break
        else:
            print("  Please enter 1 or 2.")
    
    print(f"\n{colors['MAGENTA']}You chose {prepNames[prepChoice]}!{colors['RESET']}")
    
    # Creating the sushi.
    print(f"\n{colors['GREEN']}{BOLD}...Creating your SUSHI...{colors['RESET']}\n")
    
    # Display ingredient summary.
    print(f"\n{colors['CYAN']}{BOLD}--- YOUR INGREDIENTS ---{colors['RESET']}\n")
    
    # Print rice information.
    riceText = f" Rice: {riceNames[riceChoice]} - Pattern: {ricePatterns[riceChoice]}"
    print(f"{colors[riceColors[riceChoice]]}{riceText}{colors['RESET']}")
    
    # Print filling information.
    fillingText = f" Filling: {fillingNames[fillingChoice]} - Pattern: {fillingPatterns[fillingChoice]}"
    print(f"{colors[fillingColors[fillingChoice]]}{fillingText}{colors['RESET']}")
    
    # Print topping information only if not "None".
    if toppingChoice != 4:
        toppingText = f" Topping: {toppingNames[toppingChoice]} - Pattern: {toppingPatterns[toppingChoice]}"
        print(f"{colors[toppingColors[toppingChoice]]}{toppingText}{colors['RESET']}")
    else:
        print(" Topping: None")
    
    print(f" {colors['MAGENTA']}Style: {prepNames[prepChoice]} - {prepShapes[prepChoice]} shape{colors['RESET']}")

    # ------------------------------
    # Sushi visual generation.
    # Create a visual using ASCII art and colored ingredient patterns.
    print("\n" + "-"*60)
    print(f"                {colors['CYAN']}{BOLD}YOUR SUSHI!{colors['RESET']}")
    print("="*60 + "\n")
    
    if prepShapes[prepChoice] == "round":
        # Traditional round roll.
        print("             _________________")
        print("            /                 \\")
        
        # Create colored rice line.
        riceLine = f"           |  {ricePatterns[riceChoice]}  {ricePatterns[riceChoice]}  {ricePatterns[riceChoice]}  |"
        print(f"{colors[riceColors[riceChoice]]}{riceLine}{colors['RESET']}" + "  <- Rice")
        
        # Create colored filling line.
        fillingLine = f"           |  {fillingPatterns[fillingChoice]}  {fillingPatterns[fillingChoice]}  {fillingPatterns[fillingChoice]}  |"
        print(f"{colors[fillingColors[fillingChoice]]}{fillingLine}{colors['RESET']}" + f"  <- {fillingNames[fillingChoice]}")
        
        # Bottom rice layer.
        print(f"{colors[riceColors[riceChoice]]}{riceLine}{colors['RESET']}")
        
        # Add topping if present.
        if toppingPatterns[toppingChoice] != "":
            toppingLine = f"           |  {toppingPatterns[toppingChoice]}  {toppingPatterns[toppingChoice]}  {toppingPatterns[toppingChoice]}  |"
            print(f"{colors[toppingColors[toppingChoice]]}{toppingLine}{colors['RESET']}" + f"  <- {toppingNames[toppingChoice]}")
        
        print("            \\_________________/")
        
    else:
        # Hand roll (cone shape).
        print("                  /|")
        
        fillingLine = f"                 / | {fillingPatterns[fillingChoice]}"
        print(f"{colors[fillingColors[fillingChoice]]}{fillingLine}{colors['RESET']}" + f"  <- {fillingNames[fillingChoice]}")
        
        if toppingPatterns[toppingChoice] != "":
            toppingLine = f"                /  | {toppingPatterns[toppingChoice]}"
            print(f"{colors[toppingColors[toppingChoice]]}{toppingLine}{colors['RESET']}" + f"  <- {toppingNames[toppingChoice]}")
        
        # Use for loop to simulate rice layering.
        for i in range(2):
            spaces = " " * (15-i)
            riceLine = f"{spaces}/ {' ' * (i+2)}| {ricePatterns[riceChoice]}"
            if i == 0:
                print(f"{colors[riceColors[riceChoice]]}{riceLine}{colors['RESET']}" + "  <- Rice")
            else:
                print(f"{colors[riceColors[riceChoice]]}{riceLine}{colors['RESET']}")
        
        print("             /_____|")
        print("              Cone!")
    
    # ------------------------------
    # Ending message.
    print(f"\n {colors['CYAN']}{BOLD}Congratulations, Chef {playerName}!{colors['RESET']}")
    print(f"\n {colors['CYAN']}{BOLD}Enjoy Your Sushi!{colors['RESET']}")
    print("\n" + "-"*60 + "\n")
    print("\n Thank you for playing SUSHI ADVENTURE! \n")

# ------------------------------
# Program execution.
# This ensures the game only runs when the script is executed directly.
if __name__ == "__main__":
    main()