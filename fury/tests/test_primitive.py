import numpy as np
import numpy.testing as npt
import fury.primitive as fp


def test_vertices_primitives():
    # Tests the default vertices of all the built in primitive shapes.
    l_primitives = [(fp.prim_square, (4, 3)),
                    (fp.prim_box, (8, 3)),
                    (fp.prim_star, np.shape(fp.prim_star()), -3, 3, -0.666666666667),
                    (fp.prim_rhombicuboctahedron, np.shape(fp.prim_rhombicuboctahedron()), -4, 4, 0)]

    for func, shape, min, max, mean in l_primitives:
        vertices, _ = func()
        npt.assert_equal(vertices.shape, shape)
        npt.assert_equal(np.mean(vertices), mean)
        npt.assert_equal(vertices.min(), min)
        npt.assert_equal(vertices.max(), max)

    vertices, _ = fp.prim_star(3)
    npt.assert_equal(vertices.shape, (12, 3))
    npt.assert_equal(np.mean(vertices), .11111111)
    npt.assert_equal(vertices.min(), -3)
    npt.assert_equal(vertices.max(), 3)



def test_triangles_primitives():
    l_primitives = [(fp.prim_square, (2, 3)),
                    (fp.prim_box, (12, 3))]

    for func, shape in l_primitives:
        vertices, triangles = func()
        npt.assert_equal(triangles.shape, shape)
        npt.assert_equal(list(set(np.concatenate(triangles, axis=None))),
                         list(range(len(vertices))))


def test_spheres_primitives():
    l_primitives = [('symmetric362', 362, 720), ('symmetric642', 642, 1280),
                    ('symmetric724', 724, 1444), ('repulsion724', 724, 1444),
                    ('repulsion100', 100, 196), ('repulsion200', 200, 396)]

    for name, nb_verts, nb_triangles in l_primitives:
        verts, faces = fp.prim_sphere(name)
        npt.assert_equal(verts.shape, (nb_verts, 3))
        npt.assert_almost_equal(np.mean(verts), 0)
        npt.assert_equal(len(faces), nb_triangles)
        npt.assert_equal(list(set(np.concatenate(faces, axis=None))),
                         list(range(len(verts))))

    npt.assert_raises(ValueError, fp.prim_sphere, 'sym362')


def test_superquadric_primitives():
    # test default, should be like a sphere 362
    sq_verts, sq_faces = fp.prim_superquadric()
    s_verts, s_faces = fp.prim_sphere('symmetric362')

    npt.assert_equal(sq_verts.shape, s_verts.shape)
    npt.assert_equal(sq_faces.shape, s_faces.shape)

    npt.assert_almost_equal(sq_verts, s_verts)

    # Apply roundness
    sq_verts, sq_faces = fp.prim_superquadric(roundness=(2, 3))
    npt.assert_equal(sq_verts.shape, s_verts.shape)
    npt.assert_equal(sq_faces.shape, s_faces.shape)

    # TODO: We need to check some superquadrics shape


def test_repeat_primitive():
    # init variables
    verts, faces = fp.prim_square()
    centers = np.array([[0, 0, 0], [5, 0, 0], [10, 0, 0]])
    dirs = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    colors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1.]])

    big_verts, big_faces, big_colors = fp.repeat_primitive(vertices=verts,
                                                           faces=faces,
                                                           centers=centers,
                                                           directions=dirs,
                                                           colors=colors)

    npt.assert_equal(big_verts.shape[0], verts.shape[0] * centers.shape[0])
    npt.assert_equal(big_faces.shape[0], faces.shape[0] * centers.shape[0])
    npt.assert_equal(big_colors.shape[0], verts.shape[0] * centers.shape[0])

    # TODO: Check the array content


def test_repeat_primitive_function():
    # init variables
    centers = np.array([[0, 0, 0], [5, 0, 0], [10, 0, 0]])
    dirs = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    colors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) * 255
    phi_theta = np.array([[1, 1], [1, 2], [2, 1]])

    res = fp.repeat_primitive_function(func=fp.prim_superquadric,
                                       centers=centers,
                                       func_args=phi_theta,
                                       directions=dirs,
                                       colors=colors)

    big_verts, big_faces, big_colors = res
