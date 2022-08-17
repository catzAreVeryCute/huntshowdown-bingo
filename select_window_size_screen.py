import tkinter as tk
import tkinter.font as font


# Default window size of main application
# The class below will set this based on user input
WIDTH = 1004
HEIGHT = 1128

# Height of buttons is 124 pixels; add 4 to give a bit of padding
HEIGHT_OFFSET = 124 + 4

TITLE = "Hunt: Showdown Bingo"

"""
Asks the user to select a window size when the application launches.

In the 500x500, 750x750, and 1500x1500 window size options, the bingo markers
are off by a few pixels. 
"""
class SelectWindowSizeScreen(tk.Tk):
    def __init__(self, *args, **kwargs):
        global HEIGHT_OFFSET

        # Need to call the tkinter constructor
        tk.Tk.__init__(self, *args, **kwargs)

        # Set window size and title
        self.geometry("300x250") 
        self.title(TITLE)      

        LABEL_FONT = font.Font(size=16) # Font for labels
        OTHER_FONT = font.Font(size=12) # Font for everything else

        label = tk.Label(text="Select a window size")
        label.pack()
        label['font'] = LABEL_FONT

        # Used to keep track of which window size the user has selected
        self.var = tk.IntVar(None, 1000)

        # Radio buttons for the different window sizes
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

        # An okay button. Executes the set window size func when clicked
        btn = tk.Button(text="Okay", height=2, command=self.set_window_size)
        btn.pack()
        btn['font'] = OTHER_FONT

    def set_window_size(self):
        """
        Width and height of the application are set and then the window is
        destroyed
        """
        global WIDTH, HEIGHT

        # The actual application window itself needs to be bigger than what the user
        # selected. For example, if 1000x1000 is selected, the bingo card will be
        # 1000x1000, but the application itself will need to be slightly larger
        WIDTH = self.var.get() + 4
        HEIGHT = self.var.get() + HEIGHT_OFFSET

        self.destroy()
