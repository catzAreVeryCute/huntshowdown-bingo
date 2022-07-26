from PIL import Image, ImageTk
from os import walk
import random
import tkinter as tk
from tkinter.filedialog import asksaveasfile

WINDOW_SIZE = "1600x1200"
TITLE = "Hunt: Showdown Bingo"

class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry(WINDOW_SIZE) # sets window size
        self.title(TITLE)          # sets window title

        # button to generate a new bingo card
        new_card_btn = tk.Button(text="New Card", command=self.get_new_bingo_card)
        new_card_btn.pack()

        save_card_btn = tk.Button(text="Save Card", command=self.save_card)
        save_card_btn.pack()

        self.card = Image.open("./assets/card.png") # The current bingo card as an Image object
        self.card_copy = self.card.copy()           # A copy of the current bingo card. Needed for resizing 
        self.card = self.card.resize((1000, 994))   # Resize bingo card according to the current window size

        self.tk_img = ImageTk.PhotoImage(self.card) # A tk version of the image is needed to embed it in the GUI
        self.label1 = tk.Label(image=self.tk_img, width=1000, height=994)
        self.label1.image = self.tk_img
        self.label1.bind('<Configure>', self._resize_image) # Call self._resize_image function whenever the label changes size
        self.label1.pack()
    
    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.card = self.card_copy.resize((new_width, new_height)) # resize the bingo card

        self.tk_img = ImageTk.PhotoImage(self.card)
        self.label1.configure(image=self.tk_img) # set the 
        self.label1.image = self.tk_img

    def save_card(self):
        file = asksaveasfile(mode='wb', defaultextension=".png", filetypes=[("PNG file", "*.png")])
        if file:
            self.card.save(file) # saves the image to the input file name. 
        
    def get_new_bingo_card(self):
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

        card = Image.open('./assets/card.png', 'r')

        while(row < 5):

            if (row != 2 or col != 2):
                tile = Image.open(f'./assets/tiles/{tiles[i]}', 'r') # open tile image
                tile = tile.convert("RGBA") # ensure we keep alpha value of pixels
                card.paste(tile, (x, y), tile) # superimpose tile onto bingo card
                i += 1
            
            x += tile_width + border_width # increment x val

            if (col == 4):
                col = 0
                row += 1
                x = 53
                y += tile_width + border_width
            else:
                col += 1
        
        self.card = card
        self.card_copy = self.card.copy()

        resized_card = card.resize((1000, 994))
        self.tk_img = ImageTk.PhotoImage(resized_card)

        self.label1.configure(image=self.tk_img)

        
if __name__ == "__main__":
    root = Main()
    root.mainloop()


