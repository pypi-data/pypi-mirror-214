from a_selenium_click_on_coords import click_on_coordinates
from ctypes import windll, byref
from ctypes.wintypes import POINT
import keyboard
from ctypes_window_info import get_window_infos
from mousekey import MouseKey
import sys

coordsclicker = sys.modules[__name__]
coordsclicker.driver = None
coords_clicker = MouseKey()
pos = POINT()


def click_on_coords(
    x: int,
    y: int,
) -> bool:
    r"""
       Clicks on the specified coordinates (x, y) on the current browser window.

    Args:
        x (int): The x-coordinate of the target location.
        y (int): The y-coordinate of the target location.

    Returns:
        bool: True if the click operation is successful, False otherwise.

    Example:

        from time import sleep
        import undetected_chromedriver as uc

        from seleniumabsxy import set_show_hotkey_coords,click_on_coords,coordsclicker

        if __name__ == "__main__":
            set_show_hotkey_coords(hotkey='ctrl+alt+k')
            chrome_opt = uc.ChromeOptions()
            chrome_opt.add_argument("--incognito")
            driver = uc.Chrome(
                options=chrome_opt,
            )
            coordsclicker.driver=driver
            sleep(5)
            driver.get(r"https://python.org")
            driver.fullscreen_window()
            # go to the object you want to click on, press 'ctrl+alt+k', and call click_on_coords(x,y)
    """
    script_timeout = 10
    co = get_browser_window_coords()
    x1 = abs(int(x - co["offset_x"]))
    y1 = abs(int(y - co["offset_y"]))
    try:
        click_on_coordinates(coordsclicker.driver, x1, y1, script_timeout=script_timeout)
        return True
    except Exception:
        return False


def set_show_hotkey_coords(hotkey: str = "ctrl+alt+k") -> None:
    """
    Sets a hotkey combination to print the current cursor coordinates.

    Args:
        hotkey (str, optional): The hotkey combination. Defaults to "ctrl+alt+k".
    """
    keyboard.add_hotkey(hotkey, print_coords)


def print_coords() -> tuple[int, int]:
    """
    Prints the current cursor coordinates and returns them.

    Returns:
        tuple[int, int]: The x and y coordinates of the cursor.
    """
    get_cursor()
    print(f"\nx={pos.x}, y={pos.y}\n")
    return pos.x, pos.y


def get_cursor() -> None:
    """
    Gets the current cursor position and updates the 'pos' variable.
    """
    windll.user32.GetCursorPos(byref(pos))


def get_browser_window_coords() -> dict:
    """
    Retrieves the coordinates and dimensions of the current browser window.

    Returns:
        dict: A dictionary containing the window offset, height, width, and center coordinates.
    """
    widget1 = "WidgetWin_1"
    bar = 0
    boundingbox = (0, 0, 0, 0)
    aftercheckpids = [coordsclicker.driver.browser_pid]
    wii = get_window_infos()
    allei = []
    for g in wii:
        if g.pid in aftercheckpids:
            for _ in coords_clicker.get_elements_from_hwnd(g.hwnd)["family"]:
                allei.append(_)
    alle = list(set(allei))
    for _ in alle:
        if "Chrome_RenderWidgetHostHWND" in _.title:
            bar = _.coords_win[2]

    for g in wii:
        if g.pid in aftercheckpids:
            if "WidgetWin" in g.class_name:
                if sum(g.dim_win) > 0:
                    if widget1 in g.class_name:
                        boundingbox = (
                            g.coords_win[0],
                            g.coords_win[2] + bar,
                            g.coords_win[1],
                            g.coords_win[3],
                        )
    offset_x = boundingbox[0]
    offset_y = boundingbox[1]
    height = boundingbox[3] - boundingbox[1]
    width = boundingbox[2] - boundingbox[0]
    center = offset_x + width // 2, offset_y + height // 2
    vara = {
        "offset_x": offset_x,
        "offset_y": offset_y,
        "height": height,
        "width": width,
        "center": center,
    }
    return vara
