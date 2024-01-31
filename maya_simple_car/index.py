import maya.cmds as cmds

def create_car(name,length=2,width=1):
    body = create_body(length,width)
    tires = create_tiers(length,width)
    final_name = assemble_car(name,body,tires)
    
    cmds.select(clear=True)
    
    return final_name

def create_body(length,width):
    body = cmds.polyPlane(w=length,h=width,name="body")
    return body

def create_tiers(body_length,body_width):
    tire_width  = 0.25 * body_width
    tire_radius = 0.25 * body_length
    x_pos = 0.5 * body_length
    z_pos = 0.5 * body_width + 0.5 * tire_width
    # all in the middle first, then move around
    fl_tire = create_tier("front_left_tire", tire_width,tire_radius,x_pos,0,-z_pos)
    fr_tire = create_tier("front_right_tire", tire_width,tire_radius,x_pos,0,z_pos)
    rl_tire = create_tier("rear_left_tire", tire_width,tire_radius,-x_pos,0,-z_pos)
    rr_tire = create_tier("rear_right_tire", tire_width,tire_radius,-x_pos,0,z_pos)
        
    return [fl_tire,fr_tire,rl_tire,rr_tire]
    
def create_tier(name,width,radius,tx,ty,tz):
    # get the first transform node
    tire = cmds.polyCylinder(h=width,r=radius,ax=(0,0,1),sc=True,name=name)[0]
    cmds.setAttr(f"{tire}.translate",tx,ty,tz)
    return tire
    
def assemble_car(name,body,tires):
    body_grp = cmds.group(body,name="body_grp")
    tires_grp = cmds.group(tires,name="tires_grp")
    
    car_grp = cmds.group(body_grp,tires_grp,name=name)
    return car_grp

# will only execute directly
if __name__ == "__main__":
    name = create_car("test_car")
