# Changelog

What's new in the Wumbo Jumbo Casino Game.

## Unreleased

Stuff that's in the game right now but not in a version yet.

### Added

- Text Speed in the settings menu. Slow, Normal, and Fast. It actually changes the typing speed now.
- The game gets impatient if you sit at a prompt. It starts yapping after 10 seconds, and if you keep ignoring it, it takes 10 coins.
- Press g to speed up the line that's typing. f still skips the intro.
- Every "you" is red now. You, your, you're, all of it.
- You start with 100 coins. The easter egg gives you 100 more, but only once.
- The menu redraws after the easter egg messages so you're not left staring at nothing.

### Changed

- Settings stays on the settings menu after you change the text speed.
- Took out the empty Text Color option. Just Text Speed and Go Back now.
- Menu titles and options get the red "you" treatment too.

### Fixed

- Text Speed actually works. Before it was changing a variable that slow_print didn't even use.
- The easter egg doesn't just do nothing on the second try anymore. It tells you you already found it.
- "Go Back" in settings actually goes back instead of saying nothing is here.
- Fixed the delay/text_speed mix-up in slow_print.

## 1.0.1 - 2026-10-16

Menu changes, settings, and fixes.

### Added

- A settings menu (option 3). It's empty right now, but it exists.
- Option 1 now has an actual game menu.
- The menu draws itself, a sleek yet nice animation.
- New colored texts for some dialogues.

### Changed

- Made room for the new settings option
- Colored words don't slow down the dialogue anymore

### Fixed

- Fixed some logical issues
- Stalls get counted correctly now

## 1.0.0 - 2026-10-14

First playable draft.

### Added

- A nice and neat intro that sets the mood of the game!
- A typewriter effect for better engagement
- Text colors for visualmaxxing
- A basic menu system.
- A little easter egg. maybe
- `README.md` and `requirements.txt`.

### Changed

- Nothing yet since this is the first version :(

### Removed

- Nothing yet since this is the first version :(
