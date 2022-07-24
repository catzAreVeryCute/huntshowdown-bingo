from PIL import Image
from os import walk
import random





# for i in range(1, 25):
#     random.choice(tiles)


# background = Image.open('./assets/card.png', 'r')
# tile = Image.open('./assets/CainSpotted.png', 'r')

# tile_w, tile_h = tile.size
# bg_w, bg_h = background.size

# # Image.Image.paste(background, tile, (50,45))

# tile = tile.convert("RGBA")
# background.paste(tile, (50, 45), tile)


# # background.show()

# background.save('test.png')



# img = Image.open('/path/to/file', 'r')
# img_w, img_h = img.size
# background = Image.new('RGBA', (1440, 900), (255, 255, 255, 255))
# bg_w, bg_h = background.size
# offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
# background.paste(img, offset)
# background.save('out.png')

def select_tiles():
    pass


if __name__ == "__main__":
    tilepath = "./assets/tiles"
    tiles = next(walk(tilepath), (None, None, []))[2]  # [] if no file

    if (len(tiles) < 24):
        print("You need more tiles to have a bingo card")

    random.shuffle(tiles)
    
    tile_width = 549
    border_width = 53

    x = 53
    y = 53
    row = 0
    col = 0
    i = 0

    background = Image.open('./assets/card.png', 'r')

    print(tiles)
    while(row < 5):

        if (row != 2 or col != 2):
            tile = Image.open(f'./assets/tiles/{tiles[i]}', 'r') # open tile image
            tile = tile.convert("RGBA") # ensure we keep alpha value of pixels
            background.paste(tile, (x, y), tile) # superimpose tile onto bingo card
            i += 1
          
        x += tile_width + border_width # increment x val

        if (col == 4):
            col = 0
            row += 1
            x = 53
            y += tile_width + border_width
        else:
            col += 1
       
    background.show()
        


