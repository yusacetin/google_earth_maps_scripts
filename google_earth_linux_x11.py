################################################################################################
# Google Earth custom keyboard shortcuts
# Works on Linux with X11
# Default margin values for 1920 by 1080 resolution and whatever my screen's pixel density is
# Tested on Debian 12 with GNOME 43
# Dependencies: pynput, xdotool, xprop
# North-Top doesn't work for some reason
################################################################################################

from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller
import subprocess

STREET_VIEW_ENTER_KEY = "d"
STREET_VIEW_EXIT_KEY = "s"
NORTH_TOP_KEY = "f"

STREET_VIEW_ENTER_XMARGIN_MAXIMIZED = -35 # from window right edge
STREET_VIEW_ENTER_YMARGIN_MAXIMIZED = -130 # from window bottom edge
STREET_VIEW_EXIT_XMARGIN_MAXIMIZED = 30 # from window left edge
STREET_VIEW_EXIT_YMARGIN_MAXIMIZED = 120 # from window top edge
NORTH_TOP_XMARGIN_MAXIMIZED = -35 # from window right edge
NORTH_TOP_YMARGIN_MAXIMIZED = -180 # from window bottom edge

# Margins are slightly different when the window is not maximized
STREET_VIEW_ENTER_XMARGIN_NOT_MAXIMIZED = STREET_VIEW_ENTER_XMARGIN_MAXIMIZED - 15 # from window right edge
STREET_VIEW_ENTER_YMARGIN_NOT_MAXIMIZED = STREET_VIEW_ENTER_YMARGIN_MAXIMIZED - 35 # from window bottom edge
STREET_VIEW_EXIT_XMARGIN_NOT_MAXIMIZED = STREET_VIEW_EXIT_XMARGIN_MAXIMIZED + 20 # from window left edge
STREET_VIEW_EXIT_YMARGIN_NOT_MAXIMIZED = STREET_VIEW_EXIT_YMARGIN_MAXIMIZED + 20 # from window top edge
NORTH_TOP_XMARGIN_NOT_MAXIMIZED = NORTH_TOP_XMARGIN_MAXIMIZED - 15 # from window right edge
NORTH_TOP_YMARGIN_NOT_MAXIMIZED = NORTH_TOP_YMARGIN_MAXIMIZED - 30 # from window bottom edge

mouse = Controller()
alt_active = False # whether the Alt key is currently being pressed or not, used to check for key combinations with Alt

def get_active_window_geometry():
    window_info = subprocess.getoutput("xdotool getactivewindow getwindowgeometry --shell").split("\n")
    window_x = 0
    window_y = 0
    window_w = 0
    window_h = 0
    for i in window_info:
        (key, value) = i.split("=")
        if key == "X":
            window_x = int(value)
        elif key == "Y":
            window_y = int(value)
        elif key == "WIDTH":
            window_w = int(value)
        elif key == "HEIGHT":
            window_h = int(value)
    return (window_x, window_y, window_w, window_h)

# Called to simulate clicks on the buttons
def click_and_return(click_x, click_y):
    current_position = mouse.position # save current cursor position
    mouse.position = (click_x, click_y) # move the cursor to the click position
    mouse.click(Button.left) # perform the click
    mouse.position = current_position # restore previous cursor position

# Called when a key is pressed
def on_press(key):
    global alt_active
    try: # key.char throws an exception when non-alphanumeric keys are pressed
        window_title = subprocess.getoutput("xdotool getactivewindow getwindowname")
        if "Google Earth" in window_title:
            if key == Key.alt:
                alt_active = True # update Alt key pressed status

            elif key.char == STREET_VIEW_ENTER_KEY: # toggle street view on map view
                if alt_active: # only execute command if the alt key is pressed
                    (window_x, window_y, window_w, window_h) = get_active_window_geometry()
                    click_x = window_x + window_w + STREET_VIEW_ENTER_XMARGIN_MAXIMIZED
                    click_y = window_y + window_h + STREET_VIEW_ENTER_YMARGIN_MAXIMIZED

                    # Adjust margins if the window is not maximized
                    window_id = subprocess.getoutput("xdotool getactivewindow")
                    window_status_cmd = "xprop -id " + window_id + " _NET_WM_STATE"
                    window_status = subprocess.getoutput(window_status_cmd)
                    if not "_NET_WM_STATE_MAXIMIZED_VERT" in window_status and not "_NET_WM_STATE_MAXIMIZED_HORZ" in window_status:
                        click_x = window_x + window_w + STREET_VIEW_ENTER_XMARGIN_NOT_MAXIMIZED
                        click_y = window_y + window_h + STREET_VIEW_ENTER_YMARGIN_NOT_MAXIMIZED

                    # Simulate a click on the street view button
                    click_and_return(click_x, click_y)

            elif key.char == STREET_VIEW_EXIT_KEY: # exit street view (clicks the profile button if used in map view)
                if alt_active:
                    (window_x, window_y, window_w, window_h) = get_active_window_geometry()
                    click_x = window_x + STREET_VIEW_EXIT_XMARGIN_MAXIMIZED
                    click_y = window_y + STREET_VIEW_EXIT_YMARGIN_MAXIMIZED

                    window_id = subprocess.getoutput("xdotool getactivewindow")
                    window_status_cmd = "xprop -id " + window_id + " _NET_WM_STATE"
                    window_status = subprocess.getoutput(window_status_cmd)
                    if not "_NET_WM_STATE_MAXIMIZED_VERT" in window_status and not "_NET_WM_STATE_MAXIMIZED_HORZ" in window_status:
                        click_x = window_x + STREET_VIEW_EXIT_XMARGIN_NOT_MAXIMIZED
                        click_y = window_y + STREET_VIEW_EXIT_YMARGIN_NOT_MAXIMIZED

                    click_and_return(click_x, click_y)

            elif key.char == NORTH_TOP_KEY: # set view to north to top
                if alt_active:
                    (window_x, window_y, window_w, window_h) = get_active_window_geometry()
                    click_x = window_x + window_w + NORTH_TOP_XMARGIN_MAXIMIZED
                    click_y = window_y + window_h + NORTH_TOP_YMARGIN_MAXIMIZED

                    window_id = subprocess.getoutput("xdotool getactivewindow")
                    window_status_cmd = "xprop -id " + window_id + " _NET_WM_STATE"
                    window_status = subprocess.getoutput(window_status_cmd)
                    if not "_NET_WM_STATE_MAXIMIZED_VERT" in window_status and not "_NET_WM_STATE_MAXIMIZED_HORZ" in window_status:
                        click_x = window_x + window_w + NORTH_TOP_XMARGIN_NOT_MAXIMIZED
                        click_y = window_y + window_h + NORTH_TOP_YMARGIN_NOT_MAXIMIZED

                    click_and_return(click_x, click_y)
    except:
        pass

# Called when a key is released, only used to update Alt key pressed status
def on_release(key):
    global alt_active
    if key == Key.alt:
        alt_active = False

# Listen for keypresses
listener = Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join() # program quits immediately if this call isn't made