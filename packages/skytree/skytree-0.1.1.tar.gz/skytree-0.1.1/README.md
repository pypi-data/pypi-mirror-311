# Skytree
2D game framework for Python
_Version 0.1.1_

Skytree is a flexible, easy-to-use 2D game framework that leverages Pygame for creating side-scrolling platformers and other games with Python.

![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey)

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License, which allows you to share and adapt the material for non-commercial purposes as long as you provide appropriate attribution and share any adaptations under the same license.  
For more information, see [CC BY-NC-SA 4.0 License](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Features
Skytree uses Pygame to render 2D graphics, play audio and read user inputs. At the moment, only keyboard inputs are supported.
The engine abstracts the game loop from the user, provides a standard structure for active game objects and a way to manage game resources.
Objects are generally constructed by combining basic features (e.g., Drawable, Updateable) via multiclassing and can be connected or disconnected
ultimately to a game manager singleton object in order to make them active or inactive.
Drawable objects provide methods to manipulate their draw order and alignment, and there is a frame-by-frame animation system.
Skytree features a collision detection-response system with support for different shaped hitboxes.
User inputs are translated to string commands that can be interpreted by the game objects.
There is a system of classes dedicated to modeling game entities and spaces, with a focus on sidescrolling platformers.

## Installation

### Install via pip

The easiest way to install Skytree is through pip:

```
pip install skytree
```

### Dependencies

Skytree requires `pygame` version 2.6. When you install via pip, this will be handled automatically.

