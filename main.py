"""
<Insert File Descriptions Here>
"""
from PIL import Image, ImageTk
from os import walk
import random
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfilename
import math
import tkinter.font as font

WIDTH = 1004
HEIGHT = 1070
WINDOW_SIZE = "1004x1070"
TITLE = "Hunt: Showdown Bingo"
BG_COLOR = "black"

class Main(tk.Tk):
    def __init__(self, *args, **kwargs):

        # Need to call the tkinter constructor
        tk.Tk.__init__(self, *args, **kwargs)

        # This needs to be defined IN the class; otherwise Tkinter shits itself
        BUTTON_FONT = font.Font(size=18)

        # These variables track the x and y position of where the user clicks on the bingo card
        self.mouse_x = None
        self.mouse_y = None

        # 2D array to keep track of which tiles are marked
        self.marked = [[False for x in range(5)] for y in range(5)] 

        # Width and height of the bingo card; these dimensions are are arbitrary. The original card was too big.
        self.card_width = 1000
        self.card_height = 994

        # Restrict the size of the GUI so we don't have resize issues
        self.minsize(WIDTH, HEIGHT)
        self.maxsize(WIDTH, HEIGHT)

        # When mouse 1 (left click) is clicked, run the get_mouse_pos function
        self.bind("<Button 1>", self.get_mouse_pos)

        # Sets window size and title
        self.geometry(WINDOW_SIZE) 
        self.title(TITLE)        
        self.configure(bg=BG_COLOR) 

        # Button to generate a new bingo card; sticky=nesw lets the button fill the entire grid
        new_card_btn = tk.Button(text="New Card", height=2, command=self.get_new_bingo_card)
        new_card_btn.grid(row=0, column=0, sticky="nesw")
        new_card_btn['font'] = BUTTON_FONT

        # Button to save a bingo card
        save_card_btn = tk.Button(text="Save Card", command=self.save_card)
        save_card_btn.grid(row=0, column=1, sticky="nesw")
        save_card_btn['font'] = BUTTON_FONT

        # Button to clear the bingo card
        clear_card_btn = tk.Button(text="Clear Card", command=self.clear_bingo_card)
        clear_card_btn.grid(row=0, column=2, sticky="nesw")
        clear_card_btn['font'] = BUTTON_FONT

        # Button to add tiles to the program
        add_tiles_btn = tk.Button(text="Add Tiles", command=self.add_tiles)
        add_tiles_btn.grid(row=0, column=3, sticky="news")
        add_tiles_btn['font'] = BUTTON_FONT

        # The current bingo card as an Image object
        self.card = Image.open("./assets/card.png") 

        # A copy of the current bingo card. Needed for resizing 
        # self.card_copy = self.card.copy()         

        # Resize bingo card according to the current window size
        self.card = self.card.resize((self.card_width, self.card_height))  

        # A tk version of the image is needed to embed it in the GUI
        self.tk_img = ImageTk.PhotoImage(self.card) 
    
        # Embed the image in a canvas, and make the canvas the same size as the bingo card
        self.canvas = tk.Canvas(self, width=self.card_width, height=self.card_height)
        self.canvas.grid(row=1, columnspan=4)
        self.canvas.create_image(0,0, image=self.tk_img, anchor='nw')
    

    def save_card(self):
        """
        Saves the bingo card as a .png file.
        """
        file = asksaveasfile(mode='wb', defaultextension=".png", filetypes=[("PNG file", "*.png")]) # opens a dialogue box
        if file:
            self.card.save(file) # saves the image


    def add_tiles(self):
        file = askopenfilename(defaultextension=".png", filetypes=[("PNG file", "*.png")]) # opens a dialogue box
        if file:
            try:
                fname = file[file.rfind('/')+1:]
                tile = Image.open(file, 'r')
                tile.save(f'./assets/tiles/{fname}')
                
                tk.messagebox.showinfo("Success!", f"{fname} was successfully added.")
            except Exception as e:
                tk.messagebox.showinfo("Error", e)

    
    def clear_bingo_card(self):
        self.canvas.delete("marker")
        self.marked = [[False for x in range(5)] for y in range(5)] 


    def get_mouse_pos(self, event):
        """
        If the bingo card is clicked on, we determine where the card was clicked on in x and y pixel coordinates. 
        """

        # this variable is the widget that was clicked on
        caller = event.widget

        # Only set mouse_x and mouse_y if the widget clicked on is the label holding the bingo card image
        if (isinstance(caller, tk.Canvas)):
            self.mouse_x = event.x
            self.mouse_y = event.y

            self.mark_card()


    def mark_card(self):
        border_thickness = round((self.card_width * 0.10385) / 6)
        tile_width = round((self.card_width - (self.card_width * 0.10385)) / 5)
        tile_height = round((self.card_height - (self.card_height * 0.1045)) / 5)

        col = 0
        x = self.mouse_x
        y = self.mouse_y

        while True:
            if (x < border_thickness):
                print("Clicked on the border!")
                return
            elif (x < border_thickness + tile_width):
                break
            else:
                x = x - (tile_width + border_thickness)
                col += 1

        row = 0
        while True:
            if (y < border_thickness):
                print("Clicked on the border!")
                return
            elif (y < border_thickness + tile_width):
                break
            else:
                y = y - (tile_width + border_thickness)
                row += 1
        
        self.marked[col][row] = not self.marked[col][row]

        draw_width = round(border_thickness / 2)
        x1 = (col * tile_width) + (col * border_thickness) + border_thickness 
        y1 = (row * tile_height) + (row * border_thickness) + border_thickness

        x2 = (col * tile_width) + (col * border_thickness) + border_thickness + tile_width + (1 * col)
        y2 = (row * tile_height) + (row * border_thickness) + border_thickness + tile_height + (1 * row)

        if (self.marked[col][row]):
            self.canvas.create_polygon([x1, y1, x2, y1, (x2 - draw_width), (y1 + draw_width), (x1 + draw_width), (y1 + draw_width)], fill="blue", tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_polygon([x2, y1, x2, y2, (x2 - draw_width), (y2 - draw_width), (x2 - draw_width), (y1 + draw_width)], fill ="blue", tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_polygon([x2, y2, x1, y2, (x1 + draw_width), (y2 - draw_width), (x2 - draw_width), (y2 - draw_width)], fill="blue", tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_polygon([x1, y2, x1, y1, (x1 + draw_width), (y1 + draw_width), (x1 + draw_width), (y2 - draw_width)], fill="blue", tags=(f"col{col}row{row}", "marker"))
        else:
            self.canvas.delete(f"col{col}row{row}")


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
        border_thickness = 53

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
            x += tile_width + border_thickness 

            # We only increment the y value whenever we get to the last column in the bingo card
            if (col == 4):
                col = 0
                row += 1
                x = 53
                y += tile_height + border_thickness
            else:
                col += 1
        
        # Once card is completed, set the member variables
        self.card = card
        self.card_copy = self.card.copy()

        resized_card = card.resize((1000, 994))
        self.tk_img = ImageTk.PhotoImage(resized_card)

        self.canvas.create_image(0,0, image=self.tk_img, anchor='nw')
        self.marked = [[False for x in range(5)] for y in range(5)] 


if __name__ == "__main__":
    root = Main()
    root.mainloop()


