# Blockability
A Pygame block engine with linear exploration (a work in progress).

## Known issues
* jumping downward into door can cause falling back out but warping to next room, causing you to fall through bottom of world
	
## Changes since platformy
(all changes since initial commit that had 1-color blocks, exit on door, 1-frame non-alpha sprite)

## Credits
* based on LiefAndersen's platformy
* turtle supplied by LiefAndersen (I could not find any source via google similar image search)
* All the square graphic tiles used in this program from the file DungeonCrawl_ProjectUtumnoTileset.png (CC-0) is the Public domain roguelike tileset "RLTiles". Some of the tiles have been modified by expertmm. You can find the original tileset at: http://rltiles.sf.net You can find Dungeon Crawl Stone Soup modified tilesets at: http://code.google.com/p/crawl-tiles/downloads/list

### Music
* A2backw by OATMEALCRUNCH CC-0 (117818__oatmealcrunch__a2backw.ogg)

### Sound
* door by rivernile7 CC-BY (door-wood-open and door-wood-close are based on 

### Info for Developers
#### Instructions for working with pygame with python 3 in Geany
Download python 3.2 from https://www.python.org/ftp/python/3.2.5/python-3.2.5.msi
 (must be 3.2 for pygame to work) and install (during install, choose install for All Users)
Download Pygame 1.9.2 py3.2 (make sure you get python 3.2 version) from http://pygame.org/ftp/pygame-1.9.2a0.win32-py3.2.msi and install
Download Geany from geany.org and install
In Geany, change options for python:
open a python file or save the untitled file to untitled.py (in order to be able to change py file settings), then click Edit, Preferences, Editor, "Indentation" tab.
for Type choose "Spaces"
Make sure "Tab key indents" is unchecked
For  your benefit, in the "Display" tab check "Show indentation guides"
On "Files" side tab, make sure "Replace tabs by space" is checked
OK
To use the new settings for the current file, Click "Project," "Apply Default Documentation"
