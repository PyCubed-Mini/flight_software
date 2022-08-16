try:
    from ulab.numpy import array
except ImportError:
    from numpy import array

eci_state = array([6871, -6571, -7071, 2, -10, 3])  # [x, y, z, vx, vy, vz]
