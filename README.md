# Wumbo Jumbo Casino Game

A tiny story-based text game that's just for the terminal and written in Python.

> **Status:** (v1.0.2). The intro, the menu, the settings, and coins are in.
> The casino games are still cooking.

## About

You wake up in an alley with no idea how you got there. Follow the light and
see what is waiting for you at the end of it.

## Features

- Typewriter-style text that prints one character at a time to keep you engaged and interested. You can change the speed in settings.
- Colored text to make the game more visually appealing.
- Amazing menu animations
- Press f to skip the intro, press g to speed up the line that's typing
- The game gets impatient if you sit at a prompt too long. Its lowkenoinely sentinent?
- A coin pouch that starts at 100 coins
- Hidden features and easter eggs?

## Requirements

- Python 3 (developed and tested with Python 3.13)
- A terminal that supports ANSI colors

There are no third-party dependencies. The game only uses the Python standard
library.

## Running the game

```bash
python3 gambling-game.py
```

(NOTE: To skip the intro entirely, press f. Press g to speed up a line.)

## How to play

After the intro, choose an option from the menu by typing its number and
pressing Enter:

| Option | Action           |
| ------ | ---------------- |
| 1      | Enter the Casino |
| 2      | Stall time       |
| 3      | Settings         |
| 4      | Walk away        |

Option 1 opens a menu of its own, which is still empty. Option 2 stalls time and
the game keeps count, so don't push your luck. Option 3 opens the settings menu,
where you can change the text speed. Option 4 ends the game. See the roadmap below.

## Settings

Right now it's just Text Speed: Slow, Normal, or Fast. It changes right away,
although it doesn't save :(

## Roadmap

- [x] Coin system (basic)
- [ ] Actual casino games (slots, blackjack, whatever)
- [ ] Inventory (the game says press I, but there's nothing there yet)
- [ ] Saving your stuff between runs
- [ ] ASCII art text
- [ ] More settings (color themes, etc.)

## Project files

| File                | Purpose                                  |
| ------------------- | ---------------------------------------- |
| `gambling-game.py`  | The game                                 |
| `requirements.txt`  | Python dependencies (currently none)     |
| `CHANGELOG.md`      | What changed in each version             |

## Author

Made by slopmanufacturer.
