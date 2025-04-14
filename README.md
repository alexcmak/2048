# SetGame

A simple 1-player Python implemenation of the classic card game SET.

## Requirements

You will need **Python 3** and **pygame**

Please read more about [how to install](https://www.pygame.org/wiki/GettingStarted) pygame.

**pip** can be tricky to run, pygame can be tricky to install. This may help you:

`pip install pygame --pre`

To run this game once you have python and pygame, run something like this in the command line:

`python SETGame.py`

## Features

This game displays up to 4 rows of cards. Pick any 3 cards and the program will tell you if the cards satisify the requirements to make a _set_.
Please read more about the SET game [here](https://en.wikipedia.org/wiki/Set_(card_game)).

![screenshot](https://github.com/alexcmak/SETGame/blob/main/images/screen1.png)

- Use left click to select a card
- Hold right click to get a hint 

## Math
There is quite a bit of [math](https://www.setgame.com/sites/default/files/teacherscorner/SETPROOF.pdf) involved in this deceptively simple game. I have not used any _discrete math_ since I studied that in college over 30 years ago. Python is a good choice to write a game like this because it already support "12 choose 3" kind of _combination_ math. 

It's a card game, don't over think it, what good is a _proof_ of how many rows you can get but without a set? This is why I am not and never will be a mathemathican.



## Future Versions

- improved graphics
- help screen that spell out the rules
