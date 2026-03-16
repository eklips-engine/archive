import json, sys
from classes import cv
from pyglet import resource
from SpecialIsResourceDataLoadable import IS_IT

ignore_dirparam = False
project_file    = "eklips/game.json" # Change this for your project file

argv            = sys.argv
id              = 0
for i in argv:
    try:
        aftr  = argv[id+1]
    except:
        pass
    if i == "-js":
        project_file    = aftr
    if i == "-dir":
        ignore_dirparam = aftr.replace("%20", " ")
    id   += 1

game_bdata     = 0
data_directory = 0
game_name      = 0
cvars          = 0

def _init():
    global project_file,game_bdata,data_directory,game_name,cvars
    if IS_IT:
        game_bdata     = json.loads(resource.file(f"{project_file}").read())
    else:
        game_bdata     = json.loads(open(f"{project_file}").read())
    cvars          = cv.CvarCollection()
    cvars.init_from(game_bdata["cvars"])
    if ignore_dirparam:
        data_directory = ignore_dirparam
        cvars.set("directory", data_directory, data_directory, "directoryParameterModifiedByExecuteParam")
    else:
        data_directory = cvars.get("directory")
        if data_directory == "point::UseGameJsonParent":
            # Windows on its way to not use the standard and use the fucking backwards slash, WHY?!
            data_directory = project_file.replace("\\","/").split("/")[-1]
    game_name      = game_bdata["game_name"]
    return cvars