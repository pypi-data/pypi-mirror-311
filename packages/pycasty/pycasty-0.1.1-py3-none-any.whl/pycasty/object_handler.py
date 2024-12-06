from .sprite_object import *
import pkg_resources

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = pkg_resources.resource_filename(__name__,'resources/sprites/static_sprites/')
        self.anim_sprite_path = pkg_resources.resource_filename(__name__,'resources/sprites/animated_sprites/')
        add_sprite = self.add_sprite

        # sprite map
        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))




# from .sprite_object import *

# class ObjectHandler:
#     def __init__(self, game):
#         self.game = game
#         self.sprite_list = []
#         self.static_sprite_path = 'resources/sprites/static_sprites/'
#         self.anim_sprite_path = 'resources/sprites/animated_sprites/'
#         add_sprite = self.add_sprite

#         # sprite map
#         add_sprite(SpriteObject(game))
#         add_sprite(AnimatedSprite(game))


