import curses

import cv2
import numpy as np


def webcam_to_ascii(terminal) -> None:
    init_terminal(terminal)

    cap = cv2.VideoCapture(0)

    density = dict(enumerate([" ", ".", "'", ",", ":", ";", "c", "l", "x", "o",
                              "k", "X", "d", "O", "0", "K", "N"]))
    convert_to_ascii = np.vectorize(lambda x: density[x // 16])

    exit_signal = False
    while not exit_signal:
        screen_height, screen_width = terminal.getmaxyx()
        _, frame = cap.read()
        image_in_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        resized_image = cv2.resize(image_in_gray, (int(screen_width), int(screen_height)))
        ascii_image = convert_to_ascii(resized_image)
        for index_of_row, row in enumerate(ascii_image):
            terminal.addstr(index_of_row, 0, ''.join(row[:-1])[::-1])
        terminal.refresh()
        exit_signal = cv2.waitKey(1) & 0xFF == ord('q') or terminal.getch() == ord('q')

    cap.release()


def init_terminal(terminal) -> None:
    curses.noecho()
    curses.cbreak()
    terminal.nodelay(True)
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    terminal.attron(curses.color_pair(1))
    terminal.clear()


if __name__ == '__main__':
    curses.wrapper(webcam_to_ascii)
