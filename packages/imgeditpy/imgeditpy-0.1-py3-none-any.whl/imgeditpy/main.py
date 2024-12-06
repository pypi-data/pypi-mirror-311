import random
import subprocess
import tkinter as tk


class PPMImage:
    def __init__(self, width, height, max_color, pixels):
        self.width = width
        self.height = height
        self.max_color = max_color
        self.pixels = pixels

    @staticmethod
    def jpg_to_ppm(input_filename, output_filename):
        command = f"magick {input_filename} -compress none -define ppm:format=ascii {output_filename}"
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            print(f"Error occurred.{result.stderr} Make sure your inputs are valid")

    @staticmethod
    def ppm_to_jpg(input_filename, output_filename):
        command = f"magick {input_filename} -compress none {output_filename}"
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            print(f"Error occurred.{result.stderr} Make sure your inputs are valid")

    @staticmethod
    def read_ppm(filename):
        with open(filename, 'r') as f:
            format_type = f.readline().strip()
            if format_type != 'P3':
                raise ValueError("Only ASCII PPM (P3) format is supported")

            line = f.readline().strip()
            while line.startswith('#'):
                line = f.readline().strip()

            width, height = map(int, line.split())

            max_color = int(f.readline().strip())

            pixels = []
            for line in f:
                pixels.extend(map(int, line.split()))

            pixels = [(pixels[i], pixels[i + 1], pixels[i + 2]) for i in range(0, len(pixels), 3)]
            return PPMImage(width, height, max_color, pixels)

    @staticmethod
    def generate_white_ppm(width=100, height=100, max_color=255):
        pixels = []
        for i in range(height):
            for j in range(width):
                pixels.append((max_color, max_color, max_color))
        return PPMImage(width, height, max_color, pixels)

    @staticmethod
    def generate_black_ppm(width=10, height=10, max_color=255):
        pixels = []
        for i in range(height):
            for j in range(width):
                pixels.append((0, 0, 0))
        return PPMImage(width, height, max_color, pixels)

    @staticmethod
    def generate_random_ppm(width=10, height=10, max_color=255):
        pixels = []
        for i in range(height):
            for j in range(width):
                pixels.append(
                    (random.randrange(0, max_color), random.randrange(0, max_color), random.randrange(0, max_color)))
        return PPMImage(width, height, max_color, pixels)

    def write_ppm(self, filename):
        with open(filename, 'w') as f:
            f.write(f"P3\n")
            f.write(f"{self.width} {self.height}\n")
            f.write(f"{self.max_color}\n")

            for i in range(self.height):
                for j in range(self.width):
                    r, g, b = self.pixels[i * self.width + j]
                    f.write(f"{r} {g} {b} ")
                f.write("\n")

    def draw_ppm(self):
        count = 0
        for r, g, b in self.pixels:
            brightness = (r + g + b) // 3
            if brightness < 60:
                char = " "
            elif brightness < 125:
                char = "."
            elif brightness < 200:
                char = "o"
            else:
                char = "O"
            print(char, end=" ")
            count += 1
            if not count % self.width:
                print()
        print()

    def show_ppm(self):
        root = tk.Tk()
        root.title("P3 PPM Image Display")

        canvas = tk.Canvas(root, width=self.width, height=self.height)
        canvas.pack()

        for i in range(self.height):
            for j in range(self.width):
                r, g, b = self.pixels[i * self.width + j]
                color = "#{:02x}{:02x}{:02x}".format(r, g, b)
                canvas.create_line(j, i, j + 1, i, fill=color)

        root.mainloop()
