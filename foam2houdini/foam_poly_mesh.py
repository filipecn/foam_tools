from pyrr import Vector3, aabb
from foam2houdini.logging import *
import foam2houdini.io as io
from pathlib import Path
import numpy as np


class FoamPolyMesh:
    vertices: [Vector3]
    faces: [[int]]
    owners: [int]
    neighbors: [int]
    cells: []

    def __init__(self, dir_path: Path):
        # read points
        #############
        self.vertices = io.read_foam_poly_mesh_points(dir_path / "points")
        self.faces = io.read_foam_poly_mesh_faces(dir_path / "faces")
        self.owners = io.read_foam_poly_mesh_owner(dir_path / "owner")
        self.neighbors = io.read_foam_poly_mesh_neighbor(dir_path / "neighbour")
        # setup cells
        #############
        # iterate over faces and register each face to its owner cell
        max_cell_index = max(self.owners)
        self.cells = [[] for i in range(max_cell_index + 1)]
        for i in range(len(self.owners)):
            self.cells[self.owners[i]].append(i)
        # we also need to iterate neighbours as well
        for i in range(len(self.neighbors)):
            self.cells[self.neighbors[i]].append(i)

    def cell_vertices(self, cell_id) -> set:
        vertices = set()
        if 0 <= cell_id < len(self.cells):
            for f in self.cells[cell_id]:
                for v in self.faces[f]:
                    vertices.add(v)
        else:
            log_error("[cell center] Invalid cell id")
        return vertices

    def cell_center(self, cell_id: int) -> Vector3:
        if 0 > cell_id or cell_id >= len(self.cells):
            log_error("[cell center] Invalid cell id")
            return Vector3()
        center = Vector3()
        # compute centroid from face vertices
        vertices = self.cell_vertices(cell_id)
        for v in vertices:
            center += self.vertices[v]
        return center / len(vertices)

    def bounds(self):
        return aabb.create_from_points(self.vertices)

    def cell_bounds(self, cell_id):
        if 0 > cell_id or cell_id >= len(self.cells):
            log_error("[cell center] Invalid cell id")
            return Vector3()
        center = Vector3()
        vertices = self.cell_vertices(cell_id)
        return aabb.create_from_points([self.vertices[v] for v in vertices])
