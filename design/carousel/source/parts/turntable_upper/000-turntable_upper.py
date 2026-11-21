dimensions=part("turntable_lower")
d=dimensions.d
h=dimensions.h
half=dimensions.half
opacity=param("optical_opacity",0.18)
b=Cylinder(d/2,half,align=(Align.CENTER,Align.CENTER,Align.MIN))
b.color=srgb("#e6f3f8",opacity)
publish("turntable_upper",b,"透明亚克力旋转器上盘",material="acrylic",role="reference")
