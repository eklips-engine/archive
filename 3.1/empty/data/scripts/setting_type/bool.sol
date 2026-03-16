@Option
code=Sol.Save.Set(f"Settings/{category}/{option}", (not value))
txt=(Sol.Lang["yes"] if value else Sol.Lang["no"])