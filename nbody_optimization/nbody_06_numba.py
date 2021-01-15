import timeit
import numba
#SUPRESS NUMBA DEPRECIATION WARNINGS
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

"""
    N-body simulation.
"""

PI = 3.14159265358979323
SOLAR_MASS = 4 * PI * PI
DAYS_PER_YEAR = 365.24

BODIES = {
    'sun': ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], SOLAR_MASS),

    'jupiter': ([4.84143144246472090e+00,
                 -1.16032004402742839e+00,
                 -1.03622044471123109e-01],
                [1.66007664274403694e-03 * DAYS_PER_YEAR,
                 7.69901118419740425e-03 * DAYS_PER_YEAR,
                 -6.90460016972063023e-05 * DAYS_PER_YEAR],
                9.54791938424326609e-04 * SOLAR_MASS),

    'saturn': ([8.34336671824457987e+00,
                4.12479856412430479e+00,
                -4.03523417114321381e-01],
               [-2.76742510726862411e-03 * DAYS_PER_YEAR,
                4.99852801234917238e-03 * DAYS_PER_YEAR,
                2.30417297573763929e-05 * DAYS_PER_YEAR],
               2.85885980666130812e-04 * SOLAR_MASS),

    'uranus': ([1.28943695621391310e+01,
                -1.51111514016986312e+01,
                -2.23307578892655734e-01],
               [2.96460137564761618e-03 * DAYS_PER_YEAR,
                2.37847173959480950e-03 * DAYS_PER_YEAR,
                -2.96589568540237556e-05 * DAYS_PER_YEAR],
               4.36624404335156298e-05 * SOLAR_MASS),

    'neptune': ([1.53796971148509165e+01,
                 -2.59193146099879641e+01,
                 1.79258772950371181e-01],
                [2.68067772490389322e-03 * DAYS_PER_YEAR,
                 1.62824170038242295e-03 * DAYS_PER_YEAR,
                 -9.51592254519715870e-05 * DAYS_PER_YEAR],
                5.15138902046611451e-05 * SOLAR_MASS)}

@numba.jit()
def combinations_r2(iterable):
    combination_list = []
    num_items = len(iterable)

    for i in range(num_items):
        if i < num_items:
            val1 = iterable[i]
            for val2 in iterable[i + 1:]:
                tup = (val1, val2)
                combination_list.append(tup)

    return combination_list

@numba.njit(numba.types.UniTuple(numba.float64, 3) (numba.float64, numba.float64, numba.float64, numba.float64, numba.float64, numba.float64) )
def compute_deltas(x1, x2, y1, y2, z1, z2):
    return (x1-x2, y1-y2, z1-z2)

@numba.njit(numba.float64(numba.float64, numba.float64, numba.float64, numba.float64, numba.float64))
def compute_b(m, dt, dx, dy, dz):
    mag = dt * ((dx * dx + dy * dy + dz * dz) ** (-1.5))
    #mag = dt * (sum([d * d for d in [dx, dy, dz]]) ** (-1.5))
    return m * mag

#@numba.jit()
def update_vs(v1, v2, dt, dx, dy, dz, m1, m2, bodies_data, body1, body2):

    b1 = compute_b(m2, dt, dx, dy, dz) #NOT A TYPO: B1 DOES TAKE M2 & B2 DOES TAKE M1
    b2 = compute_b(m1, dt, dx, dy, dz) #NOT A TYPO: B1 DOES TAKE M2 & B2 DOES TAKE M1

    v1[0] -= dx * b1
    v1[1] -= dy * b1
    v1[2] -= dz * b1
    v2[0] += dx * b2
    v2[1] += dy * b2
    v2[2] += dz * b2

    return bodies_data

#@numba.jit()
def update_rs(dt, bodies_data, body):
    (r, [vx, vy, vz], m) = bodies_data[body]
    r[0] += dt * vx
    r[1] += dt * vy
    r[2] += dt * vz

    return bodies_data

#@numba.jit()
def advance(dt, loops, iterations, bodies_data):
    '''
        advance the system one timestep
    '''
    body_names = list(bodies_data.keys())
    for _ in range(loops):
        for _ in range(iterations):

            for combination in combinations_r2(body_names):
                body1 = combination[0]
                body2 = combination[1]
                ([x1, y1, z1], v1, m1) = bodies_data[body1]
                ([x2, y2, z2], v2, m2) = bodies_data[body2]
                (dx, dy, dz) = compute_deltas(x1, x2, y1, y2, z1, z2)
                bodies_data = update_vs(v1, v2, dt, dx, dy, dz, m1, m2, bodies_data, body1, body2)

            for body in body_names:
                bodies_data = update_rs(dt, bodies_data, body)

        print(report_energy(bodies_data))

#@numba.jit()
def report_energy(bodies_data, e=0.0):
    '''
        compute the energy and return it so that it can be printed
    '''
    body_names = list(bodies_data.keys())
    for combination in combinations_r2(body_names):
        body1 = combination[0]
        body2 = combination[1]
        ((x1, y1, z1), v1, m1) = bodies_data[body1]
        ((x2, y2, z2), v2, m2) = bodies_data[body2]
        (dx, dy, dz) = compute_deltas(x1, x2, y1, y2, z1, z2)
        e -= (m1 * m2) / (sum([d * d for d in [dx, dy, dz]]) ** 0.5)

    for body in body_names:
        (r, [vx, vy, vz], m) = bodies_data[body]
        e += m * sum(v*v for v in [vx, vy, vz]) / 2.

    return e

#@numba.jit()
def offset_momentum(ref, bodies_data, px=0.0, py=0.0, pz=0.0):
    '''
        ref is the body in the center of the system
        offset values from this reference
    '''
    for body in bodies_data.keys():
        (r, [vx, vy, vz], m) = bodies_data[body]
        px -= vx * m
        py -= vy * m
        pz -= vz * m

    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m

    return bodies_data

#@numba.jit()
def nbody(loops, reference, iterations, bodies_data):
    '''
        nbody simulation
        loops - number of loops to run
        reference - body at center of system
        iterations - number of timesteps to advance
    '''
    # Set up global state
    bodies_data = offset_momentum(bodies_data[reference], bodies_data)
    advance(0.01, loops, iterations, bodies_data)

def wrapped_test_function():
    nbody(100, 'sun', 20000, BODIES)

if __name__ == '__main__':

    num_tests = 1
    num_repeats = 3

    time_vector = timeit.repeat("wrapped_test_function()", number = num_tests, repeat = num_repeats, globals=globals())
    time_best = min(time_vector)

    print("Best Time: {:.2f}".format(time_best))
