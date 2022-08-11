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
HEIGHT = 1080
WINDOW_SIZE = "1004x1080"
TITLE = "Hunt: Showdown Bingo"
BG_COLOR = "white"
MARKER_COLOR = "yellow" 
BINGO_COLOR = "red"

class SelectWindowSizeScreen(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Need to call the tkinter constructor
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("300x250") 
        self.title(TITLE)      
        LABEL_FONT = font.Font(size=16)
        OTHER_FONT = font.Font(size=12)
  
        label = tk.Label(text="Select a window size")
        label.pack()
        label['font'] = LABEL_FONT

        self.var = tk.IntVar(None, 1000)
        r1 = tk.Radiobutton(text="500x500", variable=self.var, value=500)
        r1.pack()
        r1['font'] = OTHER_FONT

        r2 = tk.Radiobutton(text="600x600", variable=self.var, value=600)
        r2.pack()
        r2['font'] = OTHER_FONT

        r3 = tk.Radiobutton(text="750x750", variable=self.var, value=750)
        r3.pack()
        r3['font'] = OTHER_FONT

        r4 = tk.Radiobutton(text="1000x1000", variable=self.var, value=1000)
        r4.pack()
        r4['font'] = OTHER_FONT

        r5 = tk.Radiobutton(text="1500x1500", variable=self.var, value=1500)
        r5.pack()
        r5['font'] = OTHER_FONT

        btn = tk.Button(text="Okay", height=2, command=self.set_window_size)
        btn.pack()
        btn['font'] = OTHER_FONT

    def set_window_size(self):
        global WIDTH, HEIGHT
        WIDTH = self.var.get() + 4
        HEIGHT = self.var.get() + 80
        self.destroy()




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
        self.card_width = WIDTH - 4
        self.card_height = HEIGHT - 80

        # Calculate width and height of tile and thickness of purple borders
        self.border_thickness = (self.card_width * (1 / 6)) / 6
        self.tile_width = (self.card_width * (5 / 6)) / 5
        self.tile_height = self.tile_width

        # print("Border thickness is", self.border_thickness)
        # print("Tile width is", self.tile_width)

        # Restrict the size of the GUI so we don't have resize issues
        self.minsize(WIDTH, HEIGHT)
        self.maxsize(WIDTH, HEIGHT)

        # When mouse 1 (left click) is clicked, run the clicked_on_card function
        self.bind("<Button 1>", self.clicked_on_card)

        # Sets window size and title
        # self.geometry(WINDOW_SIZE) 
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
        self.card = Image.open("./assets/NEWEST_Template.png")        

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


    def clicked_on_card(self, event):
        self.set_mouse_pos(event)

        if (isinstance(event.widget, tk.Canvas)):
            self.mark_card()


    def set_mouse_pos(self, event):
        """
        If the bingo card is clicked on, we determine where the card was clicked on in x and y pixel coordinates. 
        """

        # this variable is the widget that was clicked on
        caller = event.widget

        # Only set mouse_x and mouse_y if the widget clicked on is the label holding the bingo card image
        if (isinstance(caller, tk.Canvas)):
            self.mouse_x = event.x
            self.mouse_y = event.y

            print(self.mouse_x, self.mouse_y)

        
    def draw(self, col, row, color):

        # x1 is the x coordinate for the left side of the tile box
        # x2 is the x coordinate for the right side of the tile box
        # y1 is the y coordinate for the top of the tile box
        # y2 is the y coordinate for the bottom of the tile box
        # (1*col) + 1 and (1*row) + 1 are just there to account for error
        x1 = math.floor((col * self.tile_width) + (col * self.border_thickness) + self.border_thickness)
        y1 = math.floor((row * self.tile_height) + (row * self.border_thickness) + self.border_thickness)
        x2 = (col * self.tile_width) + (col * self.border_thickness) + self.border_thickness + self.tile_width #- (1 * col) + 1
        y2 = (row * self.tile_height) + (row * self.border_thickness) + self.border_thickness + self.tile_height #- (1 * row) + 1

        if (self.marked[col][row]):

            # Draw width is the width of the bingo marker
            # When drawing, we need to move the drawing up/down and left/right by an offset
            draw_width = self.border_thickness / 2
            offset = draw_width / 2

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

            #
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
        row_ = [row_[row] for row_ in self.marked]
        col_ = self.marked[col]

        """Two issues. First, need to check that the column/row has at least 
        4 other marked tiles before we change them back to yellow. if not leave em
        
        Second, we need to make sure we aren't undoing a colored bingo from another
        row / col. So we need to check that as well"""

        diagonal1 = []
        diagonal2 = []
        [diagonal1.append(self.marked[i][4 - i]) for i in range(5)]
        [diagonal2.append(self.marked[i][i]) for i in range(5)]

        # Undoing a column bingo # TODO MAKE SURE WE ARENT FUCKING UP DIAGONAL 
        for r in range(0, 5):

            row_ = [row_[r] for row_ in self.marked]
            if (self.marked[col][r] and not all(row_)):
                if (r == (4 - col)) and all(diagonal1):
                    continue
                if (r == col and all(diagonal2)):
                    continue

                self.canvas.delete(f"col{col}row{r}")
                self.draw(col, r, MARKER_COLOR)
        
        # Undoing a row bingo
        for c in range(0, 5):

            col_ = self.marked[c]
            if (self.marked[c][row] and not all(col_)):
                if (c == (4 - row)) and all(diagonal1):
                    continue
                if (c == row and all(diagonal2)):
                    continue
                self.canvas.delete(f"col{c}row{row}")
                self.draw(c, row, MARKER_COLOR)

        # Undoing a diagonal bingo (diagonal2); top left to bottom right
        # Only need to check this if column and row of tile are the same
        if (col == row):
            for i in range(5):
                col_ = self.marked[i]
                row_ = [row_[i] for row_ in self.marked]
                if (self.marked[i][i] and not all(row_) and not all(col_)):
                    if (i == 2 and all(diagonal1)):
                        continue
                    self.canvas.delete(f"col{i}row{i}")
                    self.draw(i, i, MARKER_COLOR)

        # Undoing a diagonal bingo (diagonal1); bottom left to top right
        if (row + col == 4):
            for i in range(5):
                col_ = self.marked[i]
                row_ = [row_[4 - i] for row_ in self.marked]
                if (self.marked[i][4 - i] and not all(row_) and not all(col_)):
                    if (i == 2 and all(diagonal2)):
                        continue
                    self.canvas.delete(f"col{i}row{4 - i}")
                    self.draw(i, 4 - i, MARKER_COLOR)


    def mark_card(self):
        x = self.mouse_x
        y = self.mouse_y

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
        # If we're unmarking a tile, we need to remove what we drew and check to see if we undid a bingo
        if (self.marked[col][row]):
            self.draw(col, row, MARKER_COLOR)
            self.check_for_bingo(col, row)
        else:
            self.draw(col, row, MARKER_COLOR)
            self.undo_bingo(col, row)

        
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
        card = Image.open('./assets/NEWEST_Template.png', 'r')

        while(row < 5):

            # If row = 2 and col = 2, then we're on the freespace, so we don't need to place a tile
            if (row != 2 or col != 2):

                # Open the ith tile image 
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


if __name__ == "__main__":

    select_win_size = SelectWindowSizeScreen()
    select_win_size.mainloop()
    root = Main()
    root.mainloop()


