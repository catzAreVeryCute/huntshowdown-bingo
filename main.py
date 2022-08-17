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
import bingo_card
import select_window_size_screen

LARGE_FONT_SIZE = 18
SMALL_FONT_SIZE = 12

"""
The main bingo application
"""
class Main(tk.Tk):
    def __init__(self, *args, **kwargs):

        # Need to call the tkinter constructor
        tk.Tk.__init__(self, *args, **kwargs)

        # This needs to be defined IN the class; otherwise Tkinter shits itself
        large_button_font = font.Font(size=LARGE_FONT_SIZE)
        self.small_button_font = font.Font(size=SMALL_FONT_SIZE)

        # These variables track the x and y position of where the user clicks on the bingo card
        self.mouse_x = None
        self.mouse_y = None

        # Width and height of the bingo card
        self.card_width = select_window_size_screen.WIDTH - 4
        self.card_height = select_window_size_screen.HEIGHT - select_window_size_screen.HEIGHT_OFFSET

        # Restrict the size of the GUI so we don't have resize issues
        self.minsize(select_window_size_screen.WIDTH, select_window_size_screen.HEIGHT)
        self.maxsize(select_window_size_screen.WIDTH, select_window_size_screen.HEIGHT)

        # When mouse 1 (left click) is clicked, run the clicked_on_card function
        self.bind("<Button 1>", self.clicked_on_card)

        # Set title, background color, etc.
        self.title(select_window_size_screen.TITLE)        

        # Button to generate a new bingo card; sticky=nesw lets the button fill the entire grid
        new_card_btn = tk.Button(text="New Card", height=2, command=self.get_new_bingo_card)
        new_card_btn.grid(row=0, column=0, sticky="nesw")
        new_card_btn['font'] = large_button_font

        # Button to save a bingo card
        save_card_btn = tk.Button(text="Save Card", command=self.save_card)
        save_card_btn.grid(row=0, column=1, sticky="nesw")
        save_card_btn['font'] = large_button_font

        # Button to clear the bingo card
        clear_card_btn = tk.Button(text="Clear Card", command=self.clear_bingo_card)
        clear_card_btn.grid(row=0, column=2, sticky="nesw")
        clear_card_btn['font'] = large_button_font

        # Button to add tiles to the program
        add_tiles_btn = tk.Button(text="Add Tiles", command=self.add_tiles)
        add_tiles_btn.grid(row=0, column=3, sticky="news")
        add_tiles_btn['font'] = large_button_font

        first = tk.Button(text="1", height=2, command=lambda: self.swap_cards(0))
        first.grid(row=1, column=0, sticky="news")
        first.config(relief=tk.SUNKEN)
        first['font'] = self.small_button_font

        self.bingo_buttons = [first]

        self.add_another_card_btn = tk.Button(text="+", command=self.add_another_card)
        self.add_another_card_btn.grid(row=1, column=1, sticky="news")
        self.add_another_card_btn['font'] = self.small_button_font

        self.bingo_cards = []
        self.bingo_cards.append(bingo_card.BingoCard(self.card_width, self.card_height, self))
        self.bingo_cards[0].show_card()

        self.num_cards = 1
        self.current_card_id = 0


    def add_another_card(self):
        self.num_cards += 1
        self.add_another_card_btn.grid_forget()

        # This needs to be defined locally. If we include self.num_cards directly in the 
        # lambda function, it'll always refer to whatever self.num_cards is currently set
        # to, which isn't what we want
        id_ = self.num_cards - 1

        new_button = tk.Button(text=f"{self.num_cards}", command=lambda: self.swap_cards(id_))
        new_button.grid(row=1, column=self.num_cards - 1, sticky="news")
        new_button['font'] = self.small_button_font
        self.bingo_buttons.append(new_button)

        self.add_another_card_btn.grid(row=1, column=self.num_cards, sticky="news")

        self.bingo_cards.append(bingo_card.BingoCard(self.card_width, self.card_height, self))


    def swap_cards(self, calling_id):
        self.bingo_buttons[self.current_card_id].config(relief=tk.RAISED)
        self.bingo_cards[self.current_card_id].hide_card()

        self.current_card_id = calling_id

        self.bingo_buttons[self.current_card_id].config(relief=tk.SUNKEN)
        self.bingo_cards[self.current_card_id].show_card()


    def save_card(self):
        self.bingo_cards[self.current_card_id].save_card()


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
        self.bingo_cards[self.current_card_id].clear_bingo_card()


    def clicked_on_card(self, event):
        """
        When the user left clicks, we call set_mouse_pos to determine
        the (x, y) coordinates of the click location. If the user clicked on the
        canvas (ie, the bingo card), we call the mark_card function to mark it
        """
        self.set_mouse_pos(event)

        if (isinstance(event.widget, tk.Canvas)):
            self.bingo_cards[self.current_card_id].mark_card(self.mouse_x, self.mouse_y)


    def set_mouse_pos(self, event):
        """
        If the bingo card is clicked on, we determine where the card was clicked on in x and y pixel coordinates. 
        """

        # This variable is the widget that was clicked on
        caller = event.widget

        # Only set mouse_x and mouse_y if the widget clicked on is the label holding the bingo card image
        # This is redundant but whatever
        if (isinstance(caller, tk.Canvas)):
            self.mouse_x = event.x
            self.mouse_y = event.y


    def get_new_bingo_card(self):
        self.bingo_cards[self.current_card_id].get_new_bingo_card()


if __name__ == "__main__":
    select_win_size = select_window_size_screen.SelectWindowSizeScreen()
    select_win_size.mainloop()
    root = Main()
    root.mainloop()


