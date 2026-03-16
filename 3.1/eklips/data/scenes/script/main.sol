ux.fill((20,20,30))
ux.blit(resld.render("Please pick a package:"), [40,25], add_bg=0)
add = resld.render("Add +")
arrow = resld.render("->",size=25)
frame = ux.rect((5,5,10),(display.get_width()-40,display.get_height()-105))
offset = ux.slider(35, 75+frame.get_height()-25, min_value=0, max_value=frame.get_width(), initial_value=0, out_type=["int", 0], disp="display", width=frame.get_width()-30, id="SCROLL.0", layer=5)

add_button = ux.button(add, [40,25],layer=12,add_bg=0,anchor="right")
if add_button:
    data["Engine"]["Scene"] = "add_project"

totaloff=0
for i in fsm.get("GameData/Projects", {}):
    path=fsm.get(f"GameData/Projects/{i}")
    try:
        name = open(f"{path}/game.txt").read()
    except:
        name = "??"
    try:
        ver = open(f"{path}/ver.txt").read().splitlines()
    except:
        ver = ["0.0.0","0.0.0"]
    rendered_name=resld.render(name)
    rendered_ver=resld.render(f"App {ver[0]} | Ekl {ver[1]}", size=25, color=(40,40,60))
    if (50-offset)+totaloff > 20 and (((50-offset)+totaloff)+rendered_name.get_width()+abs(rendered_name.get_width()-rendered_ver.get_width())) < frame.get_width()+20:
        ux.blit(ux.rect((10,10,20),(5,rendered_name.get_height()+50+rendered_ver.get_height())),[(35-offset)+totaloff, 100], layer=4)
        ux.blit(rendered_name, [(50-offset)+totaloff, 115], layer=3)
        ux.blit(rendered_ver, [(50-offset)+totaloff, 175], layer=3)
    
    width=rendered_name.get_width()+abs(rendered_name.get_width()-rendered_ver.get_width())
    rect_size=(width,frame.get_height()-250)
    hover = ux.blit(ux.rect((5,5,10),rect_size),[(50-offset)+totaloff, 100], layer=-1)
    if hover["click"][0]:
        ver=ver[1].split(".")
        sv=sol_ver.split(".")
        if int(ver[0]) == int(sv[0]):
            print("Matches Major")
            if int(ver[1]) == int(sv[1]):
                print("Matches Medium")
                data["Engine"]["EditorPath"] = [path,name,ver,"p"]
                data["Engine"]["Scene"] = "edit_workflow"
            else:
                answer=askyesno(f"Eklips Editor", f"The application is not supported for your Medium version of Eklips, Run anyway?")
                if answer:
                    data["Engine"]["EditorPath"] = [path,name,ver,"p"]
                    data["Engine"]["Scene"] = "edit_workflow"
        else:
            answer=askyesno(f"Eklips Editor", f"The application is not supported for your Major version of Eklips, Run anyway?")
            if answer:
                data["Engine"]["EditorPath"] = [path,name,ver,"p"]
                data["Engine"]["Scene"] = "edit_workflow"

    if hover["hovering"]:
        ux.blit(arrow, [(30-offset)+totaloff, 120],layer=5,add_bg=0)

    totaloff+=width+30

ux.blit(frame,(20,75), layer=1)
frame_end = ux.rect((20,20,30),(20,display.get_height()-105))
ux.blit(frame_end,(0,75), layer=124)