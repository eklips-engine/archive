if txtd[1] == "kill":
    u_player.soul.damage(u_player.soul.data["hp"])
if txtd[1] == "damage":
    u_player.soul.damage(int(txtd[2]))
if txtd[1] == "speed":
    u_player.soul.data["speed"] = int(txtd[2])