import math
import random
import pygame

# Pygame setup
pygame.init()
width, length = 1280, 720
screen = pygame.display.set_mode((width, length))
clock = pygame.time.Clock()
running = True


def sign(x):
    return 1 if x >= 0 else -1


def toPolar(vec):
    magnitude = math.sqrt(vec.x ** 2 + vec.y ** 2)
    angle = (math.atan2(vec.y, vec.x)) * 180 / math.pi
    return pygame.Vector2(magnitude, angle)


def toRect(polar):
    x = math.cos(math.radians(polar.y)) * polar.x
    y = math.sin(math.radians(polar.y)) * polar.x
    return pygame.Vector2(x, y)


vec = pygame.Vector2(-1, -1)

affectionDist = 100
affectionAngle = 120


class dot:
    maxSpeed = 10
    dList = []
    alignStrength = 5.0  # Scaled to 0-100 range
    avoidStrength = 30.0  # Scaled to 0-100 range
    cohesionStrength = 2.0  # Scaled to 0-100 range

    def __init__(self):
        self.pos = pygame.Vector2(random.randint(0, width), random.randint(0, length))
        self.size = 5
        self.vel = pygame.Vector2(random.uniform(-1, 1) * dot.maxSpeed, random.uniform(-1, 1) * dot.maxSpeed)
        self.color = [255, 0, 0]
        dot.dList.append(self)

    def applyVel(self):
        if abs(self.vel.x) > dot.maxSpeed:
            self.vel.x = sign(self.vel.x) * dot.maxSpeed
        if abs(self.vel.y) > dot.maxSpeed:
            self.vel.y = sign(self.vel.y) * dot.maxSpeed
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

    def adjustColor(self):
        polar = toPolar(self.vel)
        angle = polar.y % 360
        self.color = [angle / 360 * 255, 0, 255 - angle / 360 * 255]

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.size)
        sizeFactor = 20 / dot.maxSpeed
        endPoint = pygame.Vector2(self.pos.x + self.vel.x * sizeFactor, self.pos.y + self.vel.y * sizeFactor)
        pygame.draw.line(screen, self.color, self.pos, endPoint, 2)
        self.adjustColor()

    def wallColl(self):
        if self.pos.x > width:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = width
        if self.pos.y > length:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = length

    def interaction(self, dotsInZone):
        # align
        allX = []
        allY = []
        for d in dotsInZone:
            allX.append(d.vel.x)
            allY.append(d.vel.y)
        dirX = sum(allX) / len(allX) if allX else 0
        dirY = sum(allY) / len(allY) if allY else 0
        self.vel.x += dot.alignStrength * dirX / 100.0  # Scale back to 0-1 range
        self.vel.y += dot.alignStrength * dirY / 100.0  # Scale back to 0-1 range

        # avoid
        for d in dotsInZone:
            if d != self:
                dist = self.pos.distance_to(d.pos)
                oppDir = self.pos - d.pos
                if dist != 0:
                    self.vel.x += dot.avoidStrength * oppDir.x / dist / 100.0  # Scale back to 0-1 range
                    self.vel.y += dot.avoidStrength * oppDir.y / dist / 100.0  # Scale back to 0-1 range

        # join (cohesion)
        centerX = []
        centerY = []
        for d in dotsInZone:
            centerX.append(d.pos.x)
            centerY.append(d.pos.y)
        avgX = sum(centerX) / len(centerX) if centerX else 0
        avgY = sum(centerY) / len(centerY) if centerY else 0
        cohesionVector = pygame.Vector2(avgX, avgY) - self.pos
        self.vel.x += dot.cohesionStrength * cohesionVector.x / 100.0  # Scale back to 0-1 range
        self.vel.y += dot.cohesionStrength * cohesionVector.y / 100.0  # Scale back to 0-1 range

        # Limit speed
        maxSpeed = 5
        if self.vel.length() > maxSpeed:
            self.vel.scale_to_length(maxSpeed)

    def checkVision(self):
        dotsInZone = []
        for d in dot.dList:
            dist = math.dist(d.pos, self.pos)
            if dist < affectionDist:
                selfPolar = toPolar(self.vel)
                diffPolar = toPolar(pygame.Vector2(d.pos.x - self.pos.x, d.pos.y - self.pos.y))
                angleDiff = abs(selfPolar.y - diffPolar.y)
                if angleDiff < affectionAngle:
                    # pygame.draw.line(screen, [0, 122, 122], self.pos, d.pos, 1)
                    dotsInZone.append(d)
        if dotsInZone:
            self.interaction(dotsInZone)

    def run(self):
        self.draw()
        self.applyVel()
        self.checkVision()
        self.wallColl()


numDots = 100
for i in range(numDots):
    d = dot()

# Main simulation loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Update and draw dots
    for d in dot.dList:
        d.run()

    # Update display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
