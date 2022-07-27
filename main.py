from PIL import Image, ImageTk
from os import walk
import random
import tkinter as tk
from tkinter.filedialog import asksaveasfile

WINDOW_SIZE = "1600x1200"
TITLE = "Hunt: Showdown Bingo"

class Main(tk.Tk):
    def __init__(self, *args, **kwargs):

        # Need to call the tkinter constructor
        tk.Tk.__init__(self, *args, **kwargs)

        # These variables track the x and y position of where the user clicks on the bingo card
        self.mouse_x = None
        self.mouse_y = None

        # When mouse 1 (left click) is clicked, run the get_mouse_pos function
        self.bind("<Button 1>", self.get_mouse_pos)

        # Sets window size and title
        self.geometry(WINDOW_SIZE) 
        self.title(TITLE)         

        # Button to generate a new bingo card
        new_card_btn = tk.Button(text="New Card", command=self.get_new_bingo_card).pack()

        # Button to save a bingo card
        save_card_btn = tk.Button(text="Save Card", command=self.save_card).pack()


        self.card = Image.open("./assets/card.png") # The current bingo card as an Image object
        self.card_copy = self.card.copy()           # A copy of the current bingo card. Needed for resizing 
        self.card = self.card.resize((1000, 994))   # Resize bingo card according to the current window size

        self.tk_img = ImageTk.PhotoImage(self.card) # A tk version of the image is needed to embed it in the GUI
        self.label1 = tk.Label(image=self.tk_img, width=1000, height=994, text="card")
        self.label1.image = self.tk_img

        # https://stackoverflow.com/questions/3482081/how-to-update-the-image-of-a-tkinter-label-widget
        self.label1.bind('<Configure>', self._resize_image) # Call self._resize_image function whenever the label changes size
        self.label1.pack()
    

    def _resize_image(self, event):
        """
        Whenever the user resizes the GUI, we also need to resize the bingo card image that's
        displayed. This function resizes the bingo card image and then redisplays it in the
        GUI. The _resize_image function is bound to the label containing the bingo card image,
        so whenever the label resizes, this function will execute. For simplicity, the width and
        height of the label and the width and height of the bingo card image are the same.

        When resizing the bingo card, we need to resize the original version of the image. If we keep
        resizing something that's already been resized multiple times, we lose image quality. That's
        why we resize the copy of the card instead of the card itself.

        See: https://stackoverflow.com/questions/24061099/tkinter-resize-background-image-to-window-size
        """
        new_width = event.width 
        new_height = event.height

        self.card = self.card_copy.resize((new_width, new_height)) # resize the bingo card

        self.tk_img = ImageTk.PhotoImage(self.card)
        self.label1.configure(image=self.tk_img) # set the 
        self.label1.image = self.tk_img


    def save_card(self):
        """
        Saves the bingo card as a .png file.
        """
        file = asksaveasfile(mode='wb', defaultextension=".png", filetypes=[("PNG file", "*.png")]) # opens a dialogue box
        if file:
            self.card.save(file) # saves the image


    def get_mouse_pos(self, event):
        """
        If the bingo card is clicked on, we determine where the card was clicked on in x and y pixel coordinates. 
        """

        # this variable is the widget that was clicked on
        caller = event.widget

        # Only set mouse_x and mouse_y if the widget clicked on is the label holding the bingo card image
        if (isinstance(caller, tk.Label) and caller.cget("text") == "card"):
            self.mouse_x = event.x
            self.mouse_y = event.y

            print(self.mouse_x, self.mouse_y)
         
        
    def get_new_bingo_card(self):

        # The relative path to where the tile images are stored
        tilepath = "./assets/tiles"

        # Walks through the tilepath directory and 
        # Shamefully stolen from https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
        tiles = next(walk(tilepath), (None, None, []))[2]  # [] if no file

        # Make sure that there are at least 24 tiles in the assets/tiles directory
        if (len(tiles) < 24):
            tk.messagebox.showinfo("Error", "You need at least 24 tiles to make a bingo card you braindead ape. If you're seeing this, it means the assets/tiles folder has less than 24 tiles in it.")
            return

        # Randomly shuffle the tiles. We'll use the first 24 tiles in the bingo card
        random.shuffle(tiles)

        # In the 3062x3043 version of the bingo card, each tile is 549x546 and the purple borders are 53 pixels thick
        tile_width = 549
        tile_height = 546
        border_width = 53

        # x and y coordinates on the bingo card
        x = 53
        y = 53

        # row and column on the bingo card
        row = 0
        col = 0

        # keeps track of the ith tile on the bingo card
        i = 0

        # open the blank bingo card using Pillow
        card = Image.open('./assets/card.png', 'r')

        while(row < 5):

            # If row = 2 and col = 2, then we're on the freespace, so we don't need to place a tile
            if (row != 2 or col != 2):

                # Open the ith tile image 
                tile = Image.open(f'./assets/tiles/{tiles[i]}', 'r') 

                # Convert to RGBA because we need to keep track of alpha/transparency values
                # See: https://stackoverflow.com/questions/57948254/transparet-pixels-are-being-pasted-as-black-in-pil
                tile = tile.convert("RGBA") 

                # Superimpose tile onto bingo card
                card.paste(tile, (x, y), tile) 

                i += 1

            # Increment the x value to move to the next tile in the bingo card
            x += tile_width + border_width 

            # We only increment the y value whenever we get to the last column in the bingo card
            if (col == 4):
                col = 0
                row += 1
                x = 53
                y += tile_height + border_width
            else:
                col += 1
        
        # Once card is completed, set the member variables
        self.card = card
        self.card_copy = self.card.copy()

        resized_card = card.resize((1000, 994))
        self.tk_img = ImageTk.PhotoImage(resized_card)

        # Updates the label with the new image
        # See: https://stackoverflow.com/questions/3482081/how-to-update-the-image-of-a-tkinter-label-widget
        self.label1.configure(image=self.tk_img)

        
if __name__ == "__main__":
    root = Main()
    root.mainloop()


