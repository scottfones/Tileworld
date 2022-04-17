from enum import Enum, unique
from env import *

import heapq
import math

# Design your own agent(s) in this file.
# You can use your own favorite icon or as simple as a colored square (with different colors) to represent your agent(s).
playerA_img = pygame.image.load(os.path.join("img", "playerA.png")).convert()
playerB_img = pygame.image.load(os.path.join("img", "playerB.png")).convert()
sonic_img = pygame.image.load(os.path.join("img", "sonic_art.png")).convert()


class PlayerA(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerA_img
        self.image = pygame.transform.scale(playerA_img, (WALLSIZE, WALLSIZE))
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(
            self.image, rand_color(random.randint(0, N)), self.image.get_rect(), 3
        )
        self.rect = self.image.get_rect()  # get image position
        self.rect.x = 0
        self.rect.y = 0
        self.speedx = SPEED
        self.speedy = SPEED
        self.score = 0
        self.steps = 0

    def move(self, direction):
        if direction == "r":
            self.steps += 1
            self.rect.x += self.speedx
            if self.is_player_collide_wall():
                self.rect.x -= self.speedx
        if direction == "l":
            self.steps += 1
            self.rect.x -= self.speedx
            if self.is_player_collide_wall():
                self.rect.x += self.speedx
        if direction == "u":
            self.steps += 1
            self.rect.y -= self.speedy
            if self.is_player_collide_wall():
                self.rect.y += self.speedy
        if direction == "d":
            self.steps += 1
            self.rect.y += self.speedy
            if self.is_player_collide_wall():
                self.rect.y -= self.speedy

    def is_player_collide_wall(self):
        for wall in walls:
            if self.rect.colliderect(wall):
                return True
        return False

    def update(self):
        print(
            "Current Time in milliseconds:", pygame.time.get_ticks()
        )  ## get current time
        print("Coin Data:", get_coin_data())  ## get current information of the coins
        print(
            "Wall Positions:", get_wall_data()
        )  ## get current information of the walls
        direction = 1
        # print(direction)
        if direction == 0:
            self.move("l")  ## move left
        if direction == 1:
            self.move("r")  ## move right
        if direction == 2:
            self.move("u")  ## move up
        if direction == 3:
            self.move("d")  ## move down

        # Avoid colliding with wall and go out of edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


# You can design another player class to represent the other player if they work in different ways.
class PlayerB(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerB_img
        self.image = pygame.transform.scale(playerB_img, (WALLSIZE, WALLSIZE))
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(
            self.image, rand_color(random.randint(0, N)), self.image.get_rect(), 3
        )
        self.rect = self.image.get_rect()  # get image position
        self.rect.x = 0
        self.rect.y = 0
        self.speedx = SPEED
        self.speedy = SPEED
        self.score = 0
        self.steps = 0

    def move(self, direction):
        if direction == "r":
            self.steps += 1
            self.rect.x += self.speedx
            if self.is_player_collide_wall():
                self.rect.x -= self.speedx
        if direction == "l":
            self.steps += 1
            self.rect.x -= self.speedx
            if self.is_player_collide_wall():
                self.rect.x += self.speedx
        if direction == "u":
            self.steps += 1
            self.rect.y -= self.speedy
            if self.is_player_collide_wall():
                self.rect.y += self.speedy
        if direction == "d":
            self.steps += 1
            self.rect.y += self.speedy
            if self.is_player_collide_wall():
                self.rect.y -= self.speedy

    def is_player_collide_wall(self):
        for wall in walls:
            if self.rect.colliderect(wall):
                return True
        return False

    def update(self):
        direction = 3
        # print(direction)
        if direction == 0:  ## left
            self.move("l")
        if direction == 1:  ## right
            self.move("r")
        if direction == 2:  ## up
            self.move("u")
        if direction == 3:  ## down
            self.move("d")

        # Avoid colliding with wall and go out of edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


# Hint: To cooperate, it's better if your agents explore different areas of the map, so you can write a
# communication function to broadcast their locations in order that they can keep a reasonable distance from each other.
# The bottom line is at least they shouldn't collide with each other.
# You may try different strategies (e.g. reactive, heuristic, learning, etc).


@unique
class Movement(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


def get_distance(a: tuple[int, int], b: tuple[int, int]) -> float:
    """Return the two norm distance between two points.

    Left as a float to devalue diagonal moves.
    """
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class PlayerReactivePartJiggle(pygame.sprite.Sprite):
    """Defines a Reactive, Partitioned, Jiggly agent.

    The agent is reactive in pursuing the closest coin.
    The agent is partitioned in its responsibilities (top/bottom of map).
    The agent jiggles when stuck. If its path is blocked, it will move in a random direction.
    """

    def __init__(self, is_top: bool):
        """Initialize the agent."""
        pygame.sprite.Sprite.__init__(self)
        self.image = sonic_img
        self.image = pygame.transform.scale(sonic_img, (WALLSIZE, WALLSIZE))
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(
            self.image, rand_color(random.randint(0, N)), self.image.get_rect(), 1
        )
        self.rect = self.image.get_rect()  # get image position
        self.rect.x = 0
        self.rect.y = 0
        self.speedx = SPEED
        self.speedy = SPEED
        self.score = 0
        self.steps = 0

        self.is_top = is_top
        self.my_pos = (0, 0)
        self.wall_pos = [
            (wall[0] // self.speedx, wall[1] // self.speedy) for wall in get_wall_data()
        ]

    def move(self, direction):
        """Translate movement intention into a change in position."""
        self.steps += 1
        match direction:
            case Movement.RIGHT:
                self.rect.x += self.speedx
                if self.is_player_collide_wall():
                    self.rect.x -= self.speedx
            case Movement.LEFT:
                self.rect.x -= self.speedx
                if self.is_player_collide_wall():
                    self.rect.x += self.speedx
            case Movement.UP:
                self.rect.y -= self.speedy
                if self.is_player_collide_wall():
                    self.rect.y += self.speedy
            case Movement.DOWN:
                self.rect.y += self.speedy
                if self.is_player_collide_wall():
                    self.rect.y -= self.speedy

        # Avoid colliding with wall and go out of edges
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def is_player_collide_wall(self):
        """Determine wall collision state."""
        for wall in walls:
            if self.rect.colliderect(wall):
                return True
        return False

    def _is_move_blocked(self, mov_dir: Movement) -> bool:
        next_pos = (
            self.my_pos[0] + mov_dir.value[0],
            self.my_pos[1] + mov_dir.value[1],
        )
        if next_pos in self.wall_pos:
            return True
        return False

    def update(self):
        """Implement agent's reactive logic.

        All coin locations are placed into a priority queue based on
        distance to the agent, with coin value as a tie breaker. We pop
        an item off the queue to get the goal coin and move accordingly.

        If the agent is stuck, we move in a random direction.
        """
        if self.rect.y / HEIGHT < 0.5 and not self.is_top:
            self.move(Movement.DOWN)
            return

        self.my_pos = (self.rect.x // self.speedx, self.rect.y // self.speedy)

        targets: list[tuple[float, int, tuple[int, int]]] = []
        coin_values, coin_pos = get_coin_data()
        for coin in coins:
            match (coin.rect.y / HEIGHT > 0.5, self.is_top):
                case (True, True):
                    continue
                case (False, False):
                    continue
            pos = (coin.rect.y // self.speedy, coin.rect.x // self.speedx)
            dist = get_distance(
                (self.rect.y / self.speedy, self.rect.x / self.speedx), (pos[0], pos[1])
            )
            heapq.heappush(targets, (dist, coin.value, (pos[0], pos[1])))

        if targets:
            goal = heapq.heappop(targets)
            rel_up_down = goal[2][0] - self.rect.y // self.speedy
            rel_left_right = goal[2][1] - self.rect.x // self.speedx

            if rel_left_right > 0 and not self._is_move_blocked(Movement.RIGHT):
                self.move(Movement.RIGHT)
            elif rel_left_right < 0 and not self._is_move_blocked(Movement.LEFT):
                self.move(Movement.LEFT)
            elif rel_up_down > 0 and not self._is_move_blocked(Movement.DOWN):
                self.move(Movement.DOWN)
            elif rel_up_down < 0 and not self._is_move_blocked(Movement.UP):
                self.move(Movement.UP)
            else:
                next_move = random.choice(
                    [
                        mov_dir
                        for mov_dir in Movement
                        if not self._is_move_blocked(mov_dir)
                    ]
                )
                self.move(next_move)


class PlayerReactivePartPath(PlayerReactivePartJiggle):
    """Defines a Reactive, Partitioned, Pathfinding agent.

    The agent is reactive in pursuing the closest coin.
    The agent is partitioned in its responsibilities (top/bottom of map).
    The agent uses a pathfinding algorithm to move to the closest coin.
    """

    def __init__(self, is_top: bool):
        """Initialize the agent."""
        super().__init__(is_top)

    def update(self):
        """Implement agent's reactive logic.

        All coin locations are placed into a priority queue based on
        distance to the agent, with coin value as a tie breaker. We pop
        an item off the queue to get the goal coin and move accordingly.

        If the agent is stuck, we move in a random direction.
        """
        if self.rect.y / HEIGHT < 0.5 and not self.is_top:
            self.move("d")
            return

        self.my_pos = (self.rect.x // self.speedx, self.rect.y // self.speedy)

        goal = None
        while goal == None:
            for dir in ["u", "d", "l", "r"]:
                pass
