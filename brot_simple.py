import sys

from PIL import Image


SIZE = 1023
MAX_ITER = 100


img = Image.new("RGB", (SIZE+1, SIZE+1))


def carthesiza_2_complex(point):
    """maps the 0-SIZE range to -2 1 (x axis) and -1.5 1.5 (y axis)"""
    x, y = point
    size = float(SIZE)
    x = (-2 + (x/size)*3)
    y = (-1.5 + (y/size)*3)
    return complex(x, y)

def complex_2_carthesian(point):
    x = int((point.real+2)/3 * SIZE)
    y = int((point.imag+1.5)/3 * SIZE)
    return x, y


def render(x, y):
    # if (0 <= x < SIZE) and (0 <= y < SIZE):
    # x, y = complex_2_carthesian(point)
    # pixel_value = img.getpixel((x, y))[0] + 1
    img.putpixel((x, y), (255, 255, 255))


def brot_orbit(point):
    iterations = 0
    z = point
    while (iterations < MAX_ITER) and ((z.imag**2 + z.real**2) < 4):
        z = z**2 + point
        iterations += 1
    return iterations


def main():
    for x in xrange(SIZE +1):
        for y in xrange(SIZE +1):
            point = carthesiza_2_complex((x, y))
            iterations = brot_orbit(point)
            if iterations == MAX_ITER:
                render(x, y)
        #         sys.stdout.write(".")
        #         sys.stdout.flush()
        #     else:
        #         sys.stdout.write(" ")
        #         sys.stdout.flush()
        # print
    img.save("brot.bmp", "BMP")

if __name__ == "__main__":
    main()
