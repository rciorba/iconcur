import random
from PIL import Image


SIZE = 1024
MAX_ITER = 100


img = Image.new("RGB", (SIZE, SIZE))


def complex_2_carthesian(point):
    x = int((point.real+2)/3 * SIZE)
    y = int((point.imag+1.5)/3 * SIZE)
    return x, y


def render(orbit):
    for point in orbit:
        x, y  = complex_2_carthesian(point)
        if (0 <= x < SIZE) and (0 <= y < SIZE):
            pixel_value = img.getpixel((x, y))[0] + 1
            img.putpixel((x, y), (pixel_value, pixel_value, pixel_value))


def get_point():
    return complex(-2+random.random()*3, -1+random.random()*2)


def brot_orbit(point):
    iterations = 0
    orbit = []
    z = point
    while len(orbit) < MAX_ITER and z.imag**2 + z.real**2 < 4:
        orbit.append(z)
        z = z**2 + point
    return orbit

def main():
    try:
        while 1:
            point = get_point()
            orbit = brot_orbit(point)
            if len(orbit) == MAX_ITER:
                render(orbit)
    except KeyboardInterrupt:
        img.save("brot.bmp", "BMP")

if __name__ == "__main__":
    main()
