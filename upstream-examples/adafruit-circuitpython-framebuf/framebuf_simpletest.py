# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
#
# Adapted from Adafruit's framebuf_simpletest.py to the PyMCU language subset:
# round() became integer arithmetic, the REPL print_buffer() demo and fb.text()
# were dropped (text() needs str.split, which is not compilable). The framebuffer
# operations below are the ones display drivers such as adafruit_ssd1306 use.

import adafruit_framebuf

WIDTH = 32
HEIGHT = 8

buffer = bytearray(WIDTH * ((HEIGHT + 7) // 8))
fb = adafruit_framebuf.FrameBuffer(buffer, WIDTH, HEIGHT, buf_format=adafruit_framebuf.MVLSB)

# Shapes test
fb.pixel(3, 5, True)
fb.rect(0, 0, fb.width, fb.height, True)
fb.line(1, 1, fb.width - 2, fb.height - 2, True)
fb.fill_rect(25, 2, 2, 2, True)

# Clear and redraw
fb.fill(False)
fb.hline(0, 4, WIDTH, True)
fb.vline(16, 0, HEIGHT, True)
fb.scroll(-1, 0)
