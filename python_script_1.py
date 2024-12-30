import math
import pygame
import random
import time

pygame.init()

# Constants
height, width = 600, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aim Trainer")

targetIncrement = 400
targetEvent = pygame.USEREVENT
targetPadding = 30
backgroundColor = (0, 25, 40)
lives = 3
labelFont = pygame.font.SysFont("comicsans", 24)

class Target:
    maxRadius = 30
    growthRate = 0.2
    color = "red"
    secondColor = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.growing = True

    def update(self):
        if self.growing:
            self.size += self.growthRate
            if self.size >= self.maxRadius:
                self.growing = False
        else:
            self.size -= self.growthRate

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), int(self.size))
        pygame.draw.circle(win, self.secondColor, (self.x, self.y), int(self.size * 0.8))
        pygame.draw.circle(win, self.color, (self.x, self.y), int(self.size * 0.6))
        pygame.draw.circle(win, self.secondColor, (self.x, self.y), int(self.size * 0.4))

    def collide(self, x, y):
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return distance <= self.size

def draw(win, targets):
    win.fill(backgroundColor)
    for target in targets:
        target.draw(win)

def formatTime(secs):
    milliseconds = int((secs % 1) * 1000 // 100)
    seconds = int(secs) % 60
    minutes = int(secs) // 60
    return f"{minutes:02d}:{seconds:02d}.{milliseconds}"

def topBar(win, elapsedTime, hits, misses):
    pygame.draw.rect(win, "grey", (0, 0, width, 50))
    
    timeLabel = labelFont.render(f"Time: {formatTime(elapsedTime)}", True, "black")
    speed = round(hits / elapsedTime, 1) if elapsedTime > 0 else 0
    speedLabel = labelFont.render(f"Speed: {speed} t/s", True, "black")
    hitsLabel = labelFont.render(f"Hits: {hits}", True, "black")
    livesLabel = labelFont.render(f"Lives: {lives - misses}", True, "black")

    win.blit(timeLabel, (5, 5))
    win.blit(speedLabel, (200, 5))
    win.blit(hitsLabel, (450, 5))
    win.blit(livesLabel, (650, 5))

def endScreen(win, elapsedTime, hits, clicks):
    accuracy = round(hits / clicks * 100, 1) if clicks > 0 else 0
    labels = [
        f"Time: {formatTime(elapsedTime)}",
        f"Speed: {round(hits / elapsedTime, 1) if elapsedTime > 0 else 0} t/s",
        f"Hits: {hits}",
        f"Accuracy: {accuracy}%",
    ]

    win.fill("white")
    for i, text in enumerate(labels):
        label = labelFont.render(text, True, "black")
        win.blit(label, ((width - label.get_width()) // 2, 100 + i * 50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return

def main():
    run = True
    targets = []
    pygame.time.set_timer(targetEvent, targetIncrement)
    clock = pygame.time.Clock()
    hits, clicks, misses = 0, 0, 0
    startTime = time.time()

    while run:
        clock.tick(60)
        pos = pygame.mouse.get_pos()
        click = False
        elapsedTime = time.time() - startTime

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == targetEvent:
                x = random.randint(targetPadding, width - targetPadding)
                y = random.randint(targetPadding + 50, height - targetPadding)
                targets.append(Target(x, y))
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        clickHandled = False  # Tracks if a target was hit during this click

        for target in targets[:]:  # Use a copy of the list to safely remove elements
            target.update()
            if target.size <= 0:
                targets.remove(target)
            elif click and not clickHandled and target.collide(*pos):
                targets.remove(target)
                hits += 1
                clickHandled = True  # Ensure only one target registers per click

        if click and not clickHandled:
            misses += 1  # Increment misses only if no target was hit

        if misses >= lives:
            endScreen(win, elapsedTime, hits, clicks)
            run = False

        draw(win, targets)
        topBar(win, elapsedTime, hits, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
