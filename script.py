from smithers.io.stlhandler import STLHandler
from src.read_spatial_info import dimension, diameter, min_max, DataWrapper
from src.generate_cylinders import (
    generate_cylinders_obj,
    compute_cylinder_dimensions,
)
from src.openfoam_parametrizer import generate_openfoam_configuration_dicts
from pathlib import Path
import sys
from shutil import copyfile

# PARAMETERS
# 1: the path to the OpenFOAM folder (with the subfolders system, constant, etc)
# 2: the path to the propeller.obj

openfoam_folder = sys.argv[1]
openfoam_path = Path(openfoam_folder)

propeller_path = sys.argv[2]

# copy the propeller to the OpenFOAM folder
copyfile(propeller_path, str(openfoam_path / 'constant' / 'triSurface' / 'propeller.obj'))

# first of all we read the dimension of the propeller
data = DataWrapper(propeller_path)
propeller_dimension = dimension(data)
propeller_diameter = diameter(data)

# then we generate three cylinders
cylinder_dimensions = compute_cylinder_dimensions(
    scales=[
        [1.1, 3, 1.1],
        [2.5, 9, 2.5],
        [5, 12.7, 5],
    ],
    propeller_diameter=propeller_diameter,
)
miny, maxy = generate_cylinders_obj(
    dimensions=cylinder_dimensions,
    base_folder=str(openfoam_path / "constant" / "triSurface"),
)

# we take half of the diameter of the outer cylinder, plus an epsilon
maxx,maxz = cylinder_dimensions[-1][[0,2]]/2 + 0.1
minx,minz = (-maxx,-maxz)

# y is the length
yfactor = (0.21 + 0.81) * cylinder_dimensions[-1][1]

# then we generate the parametrized dictionaries
generate_openfoam_configuration_dicts(
    destination=openfoam_folder,
    # OpenFOAM parameters
    decompose_nx=4,
    decompose_ny=4,
    decompose_nz=4,
    minx=minx,
    maxx=maxx,
    miny=miny,
    maxy=maxy,
    minz=minz,
    maxz=maxz,
)

# potrei aver invertito inlet e outlet
