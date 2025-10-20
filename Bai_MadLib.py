# ---------------------------------
# Mad Libs: "One More Game"
# This is a word-game that takes different kinds of words to enter into a story.

# How to use this program: 
# 1. Follow the prompts and type your own words (nouns, adjectives, verbs, etc.).
# 2. At the end, your custom story will be printed! 
# ---------------------------------

# Use ANSI color sequences to format the welcome text, title, and Mad Libs words. 
# The formatting is reset with additional ANSI sequencing.
# Set the color and style.
RESET = "\033[0m"
BOLD = "\033[1m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

# Provide a gap before printing.
print(" \n") 

# Start with a welcome message and game instructions.
print(f"{MAGENTA}{BOLD}--- Welcome to Mad Libs: One More Game! ---\n{RESET}")
print(f"{CYAN}Fill in the blanks with your own words and create a funny story!\n{RESET}")

# User inputs
# Each input() asks the player for a word, which it stores in a variable.
familyMember = input("Enter a noun (e.g. mom, dad): ")
challengeAdjective = input("Provide an adjective (e.g. tough, tricky): ")
excuseAdjective = input("Give another adjective (e.g. funny, creative): ")
bodyPart = input("Enter a part of the body: ")
actionVerb = input("Give a verb (e.g. defeat): ")
placeName = input("Enter a place: ")
celebrityName = input("Provide a celebrity name: ")
animalType = input("Give an animal: ")
numberMinutes = input("Give a number: ")
levelAdjective = input("Enter another adjective (e.g. final): ")
lastName = input("Enter a last name: ")
subjectName = input("Enter a school subject: ")
foodType = input("Name a type of food: ")
personName = input("Enter the name of a person in the room: ")
grandpaName = input("Give a male first name: ")
weatherGerund = input("Provide a verb that ends in -ing: ")
exclamationWord = input("Enter an exclamation: ")

# Build & print Mad Libs story
# Using string manipulation here to combine the user's words with the story text.
MadLibs = f"""
{MAGENTA}{BOLD}--- YOUR MAD LIBS STORY ---{RESET}

Convincing your {CYAN}{familyMember}{RESET} to let you stay up past your bedtime to play video games 
can be {MAGENTA}{challengeAdjective}{RESET}, but it's not impossible. Here are some {CYAN}{excuseAdjective}{RESET} excuses 
to use when you need one last game.

1. My {MAGENTA}{bodyPart}{RESET} hurts. The only way it will feel better is if I {CYAN}{actionVerb}{RESET} these 
cyborgs and save (the) {MAGENTA}{placeName}{RESET}.

2. {CYAN}{celebrityName}{RESET} also plays {MAGENTA}{animalType}{RESET} Hut so if you want me to be successful in life,
please give me {CYAN}{numberMinutes}{RESET} minutes to finish the {MAGENTA}{levelAdjective}{RESET} level.

3. Mrs. {CYAN}{lastName}{RESET}, my {MAGENTA}{subjectName}{RESET} teacher, said that video games make you smart.
She plays {CYAN}{foodType}{RESET} Assault, so she knows.

4. There's nothing else to do! {MAGENTA}{personName}{RESET} isn't here to play with, Grandpa {CYAN}{grandpaName}{RESET} went 
to bed, and it's {MAGENTA}{weatherGerund}{RESET} outside. 

5. {CYAN}{exclamationWord}{RESET}! If you let me play Night Woods, I'll clean my room. Please think about it. 
"""

print(MadLibs)