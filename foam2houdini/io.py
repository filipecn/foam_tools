from pyrr import Vector3
from foam2houdini.logging import *


def read_foam_poly_mesh_points(filename) -> [Vector3]:
    log_info("[foam poly mesh] Reading points from %s" % filename)
    points = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        offset = 18
        point_count = int(lines[offset])
        offset += 2
        for i in range(point_count):
            points.append(Vector3([float(x.strip('()')) for x in lines[offset].split()]))
            offset += 1
    log_info("[foam poly mesh] ... %d points read." % len(points))
    return points


def read_foam_poly_mesh_faces(filename) -> [[int]]:
    log_info("[foam poly mesh] Reading faces from %s" % filename)
    faces = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        offset = 18
        face_count = int(lines[offset])
        offset += 2
        for i in range(face_count):
            line = lines[offset]
            face_size = int(line[:line.find('(')])
            faces.append([int(x) for x in line[line.find('(') + 1: line.find(')')].split()])
            offset += 1
    log_info("[foam poly mesh] ... %d faces read." % len(faces))
    return faces


def read_foam_poly_mesh_owner(filename) -> [int]:
    log_info("[foam poly mesh] Reading owners from %s" % filename)
    owners = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        offset = 19
        face_count = int(lines[offset])
        offset += 2
        for i in range(face_count):
            owners.append(int(lines[offset]))
            offset += 1
    log_info("[foam poly mesh] ... %d owners read." % len(owners))
    return owners


def read_foam_poly_mesh_neighbor(filename) -> [int]:
    log_info("[foam poly mesh] Reading neighbors from %s" % filename)
    neighbors = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        offset = 19
        face_count = int(lines[offset])
        offset += 2
        for i in range(face_count):
            neighbors.append(int(lines[offset]))
            offset += 1
    log_info("[foam poly mesh] ... %d neighbors read." % len(neighbors))
    return neighbors


def read_foam_sim_variable_values(filename, do_log=False) -> [float]:
    if do_log:
        log_info("[foam] Reading field values from %s" % filename)
    values = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        offset = 21
        cell_count = int(lines[offset])
        offset += 2
        for i in range(cell_count):
            values.append(float(lines[offset]))
            offset += 1
    if do_log:
        log_info("[foam] ... %d values read." % len(values))
    return values
