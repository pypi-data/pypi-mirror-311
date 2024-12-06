from imgeditpy import PPMImage
import math


def rotate_ppm(image, angle=90, clockwise=True):
    theta = math.radians(angle % 360)
    width, height = image.width, image.height
    x0 = width // 2
    y0 = height // 2
    rotated_pixels = [(0, 0, 0)] * (width * height)
    if clockwise:
        for y in range(height):
            for x in range(width):

                new_x = int(math.cos(theta) * (x - x0) - math.sin(theta) * (y - y0) + x0)
                new_y = int(math.sin(theta) * (x - x0) + math.cos(theta) * (y - y0) + y0)

                if 0 <= new_x < width and 0 <= new_y < height:
                    rotated_pixels[new_y * width + new_x] = image.pixels[y * width + x]

    else:
        for i in range(height):
            for j in range(width):

                new_x = int(math.cos(theta) * (j - x0) + math.sin(theta) * (i - y0) + x0)
                new_y = int(-math.sin(theta) * (j - x0) + math.cos(theta) * (i - y0) + y0)

                if 0 <= new_x < width and 0 <= new_y < height:
                    rotated_pixels[new_y * width + new_x] = image.pixels[i * width + j]
    return PPMImage(width=width, height=height, max_color=image.max_color, pixels=rotated_pixels)


def resize_ppm(image, new_width=100, new_height=100):
    pixels = image.pixels
    resized_pixels = []
    x_ratio = image.width / new_width
    y_ratio = image.height / new_height

    for i in range(new_height):
        for j in range(new_width):
            x = int(j * x_ratio)
            y = int(i * y_ratio)
            resized_pixels.append(pixels[y * image.width + x])

    return PPMImage(new_width, new_height, image.max_color, resized_pixels)


def flip(image):
    return PPMImage(image.width, image.height, image.max_color, image.pixels[::-1])


def stretch_ppm(image, width_factor=1, height_factor=1):
    new_height = height_factor * image.height
    new_width = width_factor * image.width
    return resize_ppm(image, new_width, new_height)


def crop_ppm(image, *parameters, crop_option="circle"):
    width, height, max_color, pixels = image.width, image.height, image.max_color, image.pixels
    cropped_pixels = []
    x_centre, y_centre = width // 2, height // 2

    if crop_option == "circle":
        radius = parameters[0]//2
        for y in range(height):
            for x in range(width):

                if ((x - x_centre) ** 2 + (y - y_centre) ** 2) ** 0.5 <= radius:
                    cropped_pixels.append(pixels[(y * width) + x])
                else:
                    cropped_pixels.append((max_color, max_color, max_color))

    elif crop_option == "heart":
        scale = parameters[0] // 30
        for y in range(height):
            for x in range(width):
                if (((x - x_centre) ** 2 + (y_centre - y) ** 2 - (scale ** 5)) ** 3 <= (scale ** 3) * (
                        (x - x_centre) ** 2) * ((y_centre - y) ** 3)):
                    cropped_pixels.append(pixels[(y * width) + x])
                else:
                    cropped_pixels.append((max_color, max_color, max_color))

    elif crop_option == "triangle":
        def area(x1, y1, x2, y2, x3, y3):
            return 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

        side = parameters[0]
        top_vertex = (x_centre, y_centre + (3 ** 0.5) / 4 * side)
        bottom_left_vertex = (x_centre - (side / 2), y_centre - ((3 ** 0.5) / 4 * side))
        bottom_right_vertex = (x_centre + side / 2, y_centre - ((3 ** 0.5) / 4 * side))
        total_area = area(top_vertex[0], top_vertex[1], bottom_left_vertex[0], bottom_left_vertex[1],
                          bottom_right_vertex[0], bottom_right_vertex[1])
        for y in range(height):
            for x in range(width):
                area1 = area(x, y, top_vertex[0], top_vertex[1], bottom_left_vertex[0], bottom_left_vertex[1])
                area2 = area(x, y, top_vertex[0], top_vertex[1], bottom_right_vertex[0], bottom_right_vertex[1])
                area3 = area(x, y, bottom_right_vertex[0], bottom_right_vertex[1], bottom_left_vertex[0],
                             bottom_left_vertex[1])
                if area1 + area2 + area3 == total_area:
                    cropped_pixels.append(pixels[y * width + x])
                else:
                    cropped_pixels.append((max_color, max_color, max_color))

    return PPMImage(width, height, max_color, cropped_pixels)
