ux.fill((20,20,30))
path,name,ver,editorarea=data["Engine"]["EditorPath"]
ux.blit(resld.render(name,size=30), [65,25], add_bg=0)
ux.blit(resld.render(path,size=20,color=(90,90,120)), [65,55], add_bg=0)

arrow = resld.render("<-")
play = resld.render("Play")
div = resld.render("-")
script = resld.render("Properties")
files = resld.render("Files")

back_button = ux.button(arrow, [25,25],layer=12,add_bg=0, id=f"WorkflowLeave{path}", size=(30,30))
if back_button:
    data["Engine"]["Scene"] = "main"

play_button = ux.button(play, [25,25],layer=12,add_bg=0, id=f"WorkflowPlay{path}", anchor="right")
if play_button:
    print("Launching Eklips subprocess")
    old_game = open("game.txt").read()
    with open("game.txt", "w") as f:
        f.write(f"{name}\n{path}")
    os.system("python.exe Eklips.py")
    with open("game.txt", "w") as f:
        f.write(old_game)

ux.blit(div, [105,25],layer=13,add_bg=0,anchor="right")
script_button = ux.button(script, [135,25],layer=12,add_bg=0, id=f"WorkflowScript{path}", anchor="right")
if script_button:
    editorarea = "p"

ux.blit(div, [155,25],layer=13,add_bg=0,anchor="right")
files_button = ux.button(files, [185,25],layer=12,add_bg=0, id=f"WorkflowFiles{path}", anchor="right")
if files_button:
    editorarea = "f"

if editorarea == "p":
    proptxt = [resld.render("On"),resld.render("Off"),
        resld.render("Account Properties"),
        resld.render("Account System"),
        resld.render("Server"),

        resld.render("Game Data Structure"),

        resld.render("Performance Properties"),
        resld.render("Framerate Limit"),
        resld.render("Supports Alpha"),
        resld.render("Resolution"),

        resld.render("Background Properties"),
        resld.render("Background"),
        resld.render("Parallax"),

        resld.render("Font Properties"),
        resld.render("Font"),
        resld.render("Size"),

        resld.render("Gameplay Properties"),
        resld.render("Update() Path"),

        resld.render("Loading Properties"),
        resld.render("Show Tips"),
        resld.render("Splash Screen"),
        resld.render("Do not load everything"),

        resld.render("Keybinds"),
        resld.render("Key No."),
        resld.render("Key"),
        resld.render("Holdable"),
        resld.render("Script ID")
    ]
