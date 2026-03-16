if not Sol.Data<Engine>["MainMenu"]:
    Sol.Data<Player>["Vel"][0] += (int(Sol.Player.Properties["speed"]) * 10) * Sol.DT
    Sol.Data<Player>["Flp"] = 0