import pygame
from sys import exit
from pygame.math import Vector2
from random import randint, choice

class Fruit():
    def __init__(self):
        self.x_pos = randint(0, cell_no-1)
        self.y_pos = randint(0, cell_no-1)
        self.pos = Vector2(self.x_pos, self.y_pos)
        self.image = pygame.image.load('assets/Graphics/apple.png').convert_alpha()

    def draw_fruit(self):
        self.rect = self.image.get_rect(topleft=(int(self.pos.x * cell_size), int(self.pos.y * cell_size)))
        screen.blit(self.image, self.rect)

    def random_pos(self, pos):
        self.pos = pos

class Snake():
    def __init__(self):
        self.head_pos = Vector2(12, 10)
        self.tail_pos = Vector2(12, 12)
        self.body_pos = [self.head_pos, Vector2(12, 11), self.tail_pos]
        self.head_direction = ''
        self.body_directions = [self.head_direction, '', '']

        # Head
        self.head_image = pygame.image.load('assets/Graphics/head_up.png').convert_alpha()
        # Body
        self.body_vertical = pygame.image.load('assets/Graphics/body_vertical.png').convert_alpha()
        # Tail
        self.tail_image = pygame.image.load('assets/Graphics/tail_down.png').convert_alpha()

        self.body_images = [self.head_image, self.body_vertical, self.tail_image]
        self.body_rects = []
    
    def draw_snake(self):
        # self.body_rects = [pygame.Rect(body_part_pos.x*cell_size, body_part_pos.y*cell_size, cell_size, cell_size) for body_part_pos in self.body_pos]
        self.body_rects = [image.get_rect(topleft=(int(self.body_pos[i].x * cell_size), int(self.body_pos[i].y * cell_size)))
                           for i, image in enumerate(self.body_images)]
        for i in range(len(self.body_images)):
            screen.blit(self.body_images[i], self.body_rects[i])

    def movement(self):
        if self.head_direction == 'up':
            new_head_pos = self.body_pos[0] - Vector2(0, 1)
        elif self.head_direction == 'down':
            new_head_pos = self.body_pos[0] + Vector2(0, 1)
        elif self.head_direction == 'left':
            new_head_pos = self.body_pos[0] - Vector2(1, 0)
        elif self.head_direction == 'right':
            new_head_pos = self.body_pos[0] + Vector2(1, 0)

        # Updating list containing body positions
        self.body_pos = [self.body_pos[i-1] for i in range(len(self.body_pos)) if i!=0]
        self.body_pos.insert(0, new_head_pos)

        # Updating list containing body directions
        self.body_directions = [self.body_directions[i-1] for i in range(len(self.body_directions)) if i!=0]
        self.body_directions.insert(0, self.head_direction)
        # print(self.body_directions)

    def animation(self):
        # Head Images
        head_up = pygame.image.load('assets/Graphics/head_up.png').convert_alpha()
        head_down = pygame.image.load('assets/Graphics/head_down.png').convert_alpha()
        head_left = pygame.image.load('assets/Graphics/head_left.png').convert_alpha()
        head_right = pygame.image.load('assets/Graphics/head_right.png').convert_alpha()
        # Body Straight Images
        self.body_horizontal = pygame.image.load('assets/Graphics/body_horizontal.png').convert_alpha()
        # Tail Images
        tail_down = pygame.image.load('assets/Graphics/tail_down.png').convert_alpha()
        tail_left = pygame.image.load('assets/Graphics/tail_left.png').convert_alpha()
        tail_right = pygame.image.load('assets/Graphics/tail_right.png').convert_alpha()
        tail_up = pygame.image.load('assets/Graphics/tail_up.png').convert_alpha()
        # Body Turn Images
        body_bl = pygame.image.load('assets/Graphics/body_bl.png').convert_alpha()
        body_br = pygame.image.load('assets/Graphics/body_br.png').convert_alpha()
        body_tl = pygame.image.load('assets/Graphics/body_tl.png').convert_alpha()
        body_tr = pygame.image.load('assets/Graphics/body_tr.png').convert_alpha()
        # Updating images according to direction
        for i in range(len(self.body_directions)):
            direction = self.body_directions[i]
            # Checking if body part is head
            if i == 0:
                if direction == 'up': self.body_images[0] = head_up
                elif direction == 'down': self.body_images[0] = head_down
                elif direction == 'left': self.body_images[0] = head_left
                elif direction == 'right': self.body_images[0] = head_right
            # Checking if body part is tail
            elif i == len(self.body_directions)-1:
                direction = self.body_directions[i-1]
                if direction == 'up': self.body_images[-1] = tail_down
                elif direction == 'down': self.body_images[-1] = tail_up
                elif direction == 'left': self.body_images[-1] = tail_right
                elif direction == 'right': self.body_images[-1] = tail_left
            else:
                # Checking if body is moving in a straight line
                if direction == self.body_directions[i-1]:
                    if direction in ['up', 'down']: self.body_images[i] = self.body_vertical
                    elif direction in ['left', 'right']: self.body_images[i] = self.body_horizontal
                # Checking if body has turned
                else:
                    if direction == 'up':
                        if self.body_directions[i-1] == 'left': self.body_images[i] = body_bl
                        if self.body_directions[i-1] == 'right': self.body_images[i] = body_br
                    elif direction == 'down':
                        if self.body_directions[i-1] == 'left': self.body_images[i] = body_tl
                        if self.body_directions[i-1] == 'right': self.body_images[i] = body_tr
                    elif direction == 'left':
                        if self.body_directions[i-1] == 'up': self.body_images[i] = body_tr
                        if self.body_directions[i-1] == 'down': self.body_images[i] = body_br
                    elif direction == 'right':
                        if self.body_directions[i-1] == 'up': self.body_images[i] = body_tl
                        if self.body_directions[i-1] == 'down': self.body_images[i] = body_bl

    def overflow(self):
        for body_part in self.body_pos:
            if body_part.x >= cell_no: body_part.x = -1
            elif body_part.x <= -1: body_part.x = cell_no
            elif body_part.y >= cell_no: body_part.y = -1
            elif body_part.y <= -1: body_part.y = cell_no

    def collide_self(self):
        for rect in self.body_rects[1:]:
            if self.body_rects[0].colliderect(rect):
                global game_status, final_score, score
                final_score = score
                game_status = 'over'

    def extend_body(self, pos):
        self.body_pos.append(Vector2(pos))
        self.body_directions.append(self.body_directions[-1])
        current_dir = self.body_directions[-2]
        if current_dir in ['up', 'down']: self.body_images.insert(-1, self.body_vertical)
        elif current_dir in ['left', 'right']: self.body_images.insert(-1, self.body_horizontal)

    def update(self):
        self.overflow()
        self.draw_snake()
        self.collide_self()


def draw_background(screen, cell_no, cell_size):
    for x in range(cell_no):
        for y in range(cell_no):
            bg_rect = pygame.rect.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            if (x+y) % 2 == 0:
                pygame.draw.rect(screen, '#a7d13d', bg_rect)
            else:
                pygame.draw.rect(screen, '#aed746', bg_rect)

def game_over_screen(screen):
    big_font = pygame.font.Font('assets/Font/PoetsenOne-Regular.ttf', 75)
    snake_surf = big_font.render('SNAKE', True, 'black')
    snake_rect = snake_surf.get_rect(center=(360, 300))

    endscore_font = pygame.font.Font(None, 70)
    endscore_surf = endscore_font.render('SCORE: ' + str(final_score), True, 'black')
    endscore_rect = endscore_surf.get_rect(center=(360, 400))

    screen.blit(snake_surf, snake_rect)
    screen.blit(endscore_surf, endscore_rect)

pygame.init()

cell_size = 40
cell_no = 18
score_font = pygame.font.Font(None, 55)
screen = pygame.display.set_mode((cell_size*cell_no, cell_size*cell_no))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

game_status = 'over'
ate_fruit = False
current_tail_pos = (0, 0)
score = 0
final_score = 0

fruit = Fruit()
snake = Snake()

move_snake = pygame.USEREVENT + 1
pygame.time.set_timer(move_snake, 150)

while True:
    # ----------------- Event Loop --------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_status == 'over' and event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                game_status = 'standby'

        else:
            # Checks if game has already started and deals with keyboard input and snake movement if it has
            if game_status == 'active':
                if event.type == move_snake:
                    snake.movement()
                    snake.animation()
                    if ate_fruit:
                        snake.extend_body(current_tail_pos)
                        ate_fruit = False

                if event.type == pygame.KEYDOWN and (-1 < snake.body_pos[0].x < cell_no and -1 < snake.body_pos[0].y < cell_no): # 2nd condition checks if head is in frame
                    if event.key == pygame.K_UP: snake.head_direction = 'up'
                    elif event.key == pygame.K_DOWN: snake.head_direction = 'down'
                    elif event.key == pygame.K_LEFT: snake.head_direction = 'left'
                    elif event.key == pygame.K_RIGHT: snake.head_direction = 'right'

            if game_status == 'standby' and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.head_direction = 'up'
                    game_status = 'active'
                elif event.key == pygame.K_DOWN:
                    snake.head_direction = 'down'
                    game_status = 'active'
                elif event.key == pygame.K_LEFT:
                    snake.head_direction = 'left'
                    game_status = 'active'
                elif event.key == pygame.K_RIGHT:
                    snake.head_direction = 'right'
                    game_status = 'active'
    # ---------------------- Event Loop --------------------------------------

    draw_background(screen, cell_no, cell_size)

    if game_status == 'over':
        game_over_screen(screen)
        snake = Snake()
        score = 0

    else:        
        fruit.draw_fruit()
        snake.update()

        score_surf = score_font.render('SCORE: ' + str(score), True, 'black')
        score_rect = score_surf.get_rect(bottomright=(710, 720))
        screen.blit(score_surf, score_rect)

        if snake.body_rects[0].colliderect(fruit.rect):
            ate_fruit = True
            score += 1
            current_tail_pos = (snake.body_pos[-1].x, snake.body_pos[-1].y)
            total_pos = []
            for x in range(cell_no):
                for y in range(cell_no):
                    total_pos.append((x, y))
            score_positions = [(13, 17), (14, 17), (15, 17), (16, 17), (17, 17)]
            occupied_positions = [(part.x, part.y) for part in snake.body_pos] + [(fruit.x_pos, fruit.y_pos)] + score_positions
            coords = choice(list(set(total_pos) - set(occupied_positions)))
            pos = Vector2(coords)
            fruit.random_pos(pos)

    pygame.display.update()
    clock.tick(60)
