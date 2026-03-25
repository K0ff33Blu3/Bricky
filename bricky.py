import math
import pygame

class	Ball(pygame.sprite.Sprite) :
	def __init__(self) :
		super().__init__()
		self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
		pygame.draw.circle(self.image, (0,0,0), (5,5), 5)
		self.rect = self.image.get_rect()
		self.rect.center = ((300, 10))
		self.center_pos= pygame.math.Vector2(self.rect.center)
		self.speed = pygame.math.Vector2(0, 10)

	
	def move(self) -> bool :
		self.center_pos += self.speed
		self.rect.centerx = int(self.center_pos.x)
		self.rect.centery = int(self.center_pos.y)
	
		if self.rect.left <= 0 or self.rect.right >= 600 :
			self.speed.x *= -1
			self.speed = self.speed.normalize() * 10
		if self.rect.top <= 0 :
			self.speed.y *= -1
			self.speed = self.speed.normalize() * 10
		return self.rect.bottom < 800

class	Platform(pygame.sprite.Sprite) :
	SPEED = 10
	def __init__(self) :
		super().__init__()
		self.image = pygame.Surface((100, 10))
		self.image.fill((0,0,0))
		self.rect = self.image.get_rect()
		self.rect.center = ((300, 700))
		self.center_pos_x = self.rect.centerx
	
	def move_left(self) :
		if self.center_pos_x == 0 :
			return
		self.center_pos_x -= self.SPEED
		self.rect.centerx = int(self.center_pos_x)

	def move_right(self) :
		if self.center_pos_x == 600 :
			return
		self.center_pos_x += self.SPEED
		self.rect.centerx = int(self.center_pos_x)

class	Brick(pygame.sprite.Sprite) :
	def __init__(self, topleft) :
		super().__init__()
		self.image = pygame.Surface((60,30))
		self.image.fill((148, 251, 171))
		self.rect = self.image.get_rect()
		pygame.draw.rect(self.image, (0,0,0), self.rect, 2)
		self.rect.topleft = topleft
	
# init library
pygame.init()

# init display
win = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Bricky")
win.fill((232, 174, 183))

# init clock
clock = pygame.time.Clock()
FPS = 60

# init sprites 
platform = Platform()
ball = Ball()
all_sprites = pygame.sprite.Group()
all_sprites.add(platform, ball)
# init bricks 
bricks = []


# game loop 
running = True
while running :
	# set sprites
	win.fill((232, 174, 183))
	running = ball.move()

	# handle collisions
	if ball.rect.colliderect(platform.rect) :
		ball.speed.y *= -1
		hitpoint = (ball.center_pos.x - platform.center_pos_x) / 50
		ball.speed.x = hitpoint * 10

	all_sprites.draw(win)
	pygame.display.flip()

	# set dt --- time between frames 
	dt = clock.get_time()
	clock.tick(FPS) # fixes FPS

	# polling
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] :
		platform.move_left()
	elif keys[pygame.K_RIGHT] :
		platform.move_right()

	# events --- used only to quit
	for event in pygame.event.get() :
		if event.type == pygame.QUIT :
			running = False