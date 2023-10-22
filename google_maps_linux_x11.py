################################################################################################
# Google Maps custom keyboard shortcuts
# Works on Linux with X11
# Default margin values for 1920 by 1080 resolution and whatever my screen's pixel density is
# Tested on Debian 12 with GNOME 45
# Dependencies: pynput, xdotool, xprop, grep
################################################################################################

from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller
import subprocess

STREET_VIEW_ENTER_KEY = "d"
STREET_VIEW_EXIT_KEY = "s"

STREET_VIEW_ENTER_XMARGIN_MAXIMIZED = -150 # from window right edge
STREET_VIEW_ENTER_YMARGIN_MAXIMIZED = -34 # from window bottom edge
STREET_VIEW_EXIT_XMARGIN_MAXIMIZED = -30 # from window right edge
STREET_VIEW_EXIT_YMARGIN_MAXIMIZED = 110 # from window top edge

# Margins are slightly different when the window is not maximized
STREET_VIEW_ENTER_XMARGIN_NOT_MAXIMIZED = STREET_VIEW_ENTER_XMARGIN_MAXIMIZED - 15 # from window right edge
STREET_VIEW_ENTER_YMARGIN_NOT_MAXIMIZED = STREET_VIEW_ENTER_YMARGIN_MAXIMIZED - 35 # from window bottom edge
STREET_VIEW_EXIT_XMARGIN_NOT_MAXIMIZED = STREET_VIEW_EXIT_XMARGIN_MAXIMIZED - 22 # from window right edge
STREET_VIEW_EXIT_YMARGIN_NOT_MAXIMIZED = STREET_VIEW_EXIT_YMARGIN_MAXIMIZED + 15 # from window top edge

mouse = Controller()
alt_active = False # whether the Alt key is currently being pressed or not, used to check for key combinations with Alt

def get_active_window_geometry():
    window_x = int(subprocess.getoutput("xdotool getactivewindow getwindowgeometry --shell | grep X").split("=")[1])
    window_y = int(subprocess.getoutput("xdotool getactivewindow getwindowgeometry --shell | grep Y").split("=")[1])
    window_w = int(subprocess.getoutput("xdotool getactivewindow getwindowgeometry --shell | grep WIDTH").split("=")[1])
    window_h = int(subprocess.getoutput("xdotool getactivewindow getwindowgeometry --shell | grep HEIGHT").split("=")[1])
    return (window_x, window_y, window_w, window_h)

# Called when a key is pressed
def on_press(key):
    global alt_active
    try: # key.char throws an exception when non-alphanumeric keys are pressed
        if key == Key.alt:
            alt_active = True # update Alt key pressed status

        elif key.char == STREET_VIEW_ENTER_KEY: # toggle street view on map view
            if alt_active: # only execute command if the alt key is pressed
                window_title = subprocess.getoutput("xdotool getactivewindow getwindowname")
                if "Google Maps" in window_title:
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
                    current_position = mouse.position # save current mouse position
                    mouse.position = (click_x, click_y)
                    mouse.click(Button.left)
                    mouse.position = current_position # restore previous mouse position

        elif key.char == STREET_VIEW_EXIT_KEY: # exit street view (clicks the profile button if used in map view)
            if alt_active:
                window_title = subprocess.getoutput("xdotool getactivewindow getwindowname")
                if "Google Maps" in window_title:
                    (window_x, window_y, window_w, window_h) = get_active_window_geometry()
                    click_x = window_x + window_w + STREET_VIEW_EXIT_XMARGIN_MAXIMIZED
                    click_y = window_y + STREET_VIEW_EXIT_YMARGIN_MAXIMIZED

                    window_id = subprocess.getoutput("xdotool getactivewindow")
                    window_status_cmd = "xprop -id " + window_id + " _NET_WM_STATE"
                    window_status = subprocess.getoutput(window_status_cmd)
                    if not "_NET_WM_STATE_MAXIMIZED_VERT" in window_status and not "_NET_WM_STATE_MAXIMIZED_HORZ" in window_status:
                        click_x = window_x + window_w + STREET_VIEW_EXIT_XMARGIN_NOT_MAXIMIZED
                        click_y = window_y + STREET_VIEW_EXIT_YMARGIN_NOT_MAXIMIZED

                    current_position = mouse.position
                    mouse.position = (click_x, click_y)
                    mouse.click(Button.left)
                    mouse.position = current_position
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