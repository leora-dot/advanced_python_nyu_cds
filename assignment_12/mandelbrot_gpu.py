#
# A CUDA version to calculate the Mandelbrot set
#
from numba import cuda
import numpy as np
from pylab import imshow, show

@cuda.jit(device=True)
def mandel(x, y, max_iters):
    '''
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the
    Mandelbrot set given a fixed number of iterations.
    '''
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i

    return max_iters

#KERNAL DECLARATION
@cuda.jit
def compute_mandel(min_x, max_x, min_y, max_y, image, iters):

    #Calculate pixel size, as in original code

    height = image.shape[0]
    width = image.shape[1]

    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height

    #Calculate starting and ending coordinates for x,y

    start_x, start_y = cuda.grid(2)
    end_x = cuda.gridDim.x * cuda.blockDim.x
    end_y = cuda.gridDim.y * cuda.gridDim.y

    #Calculate mandel value for each element

    for x in range(start_x, width, end_x):
        real = min_x + x * pixel_size_x
        for y in range(start_y, height, end_y):
            imag = min_y + y * pixel_size_y
            image[y, x] = mandel(real, imag, iters)

if __name__ == '__main__':
    image = np.zeros((1024, 1536), dtype = np.uint8)
    blockdim = (32, 8)
    griddim = (32, 16)

    image_global_mem = cuda.to_device(image)
    compute_mandel[griddim, blockdim](-2.0, 1.0, -1.0, 1.0, image_global_mem, 20)
    image_global_mem.copy_to_host()
    imshow(image)
    show()
