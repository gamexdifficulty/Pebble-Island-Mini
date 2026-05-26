import random
from data.classes.animation import AnimationEvent
from frostlight_engine import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game

class ParticleManager:
    def __init__(self, game:"Game"):
        self.game = game
        self.particles = []
        
    def update(self):
        for particle in self.particles.copy():
            particle.update()
            if particle.can_be_deleted:
                self.particles.remove(particle)
                
    def draw(self):
        for particle in self.particles:
            particle.draw()
            
    def spawn_particle(self, type, pos, range, vel, ttl):
        particle = Particle(self.game, type, [pos[0]+random.randint(0,range[0]), pos[1]+random.randint(0,range[1])], vel, ttl)
        self.particles.append(particle)
    
class Particle:
    def __init__(self, game:"Game", type, pos, vel, timer):
        self.game = game
        self.type = type
        self.pos = pos
        self.vel = vel
        self.timer = timer
        self.can_be_deleted = False
        
        if self.type == 1:
            self.animation = AnimationEvent(self.game, self.timer, [Sprite("particle_1.png"),Sprite("particle_2.png"),Sprite("particle_3.png")], self.ready_to_delete)
    
    def ready_to_delete(self):
        self.can_be_deleted = True
    
    def update(self):
        self.pos[0] += self.vel[0] * self.game.delta_time
        self.pos[1] += self.vel[1] * self.game.delta_time
        
        if self.type == 1:
            self.pos[0] += math.sin(self.pos[1])*3*self.game.delta_time
        
        if self.type == 1:
            self.animation.update()
    
    def draw(self):
        if self.type == 1:
            self.game.window.render(self.animation.get(), self.pos)