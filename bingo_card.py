from PIL import Image, ImageTk
from os import walk
import random
import tkinter as tk
from tkinter.filedialog import asksaveasfile
import math


# Color of marker placed on bingo card
MARKER_COLOR = "yellow" 

# Color of marker when it's involved in a bingo
BINGO_COLOR = "red"

class BingoCard():
    def __init__(self, width, height, master):
        
        # Width and height of the bingo card
        self.card_width = width
        self.card_height = height

        # Calculate width and height of tile and thickness of purple borders
        self.border_thickness = (self.card_width * (1 / 6)) / 6
        self.tile_width = (self.card_width * (5 / 6)) / 5
        self.tile_height = self.tile_width

        # The current bingo card as an Image object; resize to the desired image size
        self.card = Image.open("./assets/card.png")
        self.card = self.card.resize((self.card_width, self.card_height))

        # A tk version of the image is needed to embed it in the GUI
        self.tk_img = ImageTk.PhotoImage(self.card) 

        # Embed the image in a canvas, and make the canvas the same size as the bingo card
        # Note: The canvas will automatically make itself a few pixels larger in this case.
        # That's partially why we set the window size larger than the card size
        self.canvas = tk.Canvas(master, width=self.card_width, height=self.card_height)
        # self.canvas.grid(row=2, columnspan=4)
        self.canvas.create_image(0,0, image=self.tk_img, anchor='nw')

        # 2D array to keep track of which tiles are marked
        self.marked = [[False for x in range(5)] for y in range(5)] 


    def hide_card(self):
        self.canvas.grid_forget()


    def show_card(self):
        self.canvas.grid(row=1, columnspan=4)
      

    def save_card(self):
        """
        Saves the bingo card as a .png file.
        """
        file = asksaveasfile(mode='wb', defaultextension=".png", filetypes=[("PNG file", "*.png")]) # opens a dialogue box
        if file:
            self.card.save(file) # saves the image


    def clear_bingo_card(self):
        self.canvas.delete("marker")
        self.marked = [[False for x in range(5)] for y in range(5)] 


    def get_new_bingo_card(self):

        msg_box = tk.messagebox.askquestion ('', 'Create a new card?')
        if msg_box == 'no':
            return

        duplicates = False
        msg_box = tk.messagebox.askquestion ('', 'Allow duplicate tiles in the bingo card?')

        if msg_box == 'yes':
            duplicates = True

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

        # In the 3000x3000 version of the bingo card, each tile is 500x500 and the purple borders are 83.333 pixels thick
        tile_width = 500
        tile_height = 500
        border_thickness = 83.33333

        # x and y coordinates on the bingo card
        x = 83.33333
        y = 83.3333

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
                if duplicates:
                    tile = Image.open(f'./assets/tiles/{random.choice(tiles)}', 'r') 
                else:
                    tile = Image.open(f'./assets/tiles/{tiles[i]}', 'r') 

                # Convert to RGBA because we need to keep track of alpha/transparency values
                # See: https://stackoverflow.com/questions/57948254/transparet-pixels-are-being-pasted-as-black-in-pil
                tile = tile.convert("RGBA") 

                # Superimpose tile onto bingo card
                card.paste(tile, (round(x), round(y)), tile)

                i += 1

            # Increment the x value to move to the next tile in the bingo card
            x += tile_width + border_thickness 

            # We only increment the y value whenever we get to the last column in the bingo card
            if (col == 4):
                col = 0
                row += 1
                x = 83.333333
                y += tile_height + border_thickness
            else:
                col += 1
        
        # Once card is completed, set the member variables
        self.card = card
        # self.card_copy = self.card.copy()

        resized_card = card.resize((self.card_width, self.card_height))
        self.tk_img = ImageTk.PhotoImage(resized_card)

        self.canvas.create_image(0,0, image=self.tk_img, anchor='nw')
        self.marked = [[False for x in range(5)] for y in range(5)] 


    def draw(self, col, row, color):

        # x1 is the x coordinate for the left side of the tile box
        # x2 is the x coordinate for the right side of the tile box
        # y1 is the y coordinate for the top of the tile box
        # y2 is the y coordinate for the bottom of the tile box
        x1 = math.floor((col * self.tile_width) + (col * self.border_thickness) + self.border_thickness)
        y1 = math.floor((row * self.tile_height) + (row * self.border_thickness) + self.border_thickness)
        x2 = (col * self.tile_width) + (col * self.border_thickness) + self.border_thickness + self.tile_width 
        y2 = (row * self.tile_height) + (row * self.border_thickness) + self.border_thickness + self.tile_height 

        # If the tile is to be marked, we draw on the canvas. 
        # Else we'll remove the bingo marker
        if (self.marked[col][row]):

            # Draw width is the width of the bingo marker
            # When drawing, we need to move the drawing up/down and left/right by an offset
            draw_width = self.border_thickness / 2
            offset = draw_width / 2

            # Note: A bunch of geometry was done to determine where exactly we needed to draw
            # things. 

            ### draws the square
            self.canvas.create_line(x1, y1+offset, x2, y1+offset, fill=color, width=draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x2-offset, y1, x2-offset, y2, fill=color, width=draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x2, y2-offset, x1, y2-offset, fill=color, width=draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x1+offset, y2, x1+offset, y1, fill=color, width=draw_width, tags=(f"col{col}row{row}", "marker"))

            ### draws the "x"
            self.canvas.create_line(x1+offset, y1+offset, x2-offset, y2-offset, fill=color, width=draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x2-offset, y1+offset, x1+offset, y2-offset, fill=color, width=draw_width, tags=(f"col{col}row{row}", "marker"))

            ### square black border
            border_draw_width = self.border_thickness / 4
            border_offset = border_draw_width / 2
            self.canvas.create_line(x1, y1+border_offset, x2, y1+border_offset, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x2-border_offset, y1, x2-border_offset, y2, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x2, y2-border_offset, x1, y2-border_offset, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x1+border_offset, y2, x1+border_offset, y1, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            
            ### Inner top triangle black border

            # Middle of the tile
            midpoint_x = (x2 + x1) / 2
            midpoint_y = (y2 + y1) / 2

            mid_width = (draw_width * math.sqrt(2)) / 2

            # Height of the inner triangle
            triangle_height = (midpoint_y - mid_width) - (y1 + draw_width)

            # Distance between the triangles tip and its bottom corners 
            dist = triangle_height * math.sqrt(2)

            # Calculate the x values of the bottom triangle corners
            x3 = (math.sqrt(dist**2 - triangle_height**2) - midpoint_x) * -1
            x4 = (-1 * math.sqrt(dist**2 - triangle_height**2) - midpoint_x) * -1

            # Draw the triangle
            self.canvas.create_line(x3, y1+draw_width, x4, y1+draw_width, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x4, y1+draw_width, midpoint_x, midpoint_y - mid_width, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(midpoint_x, midpoint_y - mid_width, x3, y1+draw_width, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))

            ### Inner bottom triangle black border
            self.canvas.create_line(x3, y2-draw_width, x4, y2-draw_width, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x4, y2-draw_width, midpoint_x, midpoint_y + mid_width, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(midpoint_x, midpoint_y + mid_width, x3, y2-draw_width, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))

            ### Inner left triangle black border
           
            # Height of the inner triangle; not sure if it's the same as before so we recalculate
            triangle_height = (midpoint_x - mid_width) - (x1 + draw_width)

            # Distance between the triangles tip and its bottom corners 
            dist = triangle_height * math.sqrt(2)

            # Calculate the x values of the bottom triangle corners
            y3 = (math.sqrt(dist**2 - triangle_height**2) - midpoint_y) * -1
            y4 = (-1 * math.sqrt(dist**2 - triangle_height**2) - midpoint_y) * -1

            self.canvas.create_line(x1+draw_width, y3, x1+draw_width, y4, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x1+draw_width, y4, midpoint_x - mid_width, midpoint_y, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(midpoint_x - mid_width, midpoint_y, x1+draw_width, y3, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))

            ### Inner right triangle black border
            self.canvas.create_line(x2-draw_width, y3, x2-draw_width, y4, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(x2-draw_width, y4, midpoint_x + mid_width, midpoint_y, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
            self.canvas.create_line(midpoint_x + mid_width, midpoint_y, x2-draw_width, y3, fill="black", width=border_draw_width, tags=(f"col{col}row{row}", "marker"))
        else:
            self.canvas.delete(f"col{col}row{row}")

        
    def check_for_bingo(self, col, row):
        """
        Checks if the currently marked tile causes a bingo.
        If so, all tiles involved in the bingo are removed and
        redrawn using the bingo color.
        """
        row_ = [row_[row] for row_ in self.marked]
        col_ = self.marked[col]

        # Check for a vertical bingo
        if (all(col_)):
            for r in range(0, 5):
                self.canvas.delete(f"col{col}row{r}")
                self.draw(col, r, BINGO_COLOR)
        
        # Check for a horizontal bingo
        if (all(row_)):
            for c in range(0, 5):
                self.canvas.delete(f"col{c}row{row}")
                self.draw(c, row, BINGO_COLOR)

        # Check for diagonal bingo; top left to bottom right
        if (col == row):

            # Check if there's a bingo
            bingo = True
            for i in range(0, 5):
                bingo = bingo and self.marked[i][i]

            # Change color of markers if there's a diagonal bingo
            if (bingo):
                for i in range(0, 5):
                    self.canvas.delete(f"col{i}row{i}")
                    self.draw(i, i, BINGO_COLOR)

        # Check for diagonal bingo; bottom left to top right
        if (row + col == 4):

            # Check if there's a diagonal bingo
            bingo = True
            for i in range(0, 5):
                bingo = bingo and self.marked[i][4 - i]

            # Change color of markers if there's a diagonal bingo
            if (bingo):
                for i in range(0, 5):
                    self.canvas.delete(f"col{i}row{4 - i}")
                    self.draw(i, 4 - i, BINGO_COLOR)


    def undo_bingo(self, col, row):
        """
        Checks if the tile that we're unmarking undoes any bingos. 
        If it does, we remove those tiles and redraw them using the 
        regular marker color.
        """
      
        diagonal1 = [] # Top left to bottom right
        diagonal2 = [] # Bottom left to top right
        [diagonal1.append(self.marked[i][4 - i]) for i in range(5)]
        [diagonal2.append(self.marked[i][i]) for i in range(5)]

        # Checking if we need to undo a column bingo 
        for r in range(0, 5):

            # Grab the row that the current tile is involved in
            row_ = [row_[r] for row_ in self.marked]

            # Check if the tile is marked and that it isn't involved in a bingo in row_
            if (self.marked[col][r] and not all(row_)):

                # Check that the tile isn't involved in a diagonal bingo
                if (r == (4 - col)) and all(diagonal1):
                    continue
                if (r == col and all(diagonal2)):
                    continue

                self.canvas.delete(f"col{col}row{r}")
                self.draw(col, r, MARKER_COLOR)
        
        # Checking if we need to undo a row bingo
        for c in range(0, 5):

            # Grab the column that the current tile is involved in
            col_ = self.marked[c]

            # Check if the tile is marked and that it isn't involved in a bingo in col_
            if (self.marked[c][row] and not all(col_)):

                # Check that the tile isn't involved in a diagonal bingo
                if (c == (4 - row)) and all(diagonal1):
                    continue
                if (c == row and all(diagonal2)):
                    continue
                self.canvas.delete(f"col{c}row{row}")
                self.draw(c, row, MARKER_COLOR)

        # Undoing a diagonal bingo (diagonal2); top left to bottom right
        # Only need to check this if column and row of the removed tile are the same
        if (col == row):
            for i in range(5):

                # Grab row and column that the current tile is involved in
                # We need to make sure we aren't undoing column and row bingos
                # if they exist
                col_ = self.marked[i]
                row_ = [row_[i] for row_ in self.marked]

                # Check that the tile is marked
                # Check that it isn't involved in a row bingo
                # Check that it isn't involved in a column bingo
                if (self.marked[i][i] and not all(row_) and not all(col_)):

                    # Check that it isn't involved in the other diagonal
                    if (i == 2 and all(diagonal1)):
                        continue

                    self.canvas.delete(f"col{i}row{i}")
                    self.draw(i, i, MARKER_COLOR)

        # Undoing a diagonal bingo (diagonal1); bottom left to top right
        if (row + col == 4):
            for i in range(5):

                # Grab row and column that the current tile is involved in
                # We need to make sure we aren't undoing column and row bingos
                # if they exist
                col_ = self.marked[i]
                row_ = [row_[4 - i] for row_ in self.marked]

                # Check that the tile is marked
                # Check that it isn't involved in a row bingo
                # Check that it isn't involved in a column bingo
                if (self.marked[i][4 - i] and not all(row_) and not all(col_)):

                    # Check that it isn't involved in the other diagonal
                    if (i == 2 and all(diagonal2)):
                        continue

                    self.canvas.delete(f"col{i}row{4 - i}")
                    self.draw(i, 4 - i, MARKER_COLOR)

        
    def mark_card(self, mouse_x, mouse_y):
        x = mouse_x
        y = mouse_y

        col = 0
        while True:
            if (x < self.border_thickness): # This means we clicked on a border
                return
            elif (x < self.border_thickness + self.tile_width): # Found the tile we clicked on
                break
            else:
                x = x - (self.tile_width + self.border_thickness) # The tile is further down
                col += 1

        row = 0
        while True:
            if (y < self.border_thickness): # Clicked on a border
                return
            elif (y < self.border_thickness + self.tile_width): # Found the tile we clicked on
                break
            else:
                y = y - (self.tile_width + self.border_thickness)
                row += 1
        
        self.marked[col][row] = not self.marked[col][row]

        # If we're marking a tile, we need to draw on the card and check for a bingo
        if (self.marked[col][row]):
            self.draw(col, row, MARKER_COLOR)
            self.check_for_bingo(col, row)

        # If we're unmarking a tile, we need to remove what we drew and check to see if we undid a bingo
        else:
            self.draw(col, row, MARKER_COLOR)
            self.undo_bingo(col, row)





