import pygame
import random
import time

# Настройки окна
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128, 50)  
FPS = 60

# Настройки кружочков
CIRCLE_RADIUS = 20
CIRCLE_SPEED = 1
CONTROLLED_SPEED = 5
CHANGE_DIRECTION_TIME = 1  # время в секундах
NEIGHBOR_RADIUS = 150
UPDATE_LIFE_TIME = 10  # интервал обновления жизни в секундах

class Circle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.choice([-CIRCLE_SPEED, CIRCLE_SPEED])
        self.vy = random.choice([-CIRCLE_SPEED, CIRCLE_SPEED])
        self.last_direction_change = time.time()

    def move(self):
        if time.time() - self.last_direction_change >= CHANGE_DIRECTION_TIME:
            self.vx = random.choice([-CIRCLE_SPEED, CIRCLE_SPEED])
            self.vy = random.choice([-CIRCLE_SPEED, CIRCLE_SPEED])
            self.last_direction_change = time.time()

        self.x += self.vx
        self.y += self.vy

        if self.x - CIRCLE_RADIUS < 0 or self.x + CIRCLE_RADIUS > WIDTH:
            self.x -= self.vx
            self.vx *= -1
        if self.y - CIRCLE_RADIUS < 0 or self.y + CIRCLE_RADIUS > HEIGHT:
            self.y -= self.vy
            self.vy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, GRAY, (self.x, self.y), NEIGHBOR_RADIUS, 1)
        pygame.draw.circle(screen, self.color, (self.x, self.y), CIRCLE_RADIUS)

    def check_click(self, pos):
        return (self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2 <= CIRCLE_RADIUS ** 2

    def check_neighbors(self, circles):
        neighbors = 0
        for circle in circles:
            if circle is not self and ((self.x - circle.x)**2 + (self.y - circle.y)**2) <= NEIGHBOR_RADIUS**2:
                neighbors += 1
        if neighbors == 0 or neighbors > 3:
            return 'die'
        elif neighbors == 2:
            return 'birth'
        return 'survive'

def show_start_screen():
    title_font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 60)
    rules_font = pygame.font.Font(None, 20)
    title = title_font.render('GAME OF LIFE', True, pygame.Color('white'))
    play_button = button_font.render('Play', True, pygame.Color('green'))
    rules = rules_font.render('click to control - survive as long as you can - if circle has 2 neighbours it will generate new one - less then 2 = die', True, pygame.Color('white'))

    title_rect = title.get_rect(center=(WIDTH / 2, HEIGHT / 3))
    button_rect = play_button.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    rules_rect = rules.get_rect(center=(WIDTH / 2, HEIGHT / 1.5))

    screen.fill(BACKGROUND_COLOR)
    screen.blit(title, title_rect)
    screen.blit(play_button, button_rect)
    screen.blit(rules, rules_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True

def show_game_over_screen(cycles):
    screen.fill(BACKGROUND_COLOR)
    game_over_font = pygame.font.Font(None, 60)
    info_font = pygame.font.Font(None, 40)
    game_over_text = game_over_font.render('GAME OVER', True, pygame.Color('red'))
    info_text = info_font.render(f'You survived {cycles} cycles.', True, pygame.Color('white'))
    restart_button = info_font.render('Restart', True, pygame.Color('green'))
    
    game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 3))
    info_rect = info_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    restart_rect = restart_button.get_rect(center=(WIDTH / 2, HEIGHT / 1.5))
    
    screen.blit(game_over_text, game_over_rect)
    screen.blit(info_text, info_rect)
    screen.blit(restart_button, restart_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return True

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

clock = pygame.time.Clock()
circles = [Circle(random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS), random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS), WHITE) for _ in range(10)]
controlled_circle = None
last_update = time.time()
font = pygame.font.Font(None, 32)
cycle_count = 0

running = True
if show_start_screen():  # Показать начальный экран и ждать действия пользователя
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for circle in circles:
                    if circle.check_click(pos):
                        if controlled_circle:
                            controlled_circle.color = WHITE
                        circle.color = GREEN
                        controlled_circle = circle
                        break

        keys = pygame.key.get_pressed()
        if controlled_circle:
            if keys[pygame.K_LEFT] and controlled_circle.x - CIRCLE_RADIUS > 0:
                controlled_circle.x -= CONTROLLED_SPEED
            if keys[pygame.K_RIGHT] and controlled_circle.x + CIRCLE_RADIUS < WIDTH:
                controlled_circle.x += CONTROLLED_SPEED
            if keys[pygame.K_UP] and controlled_circle.y - CIRCLE_RADIUS > 0:
                controlled_circle.y -= CONTROLLED_SPEED
            if keys[pygame.K_DOWN] and controlled_circle.y + CIRCLE_RADIUS < HEIGHT:
                controlled_circle.y += CONTROLLED_SPEED

        screen.fill(BACKGROUND_COLOR)
        for circle in circles:
            if circle != controlled_circle:
                circle.move()
            circle.draw(screen)

        # Display cycle count
        cycle_text = font.render(f'Cycle: {cycle_count}', True, pygame.Color('white'))
        screen.blit(cycle_text, (10, 10))

        # Display countdown timer
        timer_seconds = UPDATE_LIFE_TIME - int(time.time() - last_update)
        timer_text = font.render(f'Next update in: {timer_seconds} seconds', True, pygame.Color('white'))
        timer_rect = timer_text.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(timer_text, timer_rect)

        if time.time() - last_update >= UPDATE_LIFE_TIME:
            new_circles = []
            for circle in circles:
                action = circle.check_neighbors(circles)
                if action == 'survive':
                    new_circles.append(circle)
                elif action == 'birth':
                    new_circles.append(circle)
                    new_circles.append(Circle(random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS), random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS), WHITE))
            circles = new_circles
            last_update = time.time()

            if len(circles) <= 1:
                running = show_game_over_screen(cycle_count)
                if running:
                    cycle_count = 0
                    circles = [Circle(random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS), random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS), WHITE) for _ in range(10)]
                    controlled_circle = None
                    last_update = time.time()
                else:
                    break
            cycle_count += 1
        
        pygame.display.flip()
        clock.tick(FPS)
else:
    running = False

pygame.quit()
