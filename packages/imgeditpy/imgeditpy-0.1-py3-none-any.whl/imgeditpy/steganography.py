from imgeditpy import PPMImage

encrypt_key = "A"
decrypt_key = "Z"


def authorize_user(password):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if password == input("Enter the password: "):
                print("Authorized for encryption") if password == encrypt_key else print("Authorized for decryption")
                return func(*args, **kwargs)
            else:
                print("Access denied. Incorrect password")
                exit(1)

        return wrapper

    return decorator


@authorize_user(encrypt_key)
def encrypt_message(filename, output, message):
    if '\n' in message:
        print("Cannot have newline characters in your message")
        return
    binary_message = ''.join(f"{ord(each_char):08b}" for each_char in message)
    message_len = len(binary_message)

    image = PPMImage.read_ppm(filename)
    width = image.width
    height = image.height
    pixels = image.pixels

    i = 0
    for position in range(min(width, height)):
        if i >= message_len:
            break
        pixel_idx = (position * width + position)
        r, g, b = pixels[pixel_idx]
        if binary_message[i] == "1":
            r |= 1
        else:
            r &= ~1
        pixels[pixel_idx] = (r, g, b)
        i += 1

    with open(output, 'w') as f:
        f.write(f"P3\n{image.width} {image.height}\n{image.max_color}\n")
        for i in range(height):
            for j in range(width):
                r, g, b = pixels[i * width + j]
                f.write(f"{r} {g} {b} ")
            f.write("\n")


@authorize_user(decrypt_key)
def decrypt_message(filename, message_length):
    with open(filename, 'r') as f:
        _ = f.readline().strip()
        line = f.readline().strip()
        while line.startswith('#'):
            line = f.readline().strip()
        width, height = map(int, line.split())
        _ = int(f.readline().strip())
        pixels = []
        for line in f:
            pixels.extend(map(int, line.split()))

        pixels = [(pixels[i], pixels[i + 1], pixels[i + 2]) for i in range(0, len(pixels), 3)]

    binary_message = ""
    bits_needed = message_length * 8

    for position in range(min(width, height)):
        if len(binary_message) >= bits_needed:
            break
        pixel_idx = position * width + position
        r, g, b = pixels[pixel_idx]
        binary_message += str(r & 1)
    hidden_message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        hidden_message += chr(int(byte, 2))

    return hidden_message
