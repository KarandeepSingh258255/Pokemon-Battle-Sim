import math

class Pokemon:
    def __init__(self, name, hp, attack, defense, speed, moves=None, types=None):
        self.name = name.title()
        self.level = 50
        self.max_hp = math.floor((2 * hp * self.level) / 100) + self.level + 10 
        self.hp = self.max_hp
        self.attack = math.floor((2 *attack * self.level) / 100) + self.level + 5
        self.defense = math.floor((2 * defense * self.level) / 100) + self.level + 5 
        self.speed = math.floor((2 * speed * self.level) / 100) + self.level + 5
        self.moves = moves if moves else []
        self.types = types if types else []
        self.status = None
        self.sleep_turns = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def set_status(self, status):
        if self.status:
            return False

        self.status = status
        if status == "asleep":
            self.sleep_turns = 2

        return True
    
