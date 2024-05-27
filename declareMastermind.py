from enum import Enum,auto
import random, os
from typing import Optional, Final, TypeAlias, ClassVar
import copy
from dataclasses import dataclass

#Make str that won't be changed immutable using Final (Rules & Menu)
welcomeMessage: Final[str] = """\nWelcome to...
   _____                   __                       .__            .___
  /     \ _____    _______/  |_  ___________  _____ |__| ____    __| _/
 /  \ /  \\__  \  /  ___/\   __\/ __ \_  __ \/     \|  |/    \  / __ | 
/    Y    \/ __ \_\___ \  |  | \  ___/|  | \/  Y Y  \  |   |  \/ /_/ | 
\____|__  (____  /____  > |__|  \___  >__|  |__|_|  /__|___|  /\____ | 
        \/     \/     \/            \/            \/        \/      \/ 
        """
        
def clearScreen():
    os.system('cls')

rules : Final[str] = """
1. The game starts with the codemaker creating a 4 color code out of a sequence of 8 
   colours: red, green, blue, yellow, orange, purple, indigo and violet
2. The codebreaker then attempts a series of guesses to crack the code
3. After each guess feedback is given next to the guess where:
   Black means they have a correct colour in the correct position
   White means they have a correct colour in the incorrect position
4. The codebreaker gets 10 attempts to guess the code
5. If the codebreaker correctly guesses the code they win
6. If after 10 guesses the codebreaker hasn't guessed the code the codemaker wins
"""
# Available Colours for codemaking/breaking - store as a tuple so it is immutable
Colours  = ("red", "green", "blue", "yellow", "orange", "purple", "indigo", "violet")
colourLetters = ("r","g","b","y","o","p","i","v")


# Gamemodes 
class GameMode(Enum):
    PVP = 1
    PVCPU = 2
    CAMPAIGN = 3
    QUIT = 4
    

    @staticmethod
    def parse (s:str) -> Optional['GameMode']:
        match s:
            case "1" : return GameMode.PVP 
            case "2" : return GameMode.PVCPU
            case "3" : return GameMode.CAMPAIGN
            case "4" : return GameMode.QUIT
            case _ : return None 

# I've defined game state this way as there is no associated behaviour with gamestates
# meaning I don't have to make a Gamestate class with it's own functions
# instead I can just use a match case satement for each gamestate
@dataclass(eq=True, frozen=True)
class CBWin:
    def __str__(self):
        return "Codebreaker Wins!"
@dataclass(eq=True, frozen=True)
class CMWins:
    def __str__(self):
        return "Codemaker Wins!"
@dataclass(eq=True, frozen=True)
class NextTurn:
    def __str__(self):
        return "Next Turn"
GameState = TypeAlias = CBWin | CMWins | NextTurn

class Colour(Enum):
    red = "\033[1;31;40mR\033[0;37;40m"
    green = "\033[1;32;40mG\033[0;37;40m"
    blue = "\033[1;34;40mB\033[0;37;40m"
    yellow = "\033[1;33;40mY\033[0;37;40m"
    orange = "\033[38;2;255;165;0mO\033[0;37;40m"
    purple = "\033[38;2;128;0;128mP\033[0;37;40m"
    indigo = "\033[38;2;75;0;130mI\033[0;37;40m"
    violet = "\033[38;2;127;0;255mV\033[0;37;40m"

    @staticmethod
    def parse(s:str) -> Optional['Colour']:
        letter_to_color = {
            'r': Colour.red, 'g': Colour.green, 'b': Colour.blue, 'y': Colour.yellow,
            'o': Colour.orange, 'p': Colour.purple, 'i': Colour.indigo, 'v': Colour.violet
        }

        try:
            conv = letter_to_color[s]
        except KeyError:
            return None
        return conv
    
    def __str__(self) -> str:
        return self.value

class Pattern:
    size : ClassVar[int] = 4

    def __init__(self,first,second,third,fourth):
        self.first = first 
        self.second = second 
        self.third = third
        self.fourth = fourth
    
    @staticmethod
    # This previously took s as a list of strings s e.g. rbgy
    def parse(s:str) -> Optional['Pattern']:
        if len(s)!=Pattern.size:
            return None 
        
        # Use colour parsing function to validate colours in pattern
        # Collect validated colours in a list of Colour Objetcs 
        colours = []
        # rgby -> Colour.red, .... 
        for l in s:
            parsed = Colour.parse(l)
            if parsed is None:
                return None
            colours.append(parsed)
                
        
        #return a new Pattern object consisting of 4 Colour objects 
        return Pattern(colours[0],colours[1],colours[2],colours[3])
        
    def __str__(self) -> str:
        return f"{str(self.first)}{str(self.second)}{str(self.third)}{str(self.fourth)}"
    
    def __eq__(self, value: 'Pattern') -> bool:
        if not isinstance(value,Pattern):
            return False
        return(self.first,self.second,self.third,self.fourth) == (value.first,value.second,value.third,value.fourth)

class Feedback(Enum):
    Black = "Black"
    White = "White"
    Null = ""
    
    def __str__(self):
        return self.name
    
    # Test Github
    @staticmethod
    def giveFeedback(code: Pattern,guess:Pattern) -> list['Feedback']:
        feedback = []
        codeColours = [code.first,code.second,code.third,code.fourth]
        guessColours = [guess.first,guess.second,guess.third,guess.fourth]

        for i in range(4):
            if guessColours[i] == codeColours[i]:
                feedback.append(Feedback.Black)
                codeColours[i] = guessColours[i] = None
       
        for i in range(4):
            if guessColours[i] is not None and guessColours[i] in codeColours:
                feedback.append(Feedback.White)
                codeColours[codeColours.index(guessColours[i])] = None
        
        # Pad the list with Null feedback untill we reach the desired length of 4
        while len(feedback) < 4:
            feedback.append(Feedback.Null)
        
        return feedback
    


# Predefined Campaign Codes as Pattern Objects
CampaignCodes = [Pattern(Colour.red,Colour.green,Colour.blue,Colour.yellow),
                Pattern(Colour.orange,Colour.purple,Colour.blue,Colour.violet),
                Pattern(Colour.blue,Colour.indigo,Colour.purple,Colour.green),
                Pattern(Colour.purple,Colour.indigo,Colour.green,Colour.yellow)]

# Fuction to output gameboard as game progresses
# "get it to generate the string and return it, then print out separately" -E.C.
def Generateboard(feedback : list[Feedback], guess:Pattern) -> str:
    displayFeedback =[]
    for f in feedback: 
        displayFeedback.append(str(f))
    board = ""
    board += "Current Board:\n"
    board += "-" * 100
    board += "\n"
    board += f" Guess: {guess} | Feedback: {displayFeedback}\n"
    board += "-" * 100
    return board

def displayBoard(board) -> str:
    print("\n" + board)


def getUsrInput() -> Pattern:
    print("\n- Available colours to guess from are",Colours)
    usrInp = input("\n- Please enter a sequence of the first letter of each colour in (e.g. rgby): ").lower().replace(" ", "")
    validInp = Pattern.parse(usrInp)
    if validInp is None:
        print("\n! Invalid input! Please enter a 4 letter input of the first letter of the available colours","\n",colourLetters)
        return getUsrInput()
    
    return validInp 

def guessing(code: Pattern)-> bool:
    guesses = 0
    while guesses < 10:
        guess = getUsrInput()
        if guess == code:
            return True
         
        displayBoard(Generateboard(Feedback.giveFeedback(code,guess),guess))
        guesses +=1
        print("\n- Number of remaining guesses: ", 10-guesses)
    else:    
        return False  
    
# TakeTurn should replace guessing - More maintainable code (allows for diff no. guesses)
# Recursive call at NextTurn.__str__ or return NextTurn GameState which decrements turnsleft
def takeTurn(code : Pattern, turnsLeft:int, board) -> GameState:   
   while turnsLeft > 0:
    guess = getUsrInput() 
    match guess:
        case guess if guess == code:
            return CBWin.__str__
        case guess if guess != code:
            Generateboard(Feedback.giveFeedback(code,guess),guess)
            NextTurn.__str__
    turnsLeft -= 1
    return CMWins.__str__

def PVP():
    # Set up pattern by codemaker
    # Set up mastermind grid -> Need to compelete Gen/Display Board
    # Repeatedly (descending from 10)
    #      call take_turn_cb : Pattern X TurnsLeft X MasterMindGrid -> PlayState
    #      on result from call
    #      case WinCB
    #           print out message
    #           return from procedure
    #      case WinCM
    #           print out message
    #           return from procedure
    #      case Continue
    #           continue to next "iteration"

    print("! Codebreaker please look away while the codemaker sets a code !")
    code = getUsrInput()
    clearScreen()
    print("- The code has been set! Good luck guessing, Codebreaker!")
    Play = guessing(code)

    if Play == True:
        print("\n! Congratulations, Codebreaker, YOU WIN !")

    elif Play == False:
        print("\n! You're out of guesses, Codebreaker... CODEMAKER WINS !")

def PVCPU():
    code = random.sample(colourLetters, 4)
    print("- The code being generated is...", code)
    code = Pattern.parse(code)
    print("- The code has been generated succesfully!")
    Play = guessing(code)

    if Play == True:
        print("\n! Congratulations, Codebreaker, YOU WIN !")

    elif Play == False:
        print("\n! You're out of guesses, Codebreaker... CPU WINS !")

def Campaign():
    for i, Pattern in enumerate(CampaignCodes):
        print(f"\nLevel {i + 1}:")
        code = CampaignCodes[i]
        Play = guessing(code)
        if not Play:
            break
        print("\n! Well done, Codebreaker, You cracked the code! Moving on to the next level... !")
    print("\n! Congratulations! You completed the campaign !")


# Main is very long - take logic away from main and put into funcs 
def main():
    ruleFlag = False
    while True:
        print(welcomeMessage)

        if ruleFlag == False:
            print(rules)
            ruleFlag = not ruleFlag 

        for game in GameMode:
            print(game.value, "-", game.name)
        # Consider adding a getMenuOption Function - "Sepearte display logic from game logic"
        menuOption = (input("\nPlease enter a Menu Option: "))
        # USE MATCH CASE INSTEAD OF IFs  
        selection = GameMode.parse(menuOption)
        match selection:
            case GameMode.PVP :
                clearScreen()
                print("*** Player vs Player ***\n")
                PVP()
            case GameMode.PVCPU:
                clearScreen()
                print("*** Plaver Vs CPU ***\n")
                PVCPU()
            case GameMode.CAMPAIGN:
                clearScreen()
                print("*** Campaign Mode ***\n")
                Campaign()
            case GameMode.QUIT:
                break 
            case None : 
                print("Invalid Menu Option (Please select 1-4)")
                continue


if __name__ == "__main__":
    main()