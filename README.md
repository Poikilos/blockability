# Blockability
A Pygame block engine with linear exploration (a work in progress).

## Known issues
* jumping downward into door can cause falling back out but warping to next room, causing you to fall through bottom of world
	
## Differences from Platformy
All changes since initial commit are original to blockability. Initial commit was an upload of Platformy, for tracking changes from version that was the basis of the fork.
Platformy all-inclusive feature list: 1-color blocks (gray blocks, blue background, blue door), gravity, pygame-based hit detection, sys.exit() & pygame quit on door, 1-frame non-alpha sprite player character, two types of Blocks: P for platform, E for exit.
Platformy known issue list: tick method used in wrong spot, crash on exit (tested only in Python 3), jump through walls if going downward diagonally fast enough, uses inheritance instead of block properties, included an mp3 with incompatible license which was not implemented (no sound was implemented)

## Credits
* based on LiefAndersen's platformy
* turtle supplied by LiefAndersen (I could not find any source via google similar image search)
* All the square graphic tiles used in this program from the file DungeonCrawl_ProjectUtumnoTileset.png (CC-0) is the Public domain roguelike tileset "RLTiles". Some of the tiles have been modified by expertmm. You can find the original tileset at: http://rltiles.sf.net You can find Dungeon Crawl Stone Soup modified tilesets at: http://code.google.com/p/crawl-tiles/downloads/list

### Music
* A2backw by OATMEALCRUNCH CC-0 (117818__oatmealcrunch__a2backw.ogg)

### Sound
* door by rivernile7 CC-BY (door-wood-open and door-wood-close are based on 234244__rivernile7__door-open-and-close.wav)

### Info for Developers
#### Instructions for working with pygame with python 3 in Geany
see http://expertmultimedia.com/usingpython/py3pygame-geany.html
