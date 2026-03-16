# cython build
import os
import shutil

# Create cxx directory if it doesn't exist
try:
    os.mkdir("cxx")
except:
    shutil.rmtree("cxx")
    os.mkdir("cxx")

# Run the setup script with build_ext command
os.system("python cyt.py build_ext --inplace")

# Define variables
app = "Sol"
appn = open("game.txt").read().splitlines()[1]

# Find, copy and delete the original C files
shutil.copytree("classes", "cxx/classes")
try:
    shutil.copytree("classes/overlay", "cxx/classes/overlay")
except:
    print("CXX build Overlay folder issue")

for dirpath, dirnames, filenames in os.walk("cxx"):
    for filename in filenames:
        if filename.endswith(".py"):
            os.remove(os.path.join(dirpath, filename))

for dirpath, dirnames, filenames in os.walk("classes"):
    for filename in filenames:
        if filename.endswith(".c"):
            os.remove(os.path.join(dirpath, filename))

shutil.copy("solhl.c", "cxx/solhl.c")
os.remove("solhl.c")
shutil.copy(f"{app}.c", f"cxx/{app}.c")
os.remove(f"{app}.c")
shutil.copy("game.txt", "cxx/game.txt")
shutil.copytree(".soleng", "cxx/.soleng")
shutil.copytree(appn, f"cxx/{appn}")