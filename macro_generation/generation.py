import gdstk
import random
import math
min_metal6_width = 1.7 #1.64  # Minimum Metal6 width in microns
min_metal6_spacing = 1.7 #1.64 


length = 8  # Reduced from 8
avg_width = 2  # Reduced from 3
gap = 1  # Reduced from 1

sizeX = 13
sizeY = 10


x_width = [4] * sizeX
y_width = [4] * sizeY



structure = [[random.randint(0, 1) for _ in range(sizeY)] for _ in range(sizeX)]



# The GDSII file is called a library, which contains multiple cells.
lib = gdstk.Library()

# Geometry must be placed in cells.
cell = lib.new_cell("my_logo")

for x in range(sizeX):
    for y in range(sizeY):
        if structure[x][y] == 1:
            
            stitch = gdstk.rectangle((x*length, y*length+length/2-avg_width/2), (x*length+length, y*length+length/2+avg_width/2), layer=1, datatype=22)
            stitch2 = stitch.copy()
            stitch.rotate(45, center=(x*length+length/2, y*length+length/2))
            stitch2.rotate(-45, center=(x*length+length/2, y*length+length/2))

            
            combined = gdstk.boolean(stitch, stitch2, 'or', layer=1, datatype=22)
            for c in combined:
                c.fillet(0.8)
                cell.add(c)
        


# Add PR boundary (placement and routing boundary)
# Layer 235, datatype 4 for sky130 PR boundary
pr_boundary = gdstk.rectangle((0, 0), (length,length), layer=235, datatype=4)
cell.add(pr_boundary)

# active_dist = 1.5
# active_size = 3.0 
# overhang = 0.18

# for i in range(36):
#     for j in range(27):
#         tx = i * (active_size + active_dist)
#         ty = j * (active_size + active_dist)

       
#         rect1 = gdstk.rectangle((tx, ty), (tx+active_size, ty+active_size), layer=1, datatype=22)
#         cell.add(rect1)
        
#         poly_rect = gdstk.rectangle((tx-overhang, ty-overhang), (tx+active_size+overhang, ty+active_size+overhang), layer=5, datatype=22)
#         cell.add(poly_rect)

        




# Generate LEF file
def write_lef_file(filename, cell_name, cell_bounds, pins):
    """Write a LEF file for the cell"""
    with open(filename, 'w') as f:
        f.write("# LEF file generated for {}\n".format(cell_name))
        f.write("VERSION 5.8 ;\n")
        f.write("NAMESCASESENSITIVE ON ;\n")
        f.write("DIVIDERCHAR \"/\" ;\n")
        f.write("BUSBITCHARS \"[]\" ;\n")
        f.write("UNITS\n")
        f.write("   DATABASE MICRONS 1000 ;\n")
        f.write("END UNITS\n\n")
        
        # Define the cell
        f.write("MACRO {}\n".format(cell_name))
        f.write("   CLASS BLOCK ;\n")
        f.write("   FOREIGN {} 0 0 ;\n".format(cell_name))
        f.write("   SIZE {:.3f} BY {:.3f} ;\n".format(cell_bounds[2] - cell_bounds[0], cell_bounds[3] - cell_bounds[1]))
        f.write("   SYMMETRY X Y ;\n")
        
        # No pins - pure blackbox module
        # No OBS section - keep LEF simple
        
        f.write("END {}\n".format(cell_name))

# Calculate cell bounds (back to original size)
cell_width = sizeY*length  # 32 microns
cell_height = sizeX*length  # 32 microns
cell_bounds = (0, 0, cell_width, cell_height)

# Write LEF file
write_lef_file("../macros/my_logo.lef", "my_logo", cell_bounds, [])

# Save the library in a GDSII or OASIS file.
lib.write_gds("../macros/my_logo.gds")

# Optionally, save an image of the cell as SVG.
cell.write_svg("../macros/my_logo.svg")