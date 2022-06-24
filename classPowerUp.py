# --------------- POWER UPS ------------------------
class PowerUp(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = False
        self.laser = False