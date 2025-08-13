import cadquery as cq
from cadquery import exporters
import math

output_filename = "output.step"

# Parameters
plate_length = 6.562
plate_width = 2.100
plate_thickness = 0.240

corner_r1 = 0.62
corner_r2 = 0.50

chamfer_size = 0.150

hole_dia = 0.280
hole_count = 4
hole_spacing_x = 3.753
hole_offset_x = 0.625
hole_offset_y = plate_width / 2

center_hole_dia = 0.625
center_hole_offset_x = 5.398

slot_length = 1.40
slot_width = 0.625
slot_angle_deg = 31.5
slot_spacing = 1.287
slot_offset_x = 4.688
slot_offset_y = plate_width / 2

small_hole_dia = 0.18
small_hole_offset_x = 6.562 - 0.100
small_hole_offset_y = plate_width / 2

# Build rectangle and fillet corners
plate_outline = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Fillet all corners with small radius
plate_outline = plate_outline.edges("|Z").fillet(corner_r2)

# Select bottom left corner and fillet with large radius
# The bottom left corner is at (-(plate_length/2), -(plate_width/2))
bl_corner = (
    plate_outline.vertices(
        f"<X and <Y"
    )
)
plate_outline = bl_corner.fillet(corner_r1 - corner_r2)

plate = plate_outline

# 4x holes along X axis
hole_positions = []
for i in range(hole_count):
    x = hole_offset_x + i * (hole_spacing_x / (hole_count - 1))
    y = hole_offset_y
    hole_positions.append((x - plate_length/2, y - plate_width/2))

plate = plate.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_dia)

# Central large hole
plate = (
    plate.faces(">Z")
    .workplane()
    .center(center_hole_offset_x - plate_length/2, hole_offset_y - plate_width/2)
    .hole(center_hole_dia)
)

# Slotted holes (2 slots, angled)
slot_angle_rad = math.radians(slot_angle_deg)
slot_dx = math.cos(slot_angle_rad) * (slot_spacing / 2)
slot_dy = math.sin(slot_angle_rad) * (slot_spacing / 2)

slot_centers = [
    (slot_offset_x - slot_dx, slot_offset_y - slot_dy),
    (slot_offset_x + slot_dx, slot_offset_y + slot_dy),
]

for cx, cy in slot_centers:
    plate = (
        plate.faces(">Z")
        .workplane()
        .center(cx - plate_length/2, cy - plate_width/2)
        .slot2D(slot_length, slot_width, angle=slot_angle_deg)
        .cutBlind(-plate_thickness)
    )

# Small hole on right side
plate = (
    plate.faces(">Z")
    .workplane()
    .center(small_hole_offset_x - plate_length/2, small_hole_offset_y - plate_width/2)
    .hole(small_hole_dia)
)

# Chamfer bottom edge
plate = plate.edges("|Z and <Z").chamfer(chamfer_size)

assert plate.val().isValid(), "Model is not valid!"

exporters.export(plate, output_filename)