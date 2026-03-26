import math
import pygame

class	Point(pygame.sprite.Sprite) :
	def __init__(self) :
		super().__init__()
		self.width = 40
		self.height = 10
		self.image = pygame.Surface((40, 10))
		self.image.fill((255, 0, 0))
		self.rect = self.image.get_rect()
		self.font = pygame.font.SysFont()

class	Ball(pygame.sprite.Sprite) :
	def __init__(self) :
		super().__init__()
		self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
		pygame.draw.circle(self.image, (255,0,0), (5,5), 5)
		self.rect = self.image.get_rect()
		self.rect.center = ((300, 400))
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
	
	def	bounce(self, spr : pygame.sprite.Sprite) :
		self.speed.y *= -1
		hitpoint = (self.center_pos.x - spr.center_pos_x) / 50
		self.speed.x = hitpoint * 10
		self.speed = self.speed.normalize() * 10

class	Platform(pygame.sprite.Sprite) :
	SPEED = 10
	def __init__(self) :
		super().__init__()
		self.image = pygame.Surface((100, 10))
		self.image.fill((255,255,255))
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
	def __init__(self, topleft, color) :
		super().__init__()
		self.image = pygame.Surface((60,30))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		pygame.draw.rect(self.image, color, self.rect, 2)
		self.rect.topleft = topleft
		self.center_pos_x = self.rect.centerx

	
# init library
pygame.init()

# init display
win = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Bricky")

# init clock
clock = pygame.time.Clock()
FPS = 60

# init sprites 
platform = Platform()
ball = Ball()

# init bricks 
bricks = []
red = 0
green = 242
blue = 289
for y in range(0, 5) :
	red += 48
	blue -= 48
	color = (red, green, blue)
	for x in range(0,11) :
		bricks.append(Brick((x * 60, y * 30), color))
bricks_sprites = pygame.sprite.Group()
bricks_sprites.add(bricks)

all_sprites = pygame.sprite.Group()
all_sprites.add(platform, ball, bricks)

# game loop 
running = True
while running :
	# set sprites
	win.fill((0, 0, 0))
	running = ball.move()

	# handle collisions
	if ball.rect.colliderect(platform.rect) :
		ball.bounce(platform)

	hitbrick = pygame.sprite.spritecollide(ball, bricks_sprites, True)
	if  hitbrick :
		ball.bounce(hitbrick[0])

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
			exit()

