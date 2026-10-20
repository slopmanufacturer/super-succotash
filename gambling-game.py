#
# Wumbo Jumbo Casino Game made by slopmanufacturer
# Version: 1.0.1
#


import random, time, sys, os, re, threading

try:
    import termios, tty, select
except ImportError:
    termios = None
    import msvcrt


#colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"
GOLD = "\033[38;5;220m"
ORANGE = "\033[38;5;208m"
PINK = "\033[38;5;213m"
PURPLE = "\033[38;5;135m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
ANSI = re.compile(r"(\x1b\[[0-9;]*m)")
MENU_DELAY = 0.015
PROMPT = f"{CYAN}> {RESET}"
YOU = re.compile(r"\b([Yy]ou(?:'[a-z]+|r(?:s(?:elf|elves)?|self|selves)?)?)\b")

def red_you(text):
    return YOU.sub(lambda m: f"{RED}{m.group(1)}{RESET}", text)

stall_count = 0
running = True
gamble_game = True #for when user piocks 1
coin = 100
idle_time = 10
text_speed = 0.06

#skipping the intro. 
class SkipIntro(Exception):
    pass #also FUH OFF if u do skip the intro..

skippable = False

def keys_pressed():
    if not (skippable and sys.stdin.isatty()):
        return ""
    if termios is None:
        keys = ""
        while msvcrt.kbhit():
            keys += msvcrt.getwch().lower()
        return keys
    if select.select([sys.stdin], [], [], 0)[0]:
        return os.read(sys.stdin.fileno(), 1024).decode(errors="ignore").lower()
    return ""

#introduction
def slow_print(*args, text_speed=None, sep=" ", end="\n"):
    if text_speed is None:
        text_speed = globals()["text_speed"]
    text = red_you(sep.join(str(a) for a in args) + end)
    skipping = False
    for chunk in ANSI.split(text):
        if ANSI.fullmatch(chunk):
            sys.stdout.write(chunk)
            sys.stdout.flush()
            continue
        for char in chunk:
            sys.stdout.write(char)
            sys.stdout.flush()
            if skipping:
                continue
            time.sleep(text_speed)
            keys = keys_pressed()
            if "f" in keys:
                raise SkipIntro
            if "g" in keys:
                skipping = True


def start_skip():
    global skippable
    if not sys.stdin.isatty():
        return None
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd) if termios else None
    if old:
        tty.setcbreak(fd)
    skippable = True
    return fd, old


def stop_skip(state):
    global skippable
    skippable = False
    if state is None:
        return
    fd, old = state
    if old:
        termios.tcsetattr(fd, termios.TCSAFLUSH, old)
    elif termios is None:
        while msvcrt.kbhit():
            msvcrt.getwch()


def game_start():
    print("\033[2J\033[H", end="") 
    state = start_skip()
    skipped = False
    try:
        slow_print(f"Welcome to {GOLD}{BOLD}Wumbo Jumbo{RESET}!")
        slow_print(f"A {CYAN}story-driven{RESET} and {MAGENTA}decision-based{RESET} game that will leave you questioning your choices!")
        slow_print(f"You will understand and learn the game as you play.")
        slow_print(f"{PINK}Press 'F' to skip, 'G' to speed up{RESET} the dialogue.")
        slow_print(f"{DIM}Though I recommend you {DIM}reading through the whole thing...{RESET}")
        slow_print(f"{CYAN}Are you ready to begin?{RESET}\n")
    except SkipIntro:
        skipped = True
        print(RESET)
    finally:
        stop_skip(state)
    if not skipped:
        input(f"{CYAN}Press Enter to continue...{RESET}\n")
    print("\033[2J\033[H", end="") 

def intro():
    slow_print("You wake up in an alley. No idea how you got here.")
    slow_print("The city is loud, but it sounds far away.")
    slow_print("There's a narrow passage ahead. It's warm in there, and it smells sweet.")
    slow_print(f"At the end of it is a {GOLD}light{RESET}. Just one. It's hard to look at.")
    slow_print("You walk towards it. Your heart is pounding, and then\n")

    time.sleep(0.4)
    slow_print(".\n", text_speed=0.1)
    time.sleep(0.2)

    slow_print(f"A {GOLD}casino{RESET}?\n", text_speed=0.1)


    slow_print(f"You walk in front of the entrance of the {GOLD}Casino{RESET}, taking note of the lively atmosphere inside.")
    slow_print(f"You look at the entrance, specifically the name...\n")

    slow_print(f"{GOLD}Wumbo Jumbo{RESET}\n")

    slow_print(f"You take a slow yet steady breath, wondering if you should enter...\n")
    slow_print(f"You feel something in your pocket... You reached in and pulled out a...\n")
    slow_print(f"{YELLOW}Coin?{RESET}\n")
    slow_print(f"You counted the coins...")
    slow_print(f"{YELLOW}{coin}{RESET} coins.\n")
    slow_print(F"You could feel a sense of {DIM}curiosity{RESET} and {DIM}excitement{RESET} in your chest.")
    slow_print("You take a deep breath and feel adventurous...\n")
    time.sleep(2)

def run_intro():
    state = start_skip()
    if state is None:
        intro()
        return
    try:
        intro()
    except SkipIntro:
        print(RESET + "\n")
    finally:
        stop_skip(state)



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
    rows.append(f"{box['v']}{' ' * left}{red_you(title)}{' ' * (w - left - len(title))}{box['v']}")
    rows.append(f"{box['ml']}{box['h'] * w}{box['mr']}")
    for label in options:
        pad = w - 1 - len(label)
        label = red_you(label.replace("Casino", f"{GOLD}Casino{RESET}"))
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


def ask(prompt="> ", wait=idle_time, hint="\nPsst... still there?"):
    answered = threading.Event()

    def show(text):
        sys.stdout.write("\r\033[2K")      
        slow_print(f"{DIM}{text}{RESET}")  #
        
        sys.stdout.write(prompt)          
        sys.stdout.flush()

    def watch():
        if answered.wait(wait):
            return
        show(hint)
        if answered.wait(5):
            return
        show("The casino isn't gonna play itself.")
        if answered.wait(8):
            return
        show("Atleast press a button...")
        if answered.wait(5):
            return
        show("You really hate me, don't you?")
        show(f"-10 {GOLD}Coins{RESET}")
        global coin
        coin -= 10

    threading.Thread(target=watch, daemon=True).start()
    try:
        return input(prompt)
    finally:
        answered.set()

#settings menu


def text_speed_menu():
    global text_speed
    print("\n")
    while True:
        draw_menu("TEXT SPEED", ("1. Slow", "2. Normal", "3. Fast", "4. Go Back"))
        pick = ask()
        if pick == "1":
            text_speed = 0.1
            slow_print("Text speed set to slow.\n")
            return
        if pick == "2":
            text_speed = 0.06
            slow_print("Text speed set to normal.\n")
            return
        if pick == "3":
            text_speed = 0.03
            slow_print("Text speed set to fast.\n")
            return
        if pick == "4":
            return

def settings_menu():
    print("\n")
    while True:
        draw_menu("SETTINGS", ("1. Text Speed", "2. Go Back"))
        pick = ask()
        if pick == "1":
            text_speed_menu()
            continue
        if pick == "2":
            draw_menu()
            return



#game starts here
game_start()
run_intro()
draw_menu()

easter_user_count = 0 # if user wants to be greedy this will track >:)
easter_money_earned = False

while running:
    try:
        game_starting = int(ask())
        if game_starting == 1:
            while gamble_game:
                draw_menu("Choose your posion", ("1. Nothing yet...", "2. Go Back", "3. Go Back (But Cooler)"))
                gamble_pick = ask()
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
                slow_print(".", text_speed=0.4)
                slow_print("..", text_speed=0.4)
                slow_print("...\n", text_speed=0.4)
                draw_menu()
            if stall_count == 2:
                slow_print("\nYou stalled again... You seem to be bored.")
                slow_print("You took a deep sigh...\n")
                slow_print(".", text_speed=0.4)
                slow_print("..", text_speed=0.4)
                slow_print("...\n", text_speed=0.4)
                draw_menu()
            if stall_count == 3:
                slow_print("\nYou've been stalling for too long. Are you gonna enter the casino or what?")
                slow_print("You looked at your shoes... What a pity... Just choose already..\n")
                slow_print(".", text_speed=0.4)
                slow_print("..", text_speed=0.4)
                slow_print("...\n", text_speed=0.4)
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
            easter_user_count += 1
            if not easter_money_earned:
                slow_print("\nSilly little cheater...")
                slow_print(f"+100 {YELLOW}coins{RESET}!\n") # adds coins for user finding easter egg
                coin += 100
                easter_money_earned = True
            else:
                slow_print("\nYou've already found the easter egg!\n")
                slow_print(f"Don't be so {GREEN}greedy{RESET}...\n")
                slow_print("Quick tip! Press 'I' to see your inventory!\n")
            draw_menu()
            continue


    except ValueError:
        pass
    slow_print("\nPsst...", text_speed=0.07)
    slow_print(f"Choose a valid option. {GREEN}Oddball{RESET}..\n", text_speed=0.1)
    time.sleep(1)
    draw_menu()
slow_print(f"Through the {DIM}night{RESET} of fall, only the brave remain.\n", text_speed=0.07)
