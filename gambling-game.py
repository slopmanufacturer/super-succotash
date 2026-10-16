#
# Wumbo Jumbo Casino Game made by slopmanufacturer
# Version: 1.0.1
#


import random, time, sys, os, re

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
ANSI = re.compile(r"(\x1b\[[0-9;]*m)")
MENU_DELAY = 0.015

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
    for chunk in ANSI.split(text):
        if ANSI.fullmatch(chunk):
            sys.stdout.write(chunk)
            sys.stdout.flush()
            continue
        for char in chunk:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
            if f_pressed():
                raise SkipIntro

def intro():
    slow_print("You wake up in an alley. No idea how you got here.")
    slow_print("The city is loud, but it sounds far away.")
    slow_print("There's a narrow passage ahead. It's warm in there, and it smells sweet.")
    slow_print(f"At the end of it is a {GOLD}light{RESET}. Just one. It's hard to look at.")
    slow_print("You walk towards it. Your heart is pounding, and then\n")

    time.sleep(0.4)
    slow_print(".\n", delay=0.1)
    time.sleep(0.2)

    slow_print(f"A {GOLD}casino{RESET}?\n", delay=0.1)


    slow_print(f"You walk in front of the entrance of the {GOLD}Casino{RESET}, taking note of the lively atmosphere inside.")
    slow_print(f"You look at the entrance, specifically the name '{GOLD}Wumbo Jumbo{RESET}'.")
    slow_print("You take a slow yet steady breath, wondering if you should enter...\n")
    time.sleep(1.2)

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



UNICODE_BOX = {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║", "ml": "╠", "mr": "╣"}
ASCII_BOX = {"tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "-", "v": "|", "ml": "+", "mr": "+"}

def reveal(text, n):
    out = ""
    count = 0
    for chunk in ANSI.split(text):
        if ANSI.fullmatch(chunk):
            out += chunk
            continue
        for char in chunk:
            if count >= n:
                return out + RESET
            out += char
            count += 1
    return out

def draw_menu(title="WUMBO JUMBO", options=("1. Enter the Casino", "2. Stall time", "3. Settings", "4. Walk away")): #had to get AI to help me with this, holy shit. deepseek ur so goated 
    enc = (sys.stdout.encoding or "").lower()
    box = UNICODE_BOX if "utf" in enc or enc == "cp65001" else ASCII_BOX
    w = 44
    left = (w - len(title)) // 2
    rows = [f"{YELLOW}{box['tl']}{box['h'] * w}{box['tr']}{RESET}"]
    rows.append(f"{box['v']}{' ' * left}{title}{' ' * (w - left - len(title))}{box['v']}")
    rows.append(f"{box['ml']}{box['h'] * w}{box['mr']}")
    for label in options:
        pad = w - 1 - len(label)
        label = label.replace("Casino", f"{GOLD}Casino{RESET}")
        rows.append(f"{box['v']} {label}{' ' * pad}{box['v']}")
    rows.append(f"{YELLOW}{box['bl']}{box['h'] * w}{box['br']}{RESET}")

    if not sys.stdout.isatty():
        print("\n".join(rows))
        print()
        return

    walls = [f"{box['v']}{' ' * w}{box['v']}", f"{box['ml']}{' ' * w}{box['mr']}"]
    walls += [f"{box['v']}{' ' * w}{box['v']}" for _ in options]
    interior = rows[1:-1]
    empty = [""] * len(interior)

    def paint(frame, first):
        if not first:
            sys.stdout.write(f"\033[{len(rows)}A")
        for line in frame:
            sys.stdout.write("\033[2K" + line + "\n")
        sys.stdout.flush()
        time.sleep(MENU_DELAY)

    first = True
    for k in range(2, w + 3, 2):
        paint([reveal(rows[0], k)] + empty + [""], first)
        first = False
    for r in range(1, len(interior) + 1):
        paint([rows[0]] + [walls[i] if i < r else "" for i in range(len(interior))] + [""], first)
        first = False
    for k in range(2, w + 3, 2):
        paint([rows[0]] + walls + [reveal(rows[-1], k)], first)
        first = False
    for k in range(2, w + 3, 2):
        paint([rows[0]] + [reveal(row, k) for row in interior] + [rows[-1]], first)
        first = False
    paint(rows, first)
    print()


#settings menu

def settings_menu():
    print("\n")
    while True:
        draw_menu("SETTINGS", ("1. Head back", "2. Nothing here yet... Still cooking :/"))
        pick = input("> ")
        if pick == "1":
            draw_menu()
            return
        if pick == "2":
            slow_print("\nI just told you nothing was here...\n")
            continue



#game starts here

run_intro()
draw_menu()

stall_count = 0
running = True
gamble_game = True #for when user piocks 1

while running:
    try:
        game_starting = int(input("> "))
        if game_starting == 1:
            while gamble_game:
                draw_menu("Choose your posion", ("1. Nothing yet...", "2. Go Back", "3. Go Back (But Cooler)"))
                gamble_pick = input("> ")
                if gamble_pick == "1":
                    slow_print("\nNothing yet... Come back later!\n")
                    continue
                if gamble_pick == "2":
                    slow_print("\nGoing back (less cooler)...\n")
                    draw_menu()
                    break
                if gamble_pick == "3":
                    slow_print("\nGoing back (but cooler)...\n")
                    draw_menu()
                    break
            continue

        if game_starting == 2:
            stall_count += 1
            if stall_count == 1:
                slow_print("\nYou decide to stall a bit...")
                slow_print(".", delay=0.4)
                slow_print("..", delay=0.4)
                slow_print("...\n", delay=0.4)
                draw_menu()
            if stall_count == 2:
                slow_print("\nYou stalled again... You seem to be bored.")
                slow_print("You took a deep sigh...\n")
                slow_print(".", delay=0.4)
                slow_print("..", delay=0.4)
                slow_print("...\n", delay=0.4)
                draw_menu()
            if stall_count == 3:
                slow_print("\nYou've been stalling for too long. Are you gonna enter the casino or what?")
                slow_print("You looked at your shoes... What a pity... Just choose already..\n")
                slow_print(".", delay=0.4)
                slow_print("..", delay=0.4)
                slow_print("...\n", delay=0.4)
                draw_menu()
            if stall_count > 3:
                slow_print("\nYou've decided to just walk away...")
                slow_print("A small mockery echos in your head: 'Idiot..'\n")
                slow_print(f"{RED}Game Over!{RESET}\n")
                sys.exit()


            continue

        if game_starting == 3:
            settings_menu()
            continue
        if game_starting == 4:
            slow_print("\nYou decided to walk away...")
            slow_print(f"You ended the {RED}game.{RESET}\n")
            running = False
            continue
        if game_starting == 5:
            slow_print("\nSilly little cheater...")
            slow_print(f"+100 {YELLOW}coins{RESET}!\n") # adds coins for user finding easter egg
            #Coin += 100
            continue
    except ValueError:
        pass
    slow_print("\nPsst...", delay=0.07)
    slow_print(f"Choose a valid option. {GREEN}Oddball{RESET}..\n", delay=0.1)
    time.sleep(1)
    draw_menu()

#TODO
#Will add coin system and more options later
#an ascii text later
#add actual data that stays even after program closes by using json or something 67
#will add more setting options such as text speed, and color themes!!!!



#COMPLETED
"""
Settings menu
Fixed the stall issue
ate a mcflurry frfrfr
Made it so that if you played a game, your stall count resets
"""
