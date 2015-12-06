# Blockability
Includes BAWidgets, which is a complete widget system (including one-line custom dialog box creation)--see baspriteframer for an example of using BAWidgets.
Blockability is a block-based game engine specification with nonlinear exploration and persistent world. It can be implemented in pygame or any other engine. This project includes a pygame implementation of the spec (example is a work in progress).

## How-to program:
* Make a file like "example.py": make a subclass of BAGame, define run inside of it, then in main, make an instance of it (param is data_path), then call the run method (see Known issues first).

## Known issues
* fix non-working example: deprecate main in blockability.py, and re-implement, splitting into BAGame.__init__ and TheMissingString(BAGame).run
* (BAWidgets) Make listview generic, and only relist when necessary, and create pieces ahead of time (and clean up list_files code accordingly)
* (BAWidgets) add "anchor" list member to BAWidget to allow better alignment of scrollbar buttons
* (BAWidgets) add scrollbar between scrollbar buttons
* (BAWidgets) valign is not fully tested
* (BAWidgets) skinning for margin and padding is not implemented
* (BAWidgets) get_top_widget_at gets button that made dialog appear if title of dialog is clicked
* (BAWidgets) (make maximum filename length showable, then) use docking to avoid scroll_spacer_widget minimum_rect width being files_widget._minimum_rect.width-18
* jumping downward into door can cause falling back out but warping to next room, causing you to fall through bottom of world
* should generate and show credits automatically: pre_credits.txt, then <name>-CREDITS.txt for each <name> (file or folder) in data_path (recursively), then post_credits.txt
	* IF a line starts with "notify:" then do not display that part (only the rest of the line). Instead, notify the author of use using that information.
	* IF a line starts with "notified:" then do not display that entire line (it is just for keeping record of when [and how if desired] notified)


## "Story" format spec
* Universal yml variables:
	all in-game pos variables should be cartesian (pos values in yml files should be ALREADY be flipped as written to YAML since they are referring to chunk layout image pixels)
	pos is always position coordinates (usually a list with 2 elements for 2D, but can be 3 if needed)
		(divided by chunk_size in chunks.yml)
	world is always a universal worldname
	crop (used only for tileset and frame yml files): left,top,width,height
		cell_crop is used similarly, and is for tilesets with padding: for example, if cell_crop is 4,4,34,34 that will be the rect for the first cell, then the rect for the second cell (block cell 1,0) will automatically be 38,38,34,34 which comes from 4+34,4+34,34,34 (4 since 0 to 3 includes 4 pixels being skipped between each cell rect, and each cell including padding takes up 38x38)
	image_path: always relative to _images_path
* A story is stored in _data_path (Stories can share resources if you manually change paths, such as game._images_path, after you make an instance of BAGame subclass but before you call the run method)
	* A save (folder generally called state from here on) is stored as a state in data/states
	* The conditions for the beginning of the game is stored as a state called "(start)"
	* All images are stored in _images_path (usually data/images folder)
	* each WORLD for the game (story) are stored in state/worlds
	* When game is saved, states/(start) is never modified--it is instead copied fully to a new folder in states, numbered starting at 0 with state.yml containing name
	* Chunks folder in WORLD contains the chunks, and chunks.yml which defines:
		block_size: width, comma, height, in number of pixels (blocks should be stretched to this size) -- if 3D, this should be meters (opengl units)
		chunk_size: width, comma, height, in number of blocks
	* Each CHUNK of the world is saved in a folder by chunk coordinates (for example, if chunk_size is 64,64, then chunk folder named 2,1 would start at block 128,64)
	* The world (made of blocks) layout is saved in each chunk of WORLD/chunks
	* Blocks (block types) are defined in data/blocks (and used in state/chunk)
		* There is a maximum of (256*256*256) block types, since chunk layouts are stored as images where color is block
	* All players are stored in state/players (only local folders have parenthesis, such as "(1)" for local player 1)
		* world: the world where to place the camera
		* pos: the camera position
	* All characters for the game are defined in state/characters
		* location: is required for player's character if there is a player character
		* owner: who owns the character
	* Sprites are stored in yml files in data/sprites folder and all poses are references frame yml files (".yml" will be appended) in frames folder (multiple frame yml files can use same image, each with a different crop variable [or no crop variable] if needed)
	* Frames are stored in yml files in frames folder, and image_path is relative to data/images
	* Sprites can only reference frame yml files, while worlds can only reference blocks (blocks reference tilesets, so a world can reference multiple tilesets, whereas a tileset can only reference one image)




## Differences from Platformy
* All changes since initial commit are original to blockability. Initial commit was an upload of Platformy, for tracking changes from version that was the basis of the fork.
* Platformy all-inclusive feature list: 1-color blocks (gray blocks, blue background, blue door), gravity, pygame-based hit detection, sys.exit() & pygame quit on door, 1-frame non-alpha sprite player character, two types of Blocks: P for platform, E for exit.
* Platformy known issue list: tick method used in wrong spot, crash on exit (tested only in Python 3), jump through walls if going downward diagonally fast enough, uses inheritance instead of block properties, included an mp3 with incompatible license which was not implemented (no sound was implemented)

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
