# Sol_NewWindow Add%Project 350x400
ux.fill((20,20,30))
ux.blit(resld.render("Add new project:"), [80,25], add_bg=0)
arrow = resld.render("<-")
add = resld.render("Add +")
back_button = ux.button(arrow, [40,25],layer=12,add_bg=0, id="AddBack")
add_button = ux.button(add, [40,25],layer=12,add_bg=0,anchor="right bottom", id="ADDADD")
if back_button:
    data["Engine"]["Scene"] = "main"
if add_button:
    data["Engine"]["EditorPath"] = ["E:/G", "Name", ["1.0",sol_ver],"p"]
    Eklips.Execute(f"{Eklips.Resource.resfol}/data/scripts/CreateNewSave.sol",gl=globals(),lc=locals())
    data["Engine"]["Scene"] = "edit_workflow"

frame = ux.rect((5,5,10),(display.get_width()-40,display.get_height()-105))

ux.blit(frame,(20,75), layer=1)