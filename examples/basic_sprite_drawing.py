from pygametools.pygametool import *

pygame.init()
window=pygame.display.set_mode((800,600))

sprites=SpriteManager(sp("resources/example_sheet.png"))
sprites.tile_size=(8,8) # Changing Tile Size.

flower_tile=sprites.get_sprite(0,0)
running=True


while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    window.fill("white")
    window.blit(flower_tile,(0,0))
    pygame.display.update()

pygame.quit()