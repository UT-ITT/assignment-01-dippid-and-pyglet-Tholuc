import pyglet
from pyglet import shapes, text
import random
import math
from DIPPID import SensorUDP
import os
os.chdir(os.path.dirname(__file__)) # this fixed an issue for testing in Visual Studio Code with Sounds so please comment it out when it causes issues on your specific grading setup

# =========================
# CONFIG
# =========================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

CAT_SIZE = (50, 60)

CAT_SPEED = 8
CAT_DAMPING = 0.80
CAT_MAX_SPEED = 12

INPUT_DEADZONE = 0.1
DIRECTION_IMPACT = 0.35

DOG_BASESPEED = 2.5


# =========================
# WINDOW
# =========================
win = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Cat, Mouse & Dog")
pyglet.gl.glClearColor(0.08, 0.10, 0.16, 1)

sensor = SensorUDP(5700)

# =========================
# SOUNDS
# =========================

dogspawn_sound = pyglet.media.load("wuffwuff.wav", streaming=False)
cat_eat_sound = pyglet.media.load("meow.wav", streaming=False)

# =========================
# GAME STATE
# =========================
velocity_x = 0
velocity_y = 0

score = 0
highscore = 0

# =========================
# LABEL
# =========================
score_label = text.Label(
    "Score: 0  Highscore: 0",
    x=10,
    y=WINDOW_HEIGHT - 30,
    font_size=18,
    color=(230, 230, 230, 255),
)

# =========================
# CREATE FUNCTIONS
# =========================
def create_cat(x, y):
    return [
        # body
        shapes.Rectangle(x, y, 50, 40, color=(255, 150, 80)),
        # ears 
        shapes.Triangle(x, y + 40, x + 10, y + 60, x + 20, y + 40, 
                         color=(255, 150, 80)),
        shapes.Triangle(x + 30, y + 40, x + 40, y + 60, x + 50, y + 40,
                         color=(255, 150, 80)),
        # eyes
        shapes.Circle(x + 15, y + 25, 3, color=(0, 0, 0)),
        shapes.Circle(x + 35, y + 25, 3, color=(0, 0, 0)),
        # mouth
        shapes.Rectangle(x + 20, y + 10, 10, 2, color=(0, 0, 0)),
    ]


def create_mouse(x, y):
    return [
        # body
        shapes.Circle(x, y, 15, color=(190, 195, 205)),
        # ears
        shapes.Circle(x - 10, y + 10, 5, color=(190, 195, 205)),
        shapes.Circle(x + 10, y + 10, 5, color=(190, 195, 205)),
        # eyes
        shapes.Circle(x - 5, y + 3, 2, color=(0, 0, 0)),
        shapes.Circle(x + 5, y + 3, 2, color=(0, 0, 0)),
        # mouth
        shapes.Circle(x, y - 6, 2, color=(0, 0, 0)),
    ]


def create_dog(x, y):
    return [
        # body
        shapes.Circle(x, y, 25, color=(130, 90, 60)),
        # ears
        shapes.Circle(x - 18, y + 18, 10, color=(110, 70, 45)),
        shapes.Circle(x + 18, y + 18, 10, color=(110, 70, 45)),
        # eyes 
        shapes.Circle(x - 8, y + 3, 3, color=(0, 0, 0)),
        shapes.Circle(x + 8, y + 3, 3, color=(0, 0, 0)),
        # cute little nose
        shapes.Circle(x, y - 5, 4, color=(30, 20, 20)),
        # mouth
        shapes.Rectangle(x - 10, y - 12, 20, 2, color=(30, 10, 10)),
    ]


# =========================
# SPAWN FUNCTIONS
# =========================
def spawn_mouse():
    x = random.randint(50, WINDOW_WIDTH - 50)
    y = random.randint(50, WINDOW_HEIGHT - 50)
    return create_mouse(x, y)


# =========================
# GAME OBJECTS
# =========================
cat = create_cat(400, 300)
mouse = spawn_mouse()
dog = create_dog(100, 100)
dogspawn_sound.play()

# =========================
# RESET
# =========================
def reset_game():
    global score, velocity_x, velocity_y, mouse, dog

    score = 0
    velocity_x = 0
    velocity_y = 0

    cat[:] = create_cat(400, 300)
    mouse = spawn_mouse()
    dog = create_dog(100, 100)
    dogspawn_sound.play()
    update_score_label()


# =========================
# SCORE
# =========================
def update_score_label():
    score_label.text = f"Score: {score}  Highscore: {highscore}"


# =========================
# COLLISIONS
# =========================

# simple distance function, im only approximating here which i think is enough
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def check_mouse_collision():
    cat_body = cat[0]
    mouse_body = mouse[0]

    return distance(
        cat_body.x + 25,
        cat_body.y + 20,
        mouse_body.x,
        mouse_body.y,
    ) < 40


def check_dog_collision():
    cat_body = cat[0]
    dog_body = dog[0]

    return distance(
        cat_body.x + 25,
        cat_body.y + 20,
        dog_body.x,
        dog_body.y,
    ) < 45


# =========================
# UPDATE
# =========================
def update(dt):
    global velocity_x, velocity_y, score, highscore, mouse, dog

    data = sensor.get_value("accelerometer")

    if data:
        # ax/y = x and y directions from DIPPID, also we swap x and y because that worked better on my phone since i could hold it horizontally
        # raw ax/y is just without the deadzone
        
        ax_raw = data["y"]
        ay_raw = data["x"]

        ax = ax_raw * CAT_SPEED if abs(ax_raw) > INPUT_DEADZONE else 0
        ay = ay_raw * CAT_SPEED if abs(ay_raw) > INPUT_DEADZONE else 0


        velocity_x = velocity_x * CAT_DAMPING + ax * DIRECTION_IMPACT
        velocity_y = velocity_y * CAT_DAMPING + ay * DIRECTION_IMPACT
        

        velocity_x = max(-CAT_MAX_SPEED, min(CAT_MAX_SPEED, velocity_x))
        velocity_y = max(-CAT_MAX_SPEED, min(CAT_MAX_SPEED, velocity_y))
    
    # move cat
    for part in cat:
        part.x += velocity_x
        part.y += velocity_y

    # keep cat in bounds
    cat_body = cat[0]

    new_x = max(0, min(WINDOW_WIDTH - CAT_SIZE[0], cat_body.x))
    new_y = max(0, min(WINDOW_HEIGHT - CAT_SIZE[1], cat_body.y))

    # dx/y x and y directions when including the rebounding which is different from ax/y
    dx = new_x - cat_body.x
    dy = new_y - cat_body.y

    for part in cat:
        part.x += dx
        part.y += dy

    # dog AI is chasing cat very simply
    dog_body = dog[0]

    # direction from dog to cat
    dx = cat_body.x - dog_body.x
    dy = cat_body.y - dog_body.y
    dist = math.sqrt(dx * dx + dy * dy)


    # normalize distance and apply speed
    if dist > 1: # here to protect from division by zero
        dog_body.x += (dx / dist) * (DOG_BASESPEED + score / 10)
        dog_body.y += (dy / dist) * (DOG_BASESPEED + score / 10)

        dog[:] = create_dog(dog_body.x, dog_body.y)

    # mouse collision
    if check_mouse_collision():
        score += 1
        mouse = spawn_mouse()
        cat_eat_sound.play()
        update_score_label()

    # dog collision
    if check_dog_collision():
        highscore = max(highscore, score)
        reset_game()


# =========================
# DRAW
# =========================
@win.event
def on_draw():
    win.clear()

    for part in cat:
        part.draw()

    for part in mouse:
        part.draw()

    for part in dog:
        part.draw()

    score_label.draw()

@win.event
def on_close():
    os._exit(0)

# =========================
# RUN
# =========================
pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()