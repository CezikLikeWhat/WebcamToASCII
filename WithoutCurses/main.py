import os

import cv2


def convert_row_to_ascii(row) -> tuple:
    density = " .',:;clxokXdO0KN"
    return tuple(density[x // 16] for x in row)[::-1]


def convert_to_ascii(input_grays) -> tuple:
    return tuple(convert_row_to_ascii(row) for row in input_grays)


def print_array(input_ascii_array) -> None:
    print('\n'.join((''.join(row) for row in input_ascii_array)), end='')


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    screen_height, screen_width = os.popen('stty size', 'r').read().split()

    height = int(screen_height)
    width = int(screen_width)

    while cv2.waitKey(1) & 0xFF != ord('q'):
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        reduced = cv2.resize(gray, (width, height))
        converted = convert_to_ascii(reduced)
        print_array(converted)

    cap.release()
