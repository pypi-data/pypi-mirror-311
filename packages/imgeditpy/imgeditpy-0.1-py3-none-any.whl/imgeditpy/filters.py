from imgeditpy import PPMImage
import random


def grayscale_filter_ppm(image):
    gray_pixels = []

    for r, g, b in image.pixels:
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        gray_pixels.append((gray, gray, gray))
    return PPMImage(image.width, image.height, image.max_color, gray_pixels)


def invert_filter_ppm(image):
    inverted_pixels = []

    max_pixel = image.max_color
    for r, g, b in image.pixels:
        inverted_pixels.append((
            max_pixel - r,
            max_pixel - g,
            max_pixel - b
        ))
    return PPMImage(image.width, image.height, image.max_color, inverted_pixels)


def adjust_brightness_ppm(image, factor=1):
    adjusted_brightness_pixels = []

    for r, g, b in image.pixels:
        adjusted_brightness_pixels.append((
            min(int(r * factor), 255),
            min(int(g * factor), 255),
            min(int(b * factor), 255),
        ))
    return PPMImage(image.width, image.height, image.max_color, adjusted_brightness_pixels)


def snp_noise_ppm(image, intensity=0.2):
    noisy_pixels = []
    for each in image.pixels:
        if random.random() < intensity:
            noisy_pixels.append(
                tuple([0, 0, 0]) if random.random() < 0.5 else tuple(
                    [image.max_color, image.max_color, image.max_color]))
        else:
            noisy_pixels.append(each)
    return PPMImage(image.width, image.height, image.max_color, noisy_pixels)


def median_filter_ppm(image):
    def median(lst):
        sorted_lst = sorted(lst)
        n = len(sorted_lst)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_lst[mid - 1] + sorted_lst[mid]) // 2
        return sorted_lst[mid]

    def get_neighbors(image_2d, x, y, width, height):
        neighbors = []
        for i in range(max(0, y - 1), min(height, y + 2)):
            for j in range(max(0, x - 1), min(width, x + 2)):
                neighbors.append(image_2d[i][j])
        return neighbors

    def apply_median_filter(image_1d, width, height):
        image_2d = [image_1d[i * width:(i + 1) * width] for i in range(height)]
        filtered_image_2d = []
        for y in range(height):
            for x in range(width):
                neighbors = get_neighbors(image_2d, x, y, width, height)

                reds = [pixel[0] for pixel in neighbors]
                greens = [pixel[1] for pixel in neighbors]
                blues = [pixel[2] for pixel in neighbors]

                median_red = median(reds)
                median_green = median(greens)
                median_blue = median(blues)

                filtered_image_2d.append(tuple([median_red, median_green, median_blue]))

        return filtered_image_2d

    return PPMImage(image.width, image.height, image.max_color,
                    apply_median_filter(image.pixels, image.width, image.height))


def threshold_ppm(image):
    def calculate_histogram(grayscale_pixels):
        histogram = [0] * 256
        for intensity in grayscale_pixels[0]:
            histogram[intensity] += 1
        return histogram

    def otsu_threshold(histogram, total_pixels):
        sum_total = sum(i * histogram[i] for i in range(256))
        sum_background = 0
        weight_background = 0
        max_between_class_variance = 0
        best_threshold = 0

        for each_threshold in range(256):
            weight_background += histogram[each_threshold]
            if weight_background == 0:
                continue

            weight_foreground = total_pixels - weight_background
            if weight_foreground == 0:
                break

            sum_background += each_threshold * histogram[each_threshold]
            mean_background = sum_background / weight_background
            mean_foreground = (sum_total - sum_background) / weight_foreground

            between_class_variance = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
            if between_class_variance > max_between_class_variance:
                max_between_class_variance = between_class_variance
                best_threshold = each_threshold

        return best_threshold

    max_color = image.max_color
    gray_ppm = grayscale_filter_ppm(image)
    hist = calculate_histogram(gray_ppm.pixels)
    optimal_threshold = otsu_threshold(hist, image.width * image.height)

    threshold_pixels = []
    for each in image.pixels:
        r, g, b = each
        if int(0.299 * r + 0.587 * g + 0.114 * b) > optimal_threshold:
            threshold_pixels.append((max_color, max_color, max_color))
        else:
            threshold_pixels.append((0, 0, 0))

    return PPMImage(image.width, image.height, max_color, threshold_pixels)


def colour_extract_from_ppm(image, target_color, tolerance=30):
    width = image.width
    height = image.height
    pixels = image.pixels
    object_pixels = [(255, 255, 255) for _ in range(width * height)]
    primary_colour = target_color.index(max(target_color))
    mask = [2 if i == primary_colour else 1 for i in range(3)]
    print(mask)
    for i, (r, g, b) in enumerate(pixels):

        if ((abs(r - target_color[0]) < tolerance * mask[0]) and
                (abs(g - target_color[1]) < tolerance * mask[1]) and
                (abs(b - target_color[2]) < tolerance * mask[2])):
            object_pixels[i] = (r, g, b)  # Copy object pixel to output

    return PPMImage(width, height, image.max_color, object_pixels)


def brightness_extract_from_ppm(image, target_brightness_range):
    width = image.width
    height = image.height
    pixels = image.pixels
    object_pixels = [(255, 255, 255) for _ in range(width * height)]

    for i, (r, g, b) in enumerate(pixels):

        if (r + g + b) // 3 in range(target_brightness_range[0], target_brightness_range[1]):
            object_pixels[i] = (r, g, b)

    return PPMImage(width, height, image.max_color, object_pixels)
