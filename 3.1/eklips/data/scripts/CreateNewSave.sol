id=len(fsm.get("GameData/Projects"))+1
fsm.set(f"GameData/Projects/{id}", data["Engine"]["EditorPath"][0])
shutil.copytree("empty",data["Engine"]["EditorPath"][0])
with open(f'{data["Engine"]["EditorPath"][0]}/ver.txt',"w") as f:
    f.write(f"{data['Engine']['EditorPath'][2][0]}\n{sol_ver}")
with open(f'{data["Engine"]["EditorPath"][0]}/game.txt',"w") as f:
    f.write(data['Engine']['EditorPath'][1])