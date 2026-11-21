layout=part("rotor")
R=param("outer_vertex_radius",110)
inner=layout.ring_inner
t=layout.rise
skirt=param("guide_skirt_depth",2.5)
gap=param("panel_guide_width",3.6)
lip=param("guide_wall_thickness",1.5)
end_clearance=param("guide_end_clearance",0.3)
span=2*(layout.slot_end-layout.slot_d-end_clearance)
assert span>0
# Six flat cap faces share both plane and width with the actual divider end caps.
from math import cos, sin, radians, sqrt
flat_plane=layout.R-layout.flat_setback
flat_face=[f for f in layout.cap.faces() if f.geom_type==GeomType.PLANE and abs(f.normal_at().X-1)<1e-6 and abs(f.center().X-flat_plane)<1e-6][0]
flat_half=flat_face.bounding_box().size.Y/2
corner_radius=param("flat_corner_radius",0.6)
raw_half=flat_half+corner_radius*(2-sqrt(3))
outline_points=[]
for i in range(6):
    c,s=cos(radians(60*i)),sin(radians(60*i))
    for y in [-raw_half,raw_half]:
        outline_points.append((c*flat_plane-s*y,s*flat_plane+c*y))
outer=extrude(Polygon(*outline_points,align=None),t)
outer=fillet(outer.edges().filter_by(Axis.Z),corner_radius)
b=Pos(0,0,skirt)*(outer-extrude(RegularPolygon(inner,6),t))
b=chamfer(b.edges().group_by(Axis.Z)[-1],0.5)
for i in range(6):
    for s in [-1,1]:
        rail=Pos(layout.a+s*(gap+lip)/2,0,skirt/2)*Box(lip,span,skirt)
        b=b+Rot(0,0,30+60*i)*rail
b.color=srgb("#f4f1eb")
assert len(b.solids())==1
publish("top_ring",b,"可拆六边形顶环",material="pla")
