__author__ = 'tieni'

import numpy as np
cimport numpy as np

def execute(id_map, np.ndarray[np.int64_t, ndim=3] seg):
    cdef np.ndarray new_seg = np.empty_like(seg)
    cdef int shape_x = seg.shape[0]
    cdef int shape_y = seg.shape[1]
    cdef int shape_z = seg.shape[2]

    y_list = range(shape_y)
    z_list = range(shape_z)

    cdef int last_id = 0
    cdef int last_mapped_id = 0
    cdef int x_iter, z_iter, y_iter
    cdef int value
    for x_iter in range(shape_x):
        for y_iter in y_list:
            for z_iter in z_list:
                value = seg[x_iter, y_iter, z_iter]
                if last_id != value:
                    last_mapped_id = 1#id_map[value]

                new_seg[x_iter, y_iter, z_iter/2] = last_mapped_id
                last_id = value
    return new_seg