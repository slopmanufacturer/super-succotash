# Wumbo Jumbo Casino Game

A tiny story-based text game that's just for the terminal and written in Python.

> **Status:** early draft (v1.0.0). Only the intro, and some parts of the main menu exist.

## About

You wake up in an alley with no idea how you got there. Follow the light and
see what is waiting for you at the end of it.

## Features

- Typewriter-style text that prints one character at a time to keep you engaged and interested
- Colored text to make the game more visually appealing
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
| 3      | Walk away        |

Option 1 does not lead anywhere yet. Option 2 stalls time, and the game keeps
count. Option 3 ends the game. See the roadmap below.

## Roadmap

- [ ] Coin system
- [ ] More menu options
- [ ] Settings menu
- [ ] ASCII art text

## Project files

| File                | Purpose                                  |
| ------------------- | ---------------------------------------- |
| `gambling-game.py`  | The game                                 |
| `requirements.txt`  | Python dependencies (currently none)     |
| `CHANGELOG.md`      | What changed in each version             |

## Author

Made by slopmanufacturer.
