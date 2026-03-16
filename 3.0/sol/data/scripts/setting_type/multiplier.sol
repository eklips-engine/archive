@Option
code=Sol.Save.Set(f"Settings/{category}/{option}", value + 1 if int(settingdata["min"]) < value + 1 < int(settingdata["max"]) + 1 else settingdata["min"])
txt=f"{value}x"