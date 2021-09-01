import argparse
from pathlib import Path
import sys
import os
from foam2houdini.logging import *
from foam2houdini.foam_poly_mesh import FoamPolyMesh
from foam2houdini.io import read_foam_sim_variable_values
import pyrr.matrix33 as mat33

sys.path.insert(1, "/usr/local/lib/python3.8/")
import pyopenvdb as vdb

if __name__ == "__main__":
    # program parameters
    parser = argparse.ArgumentParser(
        description="Tool for converting openfoam simulation files into OpenVDB grids")
    parser.add_argument('-i', '--input_dir', type=Path,
                        help="Path to OpenFoam case containing simulation frames")
    parser.add_argument('-v', '--foam_variable', type=str, help="Field name to extract density values")
    parser.add_argument('-o', "--output_dir", type=Path)
    args = parser.parse_args()
    # check input directory
    if not args.input_dir.exists():
        log_critical("Input directory not found.")
    else:
        if not (args.input_dir / "constant/polyMesh").exists():
            log_critical("Poly Mesh directory not found.")

    # load OpenFoam Poly Mesh
    foam_mesh = FoamPolyMesh(args.input_dir / "constant/polyMesh")
    # compute mesh bounds
    mesh_bounds = foam_mesh.bounds()
    # compute cell centers
    cell_centers = []
    cell_bounds = []
    for cell_id in range(len(foam_mesh.cells)):
        cell_centers.append(foam_mesh.cell_center(cell_id))
        cell_bounds.append(foam_mesh.cell_bounds(cell_id))

    # iterate over simulation steps and generate a vdb file for each
    frame_dirs = [d for d in os.listdir(args.input_dir) if d.isnumeric()]
    current_frame_id = 0
    for frame_dir in frame_dirs:
        log_progress(current_frame_id, len(frame_dirs))
        current_frame_id += 1
        # frame data file
        field_path = args.input_dir / frame_dir / args.foam_variable
        # check frame data
        if not field_path.exists():
            log_error('Frame data not found.')
            continue
        # load cell values
        values = read_foam_sim_variable_values(field_path)

        # prepare OpenVDB grid object
        vdb_grid = vdb.FloatGrid()
        vdb_grid.name = 'foam_field'
        # vdb_grid.fill(min=(100, 100, 100), max=(199, 199, 199), value=1.0)

        # Naive Algorithm
        #################
        # For each cell, fill it up with a regular vdb grid.
        # Since OpenVDB works with discrete coordinates we need to scale our points
        # by a particular factor. The scaled coordinates are then rounded to the closest
        # integer.
        dx = 0.1
        ijk_transform = mat33.create_from_scale(1 / dx)
        vdb_grid.transform = vdb.createLinearTransform(voxelSize=dx)
        acc = vdb_grid.getAccessor()
        # For each cell, compute the bounds of the cell in ijk coordinates
        # and iterate over all coordinates registering the cell density value
        for cell_id in range(len(cell_centers)):
            ijk_bounds = [[int(round(c)) for c in (ijk_transform * bounds_corner)[0]] for bounds_corner in
                          cell_bounds[cell_id]]
            # delta = [ijk_bounds[1][i] - ijk_bounds[0][i] for i in range(3)]
            # TODO: assuming cube cells
            vdb_grid.fill(min=tuple(ijk_bounds[0]), max=tuple(ijk_bounds[1]), value=values[cell_id])
            # ijk = ijk_transform * cell_centers[cell_id]
            # ijk = (int(ijk[0][0]), int(ijk[0][1]), int(ijk[0][2]))
            # acc.setValueOn(ijk, values[cell_id])
        del acc
        # output files
        if not args.output_dir.exists():
            args.output_dir.mkdir()
        vdb.write(str(args.output_dir / (frame_dir + '.vdb')), grids=[vdb_grid])
