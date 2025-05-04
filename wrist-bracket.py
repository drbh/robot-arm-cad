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
)
from ocp_vscode import show_object
import time
import copy

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


wall_thickness = 2.0
# gap_width = 55
gap_width = 50
height = 25.0
depth = 20.0


# similar u shapw with boxes
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
c_shape = outer_box - inner_box
c_shape = Rot(0, 180, 0) * c_shape
c_shape = Pos(0, 0, -height - wall_thickness - 1) * c_shape

inner_mount = Box(
    width=gap_width,
    length=depth,
    height=6,
)

inner_mount_cut = Box(
    width=gap_width - 10,
    length=depth + 4 * wall_thickness,
    height=6,
)

inner_mount_cut = Pos(0, 0, -39) * inner_mount_cut

inner_mount = Pos(0, 0, -39) * inner_mount

inner_mount = inner_mount - inner_mount_cut

screw_holes = Cylinder(radius=1.5, height=8)

screw_holes2 = copy.copy(screw_holes)

screw_holes = Pos(8, 0, 0) * screw_holes

screw_holes = screw_holes + screw_holes2

screw_holes = Pos(-4, -22.5, -40) * screw_holes

screw_holes_other_side = copy.copy(screw_holes)

screw_holes_other_side = Pos(0, gap_width - 5, 0) * screw_holes_other_side

inner_mount = inner_mount - screw_holes - screw_holes_other_side
wrist_backet = inner_mount + c_shape + c_shape_1

show_object(
    wrist_backet,
    name="wrist_backet",
    options=dict(color="blue", alpha=0.5),
)

start_time = time.time()
exporter = Mesher()
exporter.add_shape(wrist_backet, part_number="wrist_backet")
exporter.write("output/wrist-backet.3mf")
print("Total Exporting 3mf file took", time.time() - start_time, "seconds")
