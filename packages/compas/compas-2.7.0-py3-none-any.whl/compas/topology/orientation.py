from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random

from compas.geometry import centroid_points
from compas.itertools import pairwise
from compas.topology import breadth_first_traverse


def _closest_faces(vertices, faces, nmax=10, radius=10.0):
    points = [centroid_points([vertices[index] for index in face]) for face in faces]

    k = min(len(faces), nmax)

    # determine the k closest faces for each face
    # each item in "closest" is
    # [0] the coordinates of the face centroid
    # [1] the index of the face in the list of face centroids
    # [2] the distance between the test point and the face centroid

    try:
        from scipy.spatial import cKDTree

    except Exception:
        try:
            from Rhino.Geometry import Point3d  # type: ignore
            from Rhino.Geometry import RTree  # type: ignore
            from Rhino.Geometry import Sphere  # type: ignore

        except Exception:
            from compas.geometry import KDTree

            tree = KDTree(points)
            closest = [tree.nearest_neighbors(point, k) for point in points]
            closest = [[index for xyz, index, d in nnbrs] for nnbrs in closest]

        else:
            tree = RTree()

            for i, point in enumerate(points):
                tree.Insert(Point3d(*point), i)

            def callback(sender, e):
                data = e.Tag
                data.append(e.Id)

            closest = []
            for i, point in enumerate(points):
                sphere = Sphere(Point3d(*point), radius)
                data = []
                tree.Search(sphere, callback, data)
                closest.append(data)

    else:
        tree = cKDTree(points)
        _, closest = tree.query(points, k=k, workers=-1)

    return closest


def _face_adjacency(vertices, faces, nmax=10, radius=10.0):
    closest = _closest_faces(vertices, faces, nmax=nmax, radius=radius)

    adjacency = {}

    for index, face in enumerate(faces):
        nbrs = []
        found = set()
        nnbrs = set(closest[index])

        for u, v in pairwise(face + face[0:1]):
            for nbr in nnbrs:
                if nbr == index:
                    continue
                if nbr in found:
                    continue

                for a, b in pairwise(faces[nbr] + faces[nbr][0:1]):
                    if v == a and u == b:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break

                for a, b in pairwise(faces[nbr] + faces[nbr][0:1]):
                    if u == a and v == b:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break

        adjacency[index] = nbrs

    return adjacency


def face_adjacency(points, faces):
    """Build a face adjacency dict.

    Parameters
    ----------
    points : list[point]
        The vertex locations of the faces.
    faces : list[list[int]]
        The faces defined as list of indices in the points list.

    Returns
    -------
    dict[int, list[int]]
        A dictionary mapping face identifiers (keys) to lists of neighboring faces.

    Notes
    -----
    This algorithm is used primarily to unify the cycle directions of the faces representing a mesh.
    The premise is that the faces don't have unified cycle directions yet,
    and therefore cannot be used to construct the adjacency structure. The algorithm is thus
    purely geometrical, but uses a spatial indexing tree to speed up the search.

    """
    f = len(faces)

    if f > 100:
        return _face_adjacency(points, faces)

    adjacency = {}

    for i, vertices in enumerate(faces):
        nbrs = []
        found = set()

        for u, v in pairwise(vertices + vertices[0:1]):
            for j, _ in enumerate(faces):
                if i == j:
                    continue
                if j in found:
                    continue

                for a, b in pairwise(faces[j] + faces[j][0:1]):
                    if v == a and u == b:
                        nbrs.append(j)
                        found.add(j)
                        break

                for a, b in pairwise(faces[j] + faces[j][0:1]):
                    if u == a and v == b:
                        nbrs.append(j)
                        found.add(j)
                        break

        adjacency[i] = nbrs

    return adjacency


def unify_cycles(vertices, faces, root=None):
    """Unify the cycle directions of all faces.

    Unified cycle directions is a necessary condition for the data structure to
    work properly. When in doubt, run this function on your mesh.

    Parameters
    ----------
    vertices : list[[float, float, float]]
        The vertex coordinates of the mesh.
    faces : list[list[int]]
        The faces of the mesh defined as lists of vertex indices.
    root : str, optional
        The key of the root face.

    Returns
    -------
    dict
        A halfedge dictionary linking pairs of vertices to faces.

    Raises
    ------
    Exception
        If no all faces are included in the unnification process.

    """

    def unify(node, nbr):
        # find the common edge
        for u, v in pairwise(faces[nbr] + faces[nbr][0:1]):
            if u in faces[node] and v in faces[node]:
                # node and nbr have edge u-v in common
                i = faces[node].index(u)
                j = faces[node].index(v)
                if i == j - 1 or (j == 0 and u == faces[node][-1]):
                    # if the traversal of a neighboring halfedge
                    # is in the same direction
                    # flip the neighbor
                    faces[nbr][:] = faces[nbr][::-1]
                    return

    if root is None:
        root = random.choice(list(range(len(faces))))

    adj = face_adjacency(vertices, faces)  # this is the only place where the vertex coordinates are used

    visited = breadth_first_traverse(adj, root, unify)

    if len(list(visited)) != len(faces):
        raise Exception("Not all faces were visited.")
