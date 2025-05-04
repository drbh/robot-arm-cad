import numpy as np
from build123d import (
    Pos,
    Box,
    Cylinder,
    Rot,
    export_gltf,
    Mesher,
    Triangle,
    extrude,
    scale,
    Align,
)
from ocp_vscode import show_object
import copy
import time
import math

disk_diameter = 35.0
disk_thickness = 2.0
wall_thickness = 2.0
gap_width = 50
height = 25.0
depth = 20.0
mount_hole_diameter = 3.0
mount_width = 10.0
mount_length = 8.0
mount_thickness = wall_thickness


def create_c_shape_with_mount():
    outer_box = Box(
        width=gap_width + 2 * wall_thickness,
        length=depth,
        height=height + 3,
    )

    inner_box = Box(
        width=gap_width,
        length=depth + 4 * wall_thickness,
        height=height + 3,
    )

    inner_box = Pos(wall_thickness, 0, wall_thickness) * inner_box

    mount_tab = Cylinder(radius=depth / 2, height=2)
    mount_tab = Rot(90, 0, 0) * mount_tab

    mount_tab_1 = Pos(0, -gap_width / 2 - 1, 15) * mount_tab
    mount_tab_2 = Pos(0, gap_width / 2 + 1, 15) * mount_tab

    c_shape = outer_box - inner_box
    c_shape = c_shape + mount_tab_1 + mount_tab_2

    cross_bar = Cylinder(radius=4, height=disk_diameter * 2.5)
    cross_bar = Rot(90, 0, 0) * Pos(0, 15, 0) * cross_bar
    c_shape = c_shape - cross_bar

    mounting_holes = []
    mount_width = 7

    for i in range(4):
        angle = np.radians(i * 90)
        x = mount_width * np.cos(angle)
        y = mount_width * np.sin(angle)

        _hole = Cylinder(radius=1.75, height=8)
        hole = Rot(90, 0, 0) * Pos(x, 15 + y, gap_width / 2 - 1) * _hole
        mounting_holes.append(hole)

        hole = Rot(90, 0, 0) * Pos(x, 15 + y, -gap_width / 2 + 1) * _hole
        mounting_holes.append(hole)

    for hole in mounting_holes:
        c_shape = c_shape - hole

    return c_shape


outer_well = Cylinder(radius=(depth / 2) - 1, height=4)
outer_well = Rot(90, 0, 0) * Pos(0, 15, gap_width / 2 + 4) * outer_well
outer_well2 = Rot(90, 0, 0) * Pos(0, 15, -gap_width / 2 - 4) * outer_well
wells = outer_well + outer_well2

c_shape_1 = create_c_shape_with_mount()
c_shape_2 = create_c_shape_with_mount()

c_shape_2 = Pos(0, -10 + 51, 13) * Rot(270) * c_shape_2

# back triangle
tri = Triangle(
    a=54,
    b=40,
    c=40,
)
d = 33
tri = Rot(270, 90, 0) * tri
tri_prism = extrude(tri, d)
tri_prism = Pos(-d / 2, 0, -24) * tri_prism

# find percent that is 2px smaller than the base
thickness = 4

percent = (tri.a - (2 * thickness)) / tri.a  # 2px smaller

print("triangle", tri.a)
print("percent", percent)

# tri smaller
smaller_tri = scale(tri_prism, (1, percent, percent))


tri_prism2_bottom_cut = Box(
    d,
    60,
    56,
)


tri_prism2 = copy.copy(tri_prism)

tri_prism2 = tri_prism2 - tri_prism2_bottom_cut
tri_prism = tri_prism - smaller_tri + tri_prism2
c_shape_clone = copy.copy(c_shape_1)

c_shape_clone = Rot(0, -90, 0) * c_shape_clone
c_shape_clone = (
    Pos(
        -92 + 15,
        -2.5,
        0,
    )
    * c_shape_clone
)

c_cut = Box(54, 25 + 4, 40)
c_cut = Pos(-96 + 15, -12.5 - 2.5 - 2, 10) * c_cut

c_shape_clone = c_shape_clone - c_cut


c_shape_clone = Pos(-0.34 - 68, 0, 0) * c_shape_clone


x = 25
tri4 = Triangle(
    a=x,
    b=x,
    c=math.sqrt(x**2 * 2),
)
d = 20 + 6.5
tri4 = Rot(0, 0, 270) * tri4
tri_prism4 = extrude(tri4, d)
tri_prism4 = Pos(-30.825 - 0.34 - 68, 10.05 + 0.12 - 1.34 - 3, -3.5 - 6.5) * tri_prism4

bracket_length = 48.0 + 7
bracket_width = 23.0
bracket_depth = 5.0

bracket_outer = Box(bracket_length, bracket_depth, bracket_width, align=Align.CENTER)

bracket_inner = Box(
    bracket_length - (8 + 7),
    bracket_depth,
    bracket_width - 1,
    align=Align.CENTER,
)

bracket_inner = Pos(0, 0, -1) * bracket_inner

post = Box(
    bracket_depth + 75,
    bracket_depth + 1.5,
    bracket_depth * 2,
    align=Align.CENTER,
)

post = (
    Rot(90, 0, 0)
    * Pos(12.5, bracket_depth + bracket_depth + 3.25, bracket_depth / 2)
    * post
)

postlong = copy.copy(post)
postlong = Pos(-80, 0, 0) * postlong

post = post + tri_prism4 + postlong


# screw holes at the bottom of the post
screw_hole = Cylinder(1.5, 100)
screw_hole = Rot(90, 0, 0) * Pos(12.5, 13.5, 0) * screw_hole
screw_hole = Pos(-36, 0, 0) * screw_hole
screw_hole2 = Pos(0, 0, -27) * screw_hole

post = post - screw_hole

post = Pos(-25, 0, 0) * post

bracket = bracket_outer - bracket_inner + post

extra_cut = Box(100, 20, 10)
extra_cut = Pos(0, 7.5, -15) * extra_cut

bracket = bracket - extra_cut

bracket2 = Pos(0, -5, 0) * Rot(0, 180, 180) * bracket

pos_hole_on_arm = 10

screw_hole = Cylinder(1.5, 100)
screw_hole = Rot(90, 0, 0) * Pos(pos_hole_on_arm, 13.5, 0) * screw_hole

screw_hole2 = Pos(0, 0, -27) * screw_hole

screws = screw_hole + screw_hole2

# servo mount screw holes
big_screw_hole = Cylinder(1.5, 100)
_big_screw_hole = Rot(90, 0, 0) * big_screw_hole

big_screw_hole = Pos(24, 0, 5) * _big_screw_hole
big_screw_hole2 = Pos(24, 0, -5) * _big_screw_hole

big_screw_holes = big_screw_hole + big_screw_hole2

big_screw_holes2 = Pos(-48, 0, 0) * big_screw_holes
big_screws = big_screw_holes + big_screw_holes2

bracket = bracket - big_screws
bracket2 = bracket2 - big_screws

bracket = bracket - screws
bracket2 = bracket2 - screws


brackets = bracket + bracket2
brackets = Rot(0, 90, 0) * brackets
brackets = Pos(0, 2, -84) * brackets
bracket = bracket + c_shape_clone

show_object(
    bracket,
    name="Bracket",
    options=dict(color="orange", alpha=0.5),
)

c_shape_1 = Pos(0, 0, -0.5) * c_shape_1
complete_shape = c_shape_1 + tri_prism + brackets

start_time = time.time()
exporter = Mesher()

exporter.add_shape(bracket, part_number="A")
exporter.write("output/elbow-forearm.3mf")
print("Total Exporting 3mf file took", time.time() - start_time, "seconds")
