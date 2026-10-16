# Wumbo Jumbo Casino Game

A tiny story-based text game that's just for the terminal and written in Python.

> **Status:** (v1.0.1). The intro, the menu, and an empty settings screen exist.

## About

You wake up in an alley with no idea how you got there. Follow the light and
see what is waiting for you at the end of it.

## Features

- Typewriter-style text that prints one character at a time to keep you engaged and interested
- Colored text to make the game more visually appealing
- Amazing menu animations
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

(NOTE: To skip the intro entirely, press f)

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
which is also still empty. Option 4 ends the game. See the roadmap below.

## Roadmap

- [ ] Coin system
- [ ] More menu options
- [ ] Actual settings options to put in the settings menu
- [ ] ASCII art text

## Project files

| File                | Purpose                                  |
| ------------------- | ---------------------------------------- |
| `gambling-game.py`  | The game                                 |
| `requirements.txt`  | Python dependencies (currently none)     |
| `CHANGELOG.md`      | What changed in each version             |

## Author

Made by slopmanufacturer.
