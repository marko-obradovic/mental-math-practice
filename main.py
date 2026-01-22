#!/usr/bin/env python3
"""
Terminal Mental Maths Trainer
Keyboard-only, curses-based TUI

Controls:
- Arrow keys / Tab to navigate
- Enter to select
- ESC or Q to trigger exit prompt during quiz
"""

import curses
import random
import math

# -----------------------------
# Question generation
# -----------------------------


def get_levels():
    return {
        "Addition": [100, 1000, 10000, 100000],
        "Subtraction": [100, 1000, 10000, 100000],
        "Multiplication": [12, 20, 50, 100],
        "Division": [12, 20, 50, 100],
        "Powers": [2, 3, 4, 5],  # max exponent
        "Roots": [10, 50, 100, 500],
        "Random": [],
    }


def generate_question(qtype, level):
    if qtype == "Addition":
        a = random.randint(1, level)
        b = random.randint(1, level)
        return f"{a} + {b}", a + b

    if qtype == "Subtraction":
        a = random.randint(1, level)
        b = random.randint(1, level)
        return f"{a} - {b}", a - b

    if qtype == "Multiplication":
        a = random.randint(1, level)
        b = random.randint(1, level)
        return f"{a} × {b}", a * b

    if qtype == "Division":
        b = random.randint(1, level)
        c = random.randint(1, level)
        a = b * c
        return f"{a} ÷ {b}", c

    if qtype == "Powers":
        base = random.randint(2, 12)
        exp = random.randint(2, level)
        return f"{base}^{exp}", base**exp

    if qtype == "Roots":
        root = random.randint(2, 5)
        base = random.randint(1, level)
        val = base**root
        return f"{root}√{val}", base

    if qtype == "Random":
        return generate_question(
            random.choice(["Addition", "Subtraction", "Multiplication", "Division"]),
            level,
        )


# -----------------------------
# UI helpers
# -----------------------------


def center_text(win, y, text, bold=False):
    x = (curses.COLS - len(text)) // 2
    if bold:
        win.attron(curses.A_BOLD)
    win.addstr(y, x, text)
    if bold:
        win.attroff(curses.A_BOLD)


# -----------------------------
# Menu screen
# -----------------------------


def menu(stdscr):
    curses.curs_set(0)
    options = ["Level", "Questions", "Type", "Start"]
    qtypes = list(get_levels().keys())

    selected = 0
    level = 1
    questions = 10
    qtype_idx = 0

    while True:
        stdscr.clear()
        center_text(stdscr, 2, "Mental Maths Trainer", True)

        for i, opt in enumerate(options):
            marker = ">" if i == selected else " "
            if opt == "Level":
                text = f"Level: {level}"
            elif opt == "Questions":
                text = f"Questions: {questions}"
            elif opt == "Type":
                text = f"Type: {qtypes[qtype_idx]}"
            else:
                text = "Start"
            stdscr.addstr(5 + i * 2, 10, f"{marker} {text}")

        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            selected = (selected - 1) % len(options)
        elif key in (curses.KEY_DOWN, ord("j")):
            selected = (selected + 1) % len(options)
        elif key in (curses.KEY_LEFT, ord("h")):
            if options[selected] == "Level":
                level = max(1, level - 1)
            elif options[selected] == "Questions":
                questions = max(1, questions - 1)
            elif options[selected] == "Type":
                qtype_idx = (qtype_idx - 1) % len(qtypes)
        elif key in (curses.KEY_RIGHT, ord("l")):
            if options[selected] == "Level":
                level = min(4, level + 1)
            elif options[selected] == "Questions":
                questions += 1
            elif options[selected] == "Type":
                qtype_idx = (qtype_idx + 1) % len(qtypes)
        elif key in (10, 13):  # Enter
            if options[selected] == "Start":
                return level, questions, qtypes[qtype_idx]


# -----------------------------
# Quiz screen
# -----------------------------


def quiz(stdscr, level, total_qs, qtype):
    curses.curs_set(1)
    score = 0
    levels = get_levels()
    max_val = levels[qtype][level - 1] if qtype != "Random" else 100

    for qn in range(1, total_qs + 1):
        stdscr.clear()
        question, answer = generate_question(qtype, max_val)

        stdscr.addstr(1, 2, f"Score: {score}")
        stdscr.addstr(1, curses.COLS - 20, f"Question {qn}/{total_qs}")
        center_text(stdscr, 5, question, True)
        center_text(stdscr, 8, "Your answer:")

        curses.echo()
        stdscr.move(10, curses.COLS // 2 - 5)
        user = stdscr.getstr().decode().strip()
        curses.noecho()

        try:
            if int(user) == answer:
                score += 1
        except:
            pass

    stdscr.clear()
    center_text(stdscr, 6, f"Final Score: {score}/{total_qs}", True)
    center_text(stdscr, 8, "Press any key to return to menu")
    stdscr.getch()


# -----------------------------
# Main
# -----------------------------


def main(stdscr):
    curses.use_default_colors()
    while True:
        level, qs, qtype = menu(stdscr)
        quiz(stdscr, level, qs, qtype)


if __name__ == "__main__":
    curses.wrapper(main)
