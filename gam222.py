import pygame
import sys
from PIL import Image, ImageSequence

# Настройки окна
WIDTH, HEIGHT = 400, 300
FPS = 10

# Цвета
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja Death Animation")
clock = pygame.time.Clock()

# Шрифт для текста
font = pygame.font.SysFont("arialblack", 48)

# Загрузка кадров гифки
gif_path = "kluotpvvn3y71.gif"
frames = []
pil_gif = Image.open(gif_path)
for frame in ImageSequence.Iterator(pil_gif):
    frame = frame.convert("RGBA")
    py_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
    frames.append(py_image)

# Состояния
frame_index = 0
animation_done = False
blink_counter = 0
show_sprite = True
blink_timer = 0
blinking = False
show_death_text = False
death_text_timer = 0

# Основной игровой цикл
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not animation_done:
        screen.blit(frames[frame_index], (WIDTH // 2 - 48, HEIGHT // 2 - 48))
        frame_index += 1
        if frame_index >= len(frames):
            animation_done = True
            blinking = True
            blink_timer = pygame.time.get_ticks()
    elif blinking:
        # Мерцание перед исчезновением
        now = pygame.time.get_ticks()
        if now - blink_timer > 100:  # каждые 100 мс
            show_sprite = not show_sprite
            blink_timer = now
            blink_counter += 1

        if show_sprite:
            screen.blit(frames[-1], (WIDTH // 2 - 48, HEIGHT // 2 - 48))

        if blink_counter > 6:  # 3 раза мигает
            blinking = False
            show_death_text = True
            death_text_timer = pygame.time.get_ticks()
    elif show_death_text:
        # Показываем финальный текст
        time_since = pygame.time.get_ticks() - death_text_timer
        if time_since > 400:
            text_surface = font.render("WANTED", True, RED)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
