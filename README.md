<p align="center">
  <img src="https://cdn.discordapp.com/attachments/886341235768442922/1002149841457127504/Screenshot_2022-07-27_001548-removebg-preview.png" />
</p>

![](https://cdn.discordapp.com/attachments/886341235768442922/1002183410665668659/unknown.png)

Create over 200 octilion different bingo cards (if I did my [math](https://github.com/catzAreVeryCute/huntshowdown-bingo/issues/1) right) at random using 35 different bingo tiles! Save the bingo card as image, or use the application to mark up the bingo card just by clicking on the tile. Even add your own bingo tiles to the mix! If you're curious as to what the different tiles, navigate into the project's assets folder and click on the "tiles" folder.


# Table of Contents

* [Installation](#install)
  * [Windows Installation](#windows)
  * [Other Installation](#other)
* [Usage](#usage)
* [Comments](#comments)
* [Built With](#builtwith)
* [Acknowledgements](#ack)
* [Contact](#contact)

<a name="install"></a>
## Installation

<a name="windows"></a>
### Windows Installation
I've packaged the program into a working executable that you can download. If you aren't a Windows user, or if you aren't comfortable using the exectuable, see the [other installation.](#other)

To download the executable, click on the latest release located on the right. 
![](https://cdn.discordapp.com/attachments/886341235768442922/1002195074198798436/unknown.png)

Once there, download the zip file titled "Hunt.Showdown.Bingo.zip." You can also download the source code if you'd like, but it isn't necessary for the executable to run. Once you've downloaded the zip folder, go ahead and unzip it. Inside the folder, you'll see a folder titled `dist`. Inside this folder you'll find the exectuable; it should be titled `main.exe`. To run the program, click this, and you're done! **Note: Do NOT move the executable from this folder! If you don't want to navigate to this folder everytime you want to run the program, just create a shortcut to the executable somewhere accessible.**

<a name="other"></a>
### Other Installation
You can still run the program even if you aren't on a Windows computer or if you don't want to use the provided executable. To do this, you'll need to follow these instructions. 

1.) Download Python 3 (version 3.10.5 or higher). During the installation process, **make sure that you click the tick box asking if you want to add Python 3 to your PATH.** In the image below, it's the box that's unticked. 
![](https://docs.python.org/3/_images/win_installer.png)

2.) Download the source code from the main branch. 

3.) You'll notice that the source code has a file titled `requirements.txt`. You'll want to open up a terminal and navigate to where that file is located on your computer via the terminal. Then run `pip install requirements.txt` from the terminal. You need to do this because the base installation of Python 3 alone isn't capable of running the script. 

4.) Now you should be able to run the program. To do so, run the command `python main.py` from your terminal to run the program. 

If you have trouble with these types, you can contact me via Discord. 


<a name="usage"></a>
## Usage

#### Generating a Bingo Card
To generate a new bingo card, simply click the "New Card" button. 

<br>

#### Marking a Bingo Card
Click on the tiles to mark and umark the card. 

<br>

#### Clearing the Bingo Card
Click the "Clear Card" button to get rid of all marks on the bingo card.

<br>

#### Saving the Bingo Card
If you want to save your bingo card as a .png, you can click the "Save Card" button. Saving the card DOES NOT save the markings that you've made on the card; just the blank card is saved.

<br>

#### Adding Your Own Tiles
If you want to add custom tiles for the bingo card to process, you can use the "Add Tiles" button. Upon clicking the button, a dialogue box will pop up. Select your tile image and it'll automatically be added to your assets/tiles folder. If you're going to make custom tiles for the program, ensure that they are 549x546 (549 pixels wide, 546 pixels high) and that it's a .png file. The program assumes these dimensions, so if you add an image file that doesn't fit the expectation, weird stuff will happen. Don't let weird stuff happen. 

#### Removing Tiles
If there's a particular tile that you don't want showing up on your card, you'll have to remove the image file from the `dist/assets/tiles` folder manually. 

<br>

<a name="comments"></a>
## Comments 
This'll be added later cause I'm lazy.

<a name="builtwith"></a>
## Built With
* [Python 3](https://www.python.org/downloads/) - The programming language used to write the program
* [Pillow](https://python-pillow.org/) - Used for image manipulation
* [Tkinter](https://docs.python.org/3/library/tkinter.html) - Used for creating the GUI
* [Pyinstaller](https://pyinstaller.org/en/stable/) - Used to package the program into an executable

<a name="ack"></a>
## Acknowledgements 
All assets are the property of Crytek. 

Assets were created and edited by the goated gigachad Bwabcat using Clip Studio. 

## Contact 
If you need to contact me, the maintainer of this repository for any reason, add me on my Discord: Kizie#5066
