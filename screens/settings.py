import curses
import json

arrows = ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT"]
wasd = ["w", "s", "a", "d"]

def settings(scr):
    scr.clear()
    curses.curs_set(0)
    scr.nodelay(True)

    max_height = curses.LINES
    max_width = curses.COLS

    with open("settings.json", "r") as file_read:
        data = json.load(file_read)

	# Selected button
    selected_button = 0

    button_height, button_width = 3, 10
    start_y, start_x = 4, max_width // 2 + 1  # Position of the button

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Selected
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK) # Not selected

    options = {
        "Character step": ["character_step"],
        "Dash multiplier": ["dash_multiplier"],
        "Character frames of attack": ["char_attack_frames"],
        "Boss step": ["boss_step"],
        "Boss delay": ["boss_buffer"],
        "Horizontal attack delay": [("boss_side_attack_tick", 1)],
        "Vertical attack delay": [("boss_side_attack_tick", 0)],
        "FPS": ["FPS"],
        "wasd to move? (0 or 1)": ["wasd_as_movement"]
    }

    selected_button = 0

    for index, button in enumerate(options.keys()):
        options[button].append(index)
        options[button].append(curses.newwin(button_height, button_width, start_y + button_height * index, start_x))

    while True:

        scr.addstr(max_height//2, 10, "Press 'q'", curses.color_pair(1))
        scr.addstr(max_height//2 + 1, 5, "to confirm and exit")

        for option in options.keys():
            scr.addstr(start_y + button_height//2 + options[option][1] * button_height, max_width // 2 - len(option), option)
        scr.refresh()

        for option in options.keys():
            if isinstance(options[option][0], tuple):
                content = data[options[option][0][0]][options[option][0][1]]
            else:
                content = data[options[option][0]]

            options[option][2].clear()
            options[option][2].addstr(button_height//2, button_width//2 - len(str(content))//2 - 1, str(content))
            options[option][2].box()

            if options[option][1] == selected_button:
                options[option][2].bkgd(" ", curses.color_pair(1))
            else:
                options[option][2].bkgd(" ", curses.color_pair(2))

            options[option][2].refresh()

        try: key = scr.getkey()
        except: key = "Nothing"

        if key == "q":
            with open("settings.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
            break

        if key in (arrows[1], wasd[1]):
            if selected_button + 1 < len(options.keys()):
                selected_button += 1
            else:
                selected_button = 0

        elif key in (arrows[0], wasd[0]):
            if selected_button > 0:
                selected_button -= 1
            else:
                selected_button = len(options.keys()) - 1

        elif key in (arrows[2], wasd[2], arrows[3], wasd[3]):
            for option in options.keys():
                if options[option][1] == selected_button:
                    try:
                        if isinstance(options[option][0], tuple):
                            data[options[option][0][0]][options[option][0][1]] += 1 if key in (arrows[3], wasd[3]) else -1
                        else:
                            data[options[option][0]] += 1 if key in (arrows[3], wasd[3]) else -1
                    except:
                        break
