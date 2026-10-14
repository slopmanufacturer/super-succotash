#
# Wumbo Jumbo Casino Game made by slopmanufacturer
# Version: 1.0.0
#


import random, time, sys, os

try:
    import termios, tty, select
except ImportError:
    termios = None
    import msvcrt


#color
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
GOLD = "\033[38;5;220m"
RESET = "\033[0m"

#skipping the intro. 
class SkipIntro(Exception):
    pass #also FUH OFF if u do skip the intro..

skippable = False

def f_pressed():
    if not (skippable and sys.stdin.isatty()):
        return False
    if termios is None:
        pressed = False
        while msvcrt.kbhit():
            pressed = msvcrt.getwch().lower() == "f" or pressed
        return pressed
    if select.select([sys.stdin], [], [], 0)[0]:
        return b"f" in os.read(sys.stdin.fileno(), 1024).lower()
    return False

#introduction
def slow_print(*args, delay=0.05, sep=" ", end="\n"):
    text = sep.join(str(a) for a in args) + end
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
        if f_pressed():
            raise SkipIntro

def intro():
    slow_print("You wake up in an alley. No idea how you got here.")
    slow_print("The city is loud, but it sounds far away.")
    slow_print("There's a narrow passage ahead. It's warm in there, and it smells sweet.")
    slow_print("At the end of it is a light. Just one. It's hard to look at.")
    slow_print("You walk towards it. Your heart is pounding, and then\n")

    time.sleep(0.4)
    slow_print(".\n", delay=0.1)
    time.sleep(0.2)

    slow_print(f"A {GOLD}casino{RESET}?\n", delay=0.1)


    slow_print(f"You walk in front of the entrance of the {GOLD}Casino{RESET}, taking note of the lively atmosphere inside.")
    slow_print(f"You look at the entrance, specifically the name '{GOLD}Wumbo Jumbo{RESET}'.")
    slow_print("You take a slow yet steady breath, wondering if you should enter...")

def run_intro():
    global skippable
    if not sys.stdin.isatty():
        intro()
        return
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd) if termios else None
    if old:
        tty.setcbreak(fd)
    skippable = True
    try:
        intro()
    except SkipIntro:
        print(RESET + "\n")
    finally:
        skippable = False
        if old:
            termios.tcsetattr(fd, termios.TCSAFLUSH, old)
        elif termios is None:
            while msvcrt.kbhit():
                msvcrt.getwch()

run_intro()

#THE ACTUAL GAME STAARTS HERE
UNICODE_BOX = {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║", "ml": "╠", "mr": "╣"}
ASCII_BOX = {"tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "-", "v": "|", "ml": "+", "mr": "+"}

def draw_menu(): #had to get AI to help me with this, holy shit. deepseek ur so goated 
    enc = (sys.stdout.encoding or "").lower()
    box = UNICODE_BOX if "utf" in enc or enc == "cp65001" else ASCII_BOX
    w = 44
    print(f"{YELLOW}{box['tl']}{box['h'] * w}{box['tr']}{RESET}")
    title = "WUMBO JUMBO"
    left = (w - len(title)) // 2
    print(f"{box['v']}{' ' * left}{title}{' ' * (w - left - len(title))}{box['v']}")
    print(f"{box['ml']}{box['h'] * w}{box['mr']}")
    for label in ("1. Enter the Casino", "2. Stall time", "3. Walk away"):
        pad = w - 1 - len(label)
        label = label.replace("Casino", f"{GOLD}Casino{RESET}")
        print(f"{box['v']} {label}{' ' * pad}{box['v']}")
    print(f"{YELLOW}{box['bl']}{box['h'] * w}{box['br']}{RESET}")
    print()

draw_menu()

stall_count = 0

while True:
    try:
        game_starting = int(input("> "))
        if game_starting == 1:
            break
        if game_starting == 2:
            slow_print("You decide to stall a bit...")
            slow_print(".")
            slow_print("..")
            slow_print("...")
            stall_count += 1

            if stall_count >= 3:
                slow_print("You've been stalling for too long. Are you gonna enter the casino or what?")
                slow_print("You looked at your shoes... What a pity... Just choose already..")
                draw_menu()
            continue

        if game_starting == 3:
            slow_print("See you around, pal...")
            slow_print("NOO! COME BACK PLZ!")
            sys.exit()
        if game_starting == 4:
            slow_print("Silly little cheater...")
            slow_print("+100 coins!") # adds coins for user finding easter egg
            #Coin += 100
            continue
    except ValueError:
        pass
    slow_print("Psst... Choose a valid option, pal.")

#TODO LATER
#Will add coin system and more options later
#Eat a mcflurry
#adding a settings menu, as well as an ascii text later
#fix the stall issue