R=param("rotor_radius",110)
H=param("wall_height",160)
T=param("divider_thickness",6)
F=param("floor_thickness",6)
a=param("panel_apothem",91.5)
slot_w=param("slot_width",3.5)
slot_d=param("slot_depth",2.5)
lip_t=param("slot_lip_thickness",2)
post_c=param("post_center_radius",104.5)
edge_r=param("edge_radius",0.6)
slot_end=a/3**0.5-4
panel_w=2*slot_end-0.4
web=Pos(post_c/2,0,F+H/2)*Box(post_c,T,H)
web=fillet(web.edges().filter_by(Axis.Z),edge_r)
# One solid end cap per radial divider. Flat between the two acrylic slots.
from math import cos, sin, radians
flat_setback=param("corner_flat_setback",1.0)
corner_pts=[(post_c-8,-T/2),(post_c-8,T/2),(R-flat_setback,-T/2),(R-flat_setback,T/2)]
# Collect the original two U-channel outlines; fill their common central notch.
for theta,s in [(30,-1),(-30,1)]:
    c,sn=cos(radians(theta)),sin(radians(theta))
    rects=[(a,s*(slot_end+lip_t/2),slot_w+2*lip_t,lip_t)]
    for n in [-1,1]:
        rects.append((a+n*(slot_w+lip_t)/2,s*(slot_end-slot_d/2),lip_t,slot_d))
    for xx,yy,ww,dd in rects:
        for dx in [-ww/2,ww/2]:
            for dy in [-dd/2,dd/2]:
                x,y=xx+dx,yy+dy
                corner_pts.append((c*x-sn*y,sn*x+c*y))
def cross(o,a,b):
    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
pts=sorted(set(corner_pts))
lower=[]
for p in pts:
    while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:
        lower.pop()
    lower.append(p)
upper=[]
for p in reversed(pts):
    while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:
        upper.pop()
    upper.append(p)
cap=Pos(0,0,F)*extrude(Polygon(*(lower[:-1]+upper[:-1]),align=None),H)
cap=fillet(cap.edges().filter_by(Axis.Z),0.5)
# Match the clipped six-sided footprint of the body and removable top ring.
from math import sqrt
flat_plane=R-flat_setback
flat_face=[f for f in cap.faces() if f.geom_type==GeomType.PLANE and abs(f.normal_at().X-1)<1e-6 and abs(f.center().X-flat_plane)<1e-6][0]
flat_half=flat_face.bounding_box().size.Y/2
raw_half=flat_half+edge_r*(2-sqrt(3))
floor_outline=[]
for i in range(6):
    c,s=cos(radians(60*i)),sin(radians(60*i))
    for y in [-raw_half,raw_half]:
        floor_outline.append((c*flat_plane-s*y,s*flat_plane+c*y))
floor=extrude(Polygon(*floor_outline,align=None),F)
floor=fillet(floor.edges().filter_by(Axis.Z),edge_r)
floor=chamfer(floor.edges().filter_by(Axis.Z,reverse=True),edge_r)
body=floor
for i in range(6):
    body=body+Rot(0,0,60*i)*web
for i in range(6):
    body=body+Rot(0,0,60*i)*cap
body=body & Cylinder(R,F+H,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Exact 3.5-wide slots terminate at +/-slot_end; engagement depth 2.5.
for i in range(6):
    # Relieve only the panel span, leaving exactly 2.5 mm-deep lips at each end.
    body=body-Rot(0,0,30+60*i)*Pos(a,0,F+H/2+0.05)*Box(slot_w+2*lip_t,2*(slot_end-slot_d),H+0.1)
    body=body-Rot(0,0,30+60*i)*Pos(a,0,F+H/2+0.05)*Box(slot_w,2*slot_end,H+0.1)
# User-specified underside center mark for aligning the glued purchased turntable.
alignment_d=param("alignment_recess_diameter",5)
alignment_depth=param("alignment_recess_depth",2)
body=body-Cylinder(alignment_d/2,alignment_depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
# The six dividers rise to the removable ring's upper plane.
rise=param("divider_top_extension",4)
ring_inner=param("top_ring_inner_radius",103)
ring_clearance=param("top_ring_clearance",0.25)
upstand=Pos(post_c/2,0,F+H+rise/2)*Box(post_c,T,rise)
for i in range(1,6):
    upstand=upstand+Rot(0,0,60*i)*Pos(post_c/2,0,F+H+rise/2)*Box(post_c,T,rise)
# A short shoulder below the ring preserves a continuous ring and its panel guides.
upstand=upstand & Pos(0,0,F+H)*extrude(RegularPolygon(ring_inner-ring_clearance/cos(radians(30)),6),rise)
upstand=chamfer(upstand.edges().group_by(Axis.Z)[-1],0.5)
body=body+upstand
body.color=srgb("#f4f1eb")
assert len(body.solids())==1
publish("rotor",body,"旋转筒身",material="pla")
