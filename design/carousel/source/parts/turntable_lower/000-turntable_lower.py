d=param("outside_diameter",150)
h=param("overall_height",11)
seam=0
half=h/2
b=Cylinder(d/2,half,align=(Align.CENTER,Align.CENTER,Align.MIN))
b.color=srgb("#e6f3f8",0.18)
publish("turntable_lower",b,"透明亚克力旋转器下盘",material="acrylic",role="reference")
