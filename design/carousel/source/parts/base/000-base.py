d=param("base_diameter",230)
t=param("base_thickness",6)
edge=param("edge_radius",0.6)
alignment_d=param("alignment_recess_diameter",5)
alignment_depth=param("alignment_recess_depth",2)
pad_circle=param("foot_pitch_radius",99)
pad_pocket_d=param("foot_pocket_diameter",14.4)
pad_recess=param("foot_recess_depth",0.5)
b=Cylinder(d/2,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
b=chamfer(b.edges(),edge)
# Center reference on the upper gluing face; this is a blind recess, not a pin bore.
b=b-Pos(0,0,t-alignment_depth)*Cylinder(alignment_d/2,alignment_depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
from math import cos, sin, radians
for i in range(6):
    b=b-Pos(pad_circle*cos(radians(60*i)),pad_circle*sin(radians(60*i)),0)*Cylinder(pad_pocket_d/2,pad_recess,align=(Align.CENTER,Align.CENTER,Align.MIN))
b.color=srgb("#f4f1eb")
assert len(b.solids())==1
publish("base",b,"静止底座",material="pla")
