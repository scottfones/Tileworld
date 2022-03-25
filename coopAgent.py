from env import *

# Design your own agent(s) in this file.
# You can use your own favorite icon or as simple as a colored square (with different colors) to represent your agent(s).
playerA_img = pygame.image.load(os.path.join("img", "playerA.png")).convert()
playerB_img = pygame.image.load(os.path.join("img", "playerB.png")).convert()


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
