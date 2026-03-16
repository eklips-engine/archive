import os,shutil

gametxt=open("game.txt").read().split("\n")[1]
os.system("pyinstaller Eklips.py --distpath=builds/dist --workpath=builds/work --noconfirm")
shutil.copy("game.txt", "builds/dist/Eklips/game.txt")
shutil.copytree(gametxt, "builds/dist/Eklips/"+gametxt)
shutil.copytree("classes", "builds/dist/Eklips/classes")
shutil.copytree(".ekeng", "builds/dist/Eklips/.ekeng")
shutil.copy("ekhl.py", "builds/dist/Eklips/ekhl.py")
