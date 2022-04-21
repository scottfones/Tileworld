"""User defined players."""
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
        self.rect: pygame.rect.Rect = self.image.get_rect()  # get image position
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
        for wall in get_wall_data():
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
        self.rect: pygame.rect.Rect = self.image.get_rect()  # get image position
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
    """Movement enum to represent the direction of the agent."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


def get_distance(a: tuple[int, int], b: tuple[int, int], m_type: str) -> float:
    """Return the distance between a and b Distance.

    m_type:
        "e": Euclidean Distance
        "m": Manhattan Distance
    """
    match m_type:
        case "e":
            return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        case "m":
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
    return -1


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
        self.rect: pygame.rect.Rect = self.image.get_rect()  # get image position
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
            if self.rect.colliderect(wall):  # type: ignore
                return True
        return False

    def _is_move_blocked(self, mov_dir: Movement) -> bool:
        """Determine if a movement would be blocked."""
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
        for (c_val, c_loc) in zip(coin_values, coin_pos):

            match (c_loc[1] / HEIGHT > 0.5, self.is_top):
                case (True, True):
                    continue
                case (False, False):
                    continue
            pos = (c_loc[1] // self.speedy, c_loc[0] // self.speedx)
            dist = get_distance(
                (self.rect.y // self.speedy, self.rect.x // self.speedx),
                (pos[0], pos[1]),
                "e",
            )
            heapq.heappush(targets, (dist, 9 - c_val, (pos[0], pos[1])))

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

class PlayerHybridPartPath(pygame.sprite.Sprite):
    """Defines a Hybrid, Partitioned, Pathfinding agent.

    The agent is hybrid in pursuing the best coin.
    The agent is partitioned in its responsibilities (top/bottom of map).
    The agent uses a pathfinding algorithm to move to the closest coin.
    """

    p_top_pos: tuple[int, int] = (-1, -1)
    p_bot_pos: tuple[int, int] = (-1, -1)

    def __init__(self, is_alpha: bool):
        """Initialize the agent."""
        pygame.sprite.Sprite.__init__(self)
        self.image = sonic_img
        self.image = pygame.transform.scale(sonic_img, (WALLSIZE, WALLSIZE))
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(
            self.image, rand_color(random.randint(0, N)), self.image.get_rect(), 1
        )
        self.rect: pygame.rect.Rect = self.image.get_rect()  # get image position
        self.rect.x = 0
        self.rect.y = 0
        self.speedx = SPEED
        self.speedy = SPEED
        self.score = 0
        self.steps = 0

        self.is_alpha = is_alpha
        self.is_init_sep = True
        self.my_pos = (0, 0)
        self.path = None
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
            if self.rect.colliderect(wall):  # type: ignore
                return True
        return False

    def _is_move_blocked(self, mov_dir: Movement) -> bool:
        """Determine if a movement would be blocked."""
        next_pos = (
            self.my_pos[0] + mov_dir.value[0],
            self.my_pos[1] + mov_dir.value[1],
        )
        if next_pos in self.wall_pos:
            return True
        return False

    def update(self):
        """Implement agent's hybrid logic."""
        if self.is_init_sep:
            match self.is_alpha:
                case True if self.rect.x / WIDTH < 0.5:
                    self.move(Movement.RIGHT)
                    return
                case True:
                    self.is_init_sep = False
                case False if self.rect.y / HEIGHT < 0.5:
                    self.move(Movement.DOWN)
                    return
                case False:
                    self.is_init_sep = False

        self.my_pos = (self.rect.x // self.speedx, self.rect.y // self.speedy)

        coin_vals, coin_pos = get_coin_data()
        self.coin_pos = []
        for c_val, c_loc in zip(coin_vals, coin_pos):
            if self.is_alpha and c_loc[1] / HEIGHT < 0.5:
                self.coin_pos.append((c_loc[0] // self.speedx, c_loc[1] //self.speedy))
            elif not self.is_alpha and c_loc[1] / HEIGHT > 0.5:
                self.coin_pos.append((c_loc[0] // self.speedx, c_loc[1] //self.speedy))

        if not self.path or self.path[0] not in self.coin_pos:
            visited, next_pos = self.find_path()

            self.path = [next_pos]
            while next_pos != self.my_pos:
                next_pos = visited[next_pos]
                self.path.append(next_pos)


        cmp_pos = self.path.pop()
        rel_x = cmp_pos[0] - self.my_pos[0]
        rel_y = cmp_pos[1] - self.my_pos[1]
        match (rel_x, rel_y):
            case (1, 0):
                self.move(Movement.RIGHT)
            case (-1, 0):
                self.move(Movement.LEFT)
            case (0, 1):
                self.move(Movement.DOWN)
            case (0, -1):
                self.move(Movement.UP)

        if self.is_alpha:
            PlayerHybridPartPath.p_top_pos = self.my_pos
        else:
            PlayerHybridPartPath.p_bot_pos = self.my_pos


    def find_path(self):
        frontier = []
        visited = {}

        # frontier: (priority, current_pos, prev_pos)
        heapq.heappush(frontier, (0, self.my_pos, self.my_pos))
        # Get the path to the closest coin
        while frontier:
            current = heapq.heappop(frontier)

            for mov_dir in Movement:
                next_pos = (
                    current[1][0] + mov_dir.value[0],
                    current[1][1] + mov_dir.value[1],
                )
                if -1 in next_pos:
                    continue
                if next_pos[0] > WIDTH // self.speedx or next_pos[1] > HEIGHT // self.speedy:
                    continue

                if next_pos in visited.values():
                    continue
                if next_pos in self.wall_pos:
                    continue
                if next_pos in self.coin_pos:
                    visited[next_pos] = current[1]
                    return visited, next_pos

                heapq.heappush(
                    frontier,
                    (
                        current[0] + 1,
                        next_pos,
                        current[1],
                    ),
                )
                visited[next_pos] = current[1]

        return visited, self.my_pos
