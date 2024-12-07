# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2024, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from PIL import Image


class SteganographyTool:
    def __init__(self, image_path=None):
        self.image_path = image_path
        self.img = Image.open(image_path)
        self.width, self.height = self.img.size

    def max_capacity(self):
        max_bytes = (self.width * self.height * 3) // 8
        max_symbols = max_bytes // 2
        return max_bytes, max_symbols

    def _get_binary_text(self):
        binary_text = ''
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.img.getpixel((x, y))
                for i in range(3):
                    binary_text += str(pixel[i] & 1)
        return binary_text

    def is_encoded(self):
        binary_text = self._get_binary_text()
        byte_array = [binary_text[i:i + 8] for i in range(0, len(binary_text), 8)]
        return any(byte != '00000000' for byte in byte_array)

    def _set_pixel(self, x, y, pixel):
        self.img.putpixel((x, y), tuple(pixel))

    def encode(self, secret_text):
        if self.is_encoded():
            raise ValueError("The image already contains encrypted data. Please use another image.")

        if len(secret_text.encode('utf-8')) > self.max_capacity()[0]:
            raise ValueError("The message is too long for this image.")

        binary_text = ''.join(format(byte, '08b') for byte in secret_text.encode('utf-8')) + '00000000'
        data_index = 0

        for y in range(self.height):
            for x in range(self.width):
                if data_index < len(binary_text):
                    pixel = list(self.img.getpixel((x, y)))
                    for i in range(3):  # Для R, G, B
                        if data_index < len(binary_text):
                            pixel[i] = (pixel[i] & ~1) | int(binary_text[data_index])
                            data_index += 1
                    self._set_pixel(x, y, pixel)
                else:
                    break

        self.img.save(self.image_path)

    def decode(self):
        if not self.is_encoded():
            raise ValueError("The image does not contain any encoded data.")

        binary_text = self._get_binary_text()
        byte_array = [binary_text[i:i + 8] for i in range(0, len(binary_text), 8)]
        secret_bytes = bytearray()

        for byte in byte_array:
            if byte == '00000000':
                break
            secret_bytes.append(int(byte, 2))

        if len(secret_bytes) == 0:
            return "There is no hidden message."

        return secret_bytes.decode('utf-8')

    def clear(self):
        if not self.is_encoded():
            raise ValueError("The image does not contain any encoded data to clear.")

        for y in range(self.height):
            for x in range(self.width):
                pixel = list(self.img.getpixel((x, y)))
                for i in range(3):
                    pixel[i] = pixel[i] & ~1
                self._set_pixel(x, y, pixel)

        self.img.save(self.image_path)
