# floppyAI

![FloppyAI (1)](https://user-images.githubusercontent.com/28866719/198844012-0f64d016-b9d5-4f0e-ab6e-8d8575d2eba6.png)

A flappy bird clone using machine learning ([NEAT-Python](https://link-url-here.org)) to play the game optimally and Pygame for the visuals.

The main objective here is to practice coding in Python, learn about machine learning and getting used to Python object orientation.

Important to Note:

-Running this through WSL will cause errors if your graphic drivers for WSL are not sorted. I recommend to skip the headache and rather run this with a native Linux install or Windows/Mac.

-Since the game is quite simple the AI will often generate a population capable of solving the problem within a generation or two even after slightly randomizing the positions that the obsticles spawn at if running large populations. For this reason it is recommended to run only 5 simultanious populations if you like to see the AI suffer like I do.

Potential improvments in the future:

- Proper Python docstrings.
- Add complexity to the game. Ex. A "fuel" resource required for the node to pickup to be able to continue to move.
- Create a bigger draw window.

Installation & Usage:

Requirements: Python3.8 at a minimum, pip3

1. Clone the repo.
2. Install libraries using pip listed in requirements.txt by running `pip3 install -r requirements.txt`
3. Run the program.

Yep, thats it.


