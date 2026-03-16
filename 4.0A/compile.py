import os, Data, shutil

Data._init()

print(f"## Compiling Eklips project {Data.game_name}")
print(f" ~ Modifying .spec")
og_specfile = open("Eklips.spec").read()
with open("Eklips.spec", "w") as f:
    f.write(f"data_directory = '{Data.data_directory}'\n")
    f.write(f"game_name      = '{Data.game_name}'\n")
    f.write(og_specfile)

print(f" ~ Modifying Eklips setting")
og_eklfile = open("SpecialIsResourceDataLoadable.py").read()
with open("SpecialIsResourceDataLoadable.py", "w") as f:
    f.write(f"IS_IT = True # This variable is so that the game can detect if it's an EXE or not (which are pretty much only onefile)")

print(f" ~ Compiling Eklips build")
shutil.rmtree("dist", ignore_errors=1)
os.system("pyinstaller Eklips.spec")

print(f" ~ Reverting .spec")
with open("Eklips.spec", "w") as f:
    f.writelines(og_specfile)

print(f" ~ Reverting Eklips setting back to normal")
with open("SpecialIsResourceDataLoadable.py", "w") as f:
    f.write(og_eklfile)