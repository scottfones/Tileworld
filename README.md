# CISC 489: Programming Assignment 1 - Tileworld

## Assignment

### Get Started

Download the code and create an environment with following packages:
`pip install pygame`
`pip install numpy`

### Instructions

1. The simulator provides an environment as an N x N Tileworld, in which there are randomly generated walls as obstacles and randomly generated coins as rewards.
   1. No agents can walk through the walls or get outside of the Tileworld.
   2. Once generated, the walls are fixed through the game.
   3. Each coin will have a lifespan ranging from "1-5" seconds, and a value ranging from 1-9.
   4. If an agent successfully hits/collects a coin, it will get +coin.value (line 52 and 56 in `main.py`).
   5. If two agents collide, each of the agents will get -100 (line 65 and 66 in `main.py`).
   6. The goal is to get the total score as high as possible (line 77 in `main.py`).
2. You only need to implement your design in `coopAgent.py`, complete the two classes `playerA()` and `playerB()`.
3. In `main.py`, four cases are listed. One may change the case number to switch between cases. Initially "Case 0" is set (`case = 0`).
4. Play with case 0 to get familiar with the environment and the rules.
Then try the rest cases:
   1. Case 1: two random agents in the Tileworld. This serves as the base case, in order that one may make comparison with their design.
   2. Case 2: one random agent and one self-designed agent in the Tileworld. Please design a rational agent (at least it should be better than Case 1).
   3. Case 3: two self-designed agents in the Tileworld. Please design two collaborative agents (at least it should work better than Case 2).
5. You may change some variables in `env.py`, to experience different setup of the Tileworld (e.g. larger `N` for a larger world, different `SEED` for a world with different obstacles and/or coin sets).
6. In `coopAgent.py`, pay attention to the `update` function (line 51). The simulator will automatically update the information of the world as time goes (all objects are saved in `all_sprites` and updated, line 47 in `main.py`, although you didn't explicitly call `update` of your player classes). At each time step, you can call `pygame.time.get_ticks()` (line 56) to get the current time (note: pygame time works in millisecond), call `get_coin_data()` to access current information of the coins on the map, call `get_wall_data()` to get current information of the walls (You don't need to call it every time since the walls are fixed once generated, but for the next assignment, the walls may be generated and disappear randomly).
