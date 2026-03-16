## Initialize objects
print("Initializing objects")

# Eklips.Execute(f"{Eklips.Resource.resfol}/data/scripts/objects/Entity.sol",gl=globals(),lc=locals()) <- Replace the filename with the filename of the object you want to initialize

## Define objects
print("Defining objects")
# u_lvl = Stage() <- Replace this with the class you want to initialize

## Add objects to Update() list
print("Adding objects")
data["ObjectsUpd"]={
    # Add the classes you want to initialize
}

## Exit Main Menu
data["Engine"]["MainMenu"] = 0