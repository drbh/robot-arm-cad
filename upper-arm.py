import numpy as np
from build123d import Pos, Box, Rot, Align, fillet, Plane, Axis, Mesher, Cylinder
import time
import copy
from ocp_vscode import show_object


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

mg996r_body = Box(40, 45, 20)

mg966r_flange = Box(55, 5, 20)
mg996r_flange = Pos(0, 5.5 + 1.55, 0) * mg966r_flange

mg996r_body = mg996r_body + mg996r_flange

mg996r_body = Pos(0, -0.5 - 1.55, 0) * mg996r_body

mg996r_spindle = Cylinder(3, 10)
mg996r_spindle = Rot(90, 0, 0) * Pos(12.5, 0, -22) * mg996r_spindle

mg996r_body = mg996r_body + mg996r_spindle

# back C
h = 20
back_c = Box(10, h, 33)
pos_hole_on_arm = 10
back_c = Pos(pos_hole_on_arm, -h + 2.5, 0) * back_c

back_c_inner = Pos(pos_hole_on_arm, -h + 3.75, 0) * Box(10, h - 2.5, 20)

mg996r_spindle2 = Cylinder(4, 10)
mg996r_spindle2 = Rot(90, 0, 0) * Pos(pos_hole_on_arm, 0, -22) * mg996r_spindle2

back_c_spindel = Pos(0, -40 - 10, 0) * mg996r_spindle2

back_c = back_c + back_c_spindel - back_c_inner

screw_hole = Cylinder(1.5, 100)
screw_hole = Rot(90, 0, 0) * Pos(pos_hole_on_arm, 13.5, 0) * screw_hole

screw_hole2 = Pos(0, 0, -27) * screw_hole

screws = screw_hole + screw_hole2

bracket = bracket - screws
bracket2 = bracket2 - screws
back_c = back_c - screws


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
back_c = back_c - big_screws


base = Box(45, 10 + 8, 33 + 8)
base = Pos(-50, -2.5, 0) * base

base = base - bracket
base = base - bracket2

# -50x and -2.5y
through_hole = Cylinder(1.5, 100)
through_hole = Pos(-48.5, 0, 13.5) * Rot(90, 0, 0) * through_hole

through_hole2 = Pos(0, 0, -27) * through_hole
through_hole = through_hole + through_hole2

base = base - through_hole

# for mounting
l = 30

lower_mounting = Box(40, l, 41)
lower_mounting = Pos(-52.5, -l * 2 / 3, 0) * lower_mounting

lower_mounting_cut = Box(30, 20, 100)
lower_mounting_cut = Pos(-52.5 + 5, -21, 0) * lower_mounting_cut
lower_mounting_cut = Pos(0, 0, -10) * lower_mounting_cut
lower_mounting = lower_mounting - lower_mounting_cut

mounting_base = copy.copy(base) + lower_mounting

# for extension
flipped_base = Pos(-140, 0, 0) * Rot(0, 180, 0) * base
two_sided = base + flipped_base

# middle cutout since block is too thick
middle_cutout = Box(20, 50, 30)
middle_cutout = Pos(-50 - 20, 0, 0) * middle_cutout

middle_cutout2 = Box(70, 50, 10)
middle_cutout2 = Pos(-50 - 20, 0, 0) * middle_cutout2

two_sided = two_sided - middle_cutout - middle_cutout2

upper_arm = bracket + Rot(180, 180, 0) * Pos(105, 5, 0) * bracket

show_object(upper_arm, name="Bracket", options=dict(color="dodgerblue"))

export = True

show_object(back_c, name="Back C", options=dict(color="blue", alpha=0.5))

if export:
    start_time = time.time()
    exporter = Mesher()

    exporter.add_shape(back_c, part_number="A")
    exporter.add_shape(upper_arm, part_number="A")
    exporter.write("output/upper-arm.3mf")
    print("Total Exporting 3mf file took", time.time() - start_time, "seconds")
