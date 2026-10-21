"""
Click at a screen coordinate using pyautogui AND flash a highlight ring at the click point.

Install:
  pip install pyautogui

Run:
  python click_highlight.py 500 300
or (no args) it will use your current mouse position after a 2-second countdown:
  python click_highlight.py
"""

import sys
import time
import tkinter as tk

import pyautogui


# --- Settings ---
FLASH_MS = 350          # how long the highlight stays visible
RADIUS = 10             # ring radius (pixels)
RING_WIDTH = 2          # ring thickness

# Safety: move mouse to a screen corner to abort pyautogui
pyautogui.FAILSAFE = True


def make_overlay(root: tk.Tk):
    """Create a small always-on-top overlay window used to draw the ring."""
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)          # no window border
    overlay.attributes("-topmost", True)    # stay above other windows

    # Attempt transparency (works on Windows; varies on macOS/Linux)
    bg = "magenta"
    overlay.configure(bg=bg)
    try:
        overlay.wm_attributes("-transparentcolor", bg)
    except tk.TclError:
        # Some platforms/window managers don't support it
        pass

    size = 2 * RADIUS + 24
    canvas = tk.Canvas(
        overlay,
        width=size,
        height=size,
        bg=bg,
        highlightthickness=0,
        bd=0,
    )
    canvas.pack()

    overlay.withdraw()  # hidden until used
    return overlay, canvas, size, bg


def flash_ring(overlay: tk.Toplevel, canvas: tk.Canvas, size: int, x: int, y: int):
    """Show a ring centered at screen coordinate (x, y)."""
    overlay.geometry(f"{size}x{size}+{int(x - size/2)}+{int(y - size/2)}")

    canvas.delete("all")
    cx = cy = size // 2
    canvas.create_oval(
        cx - RADIUS,
        cy - RADIUS,
        cx + RADIUS,
        cy + RADIUS,
        outline="red",
        width=RING_WIDTH,
    )

    overlay.deiconify()
    overlay.lift()


def click_with_highlight(x: int, y: int, button: str = "left", show_highlight: bool = True):
    """Main routine: flash highlight then perform a pyautogui click at (x,y)."""

    print(f"Clicking at ({x}, {y}).")

    pyautogui.click(x=x, y=y)
    # time.sleep(CLICK_DELAY_MS)
    if show_highlight:
        root = tk.Tk()
        root.withdraw()  # no main window


        overlay, canvas, size, _bg = make_overlay(root)

        # Show ring immediately
        flash_ring(overlay, canvas, size, x, y)


        def cleanup():
            try:
                overlay.withdraw()
            finally:
                root.destroy()

        # Schedule click shortly after the highlight appears
        # Hide highlight and exit
        root.after(FLASH_MS, overlay.withdraw)
        root.after(FLASH_MS + 100, cleanup)

        root.mainloop()


def parse_coords():
    # if len(sys.argv) >= 3:
    #     return int(sys.argv[1]), int(sys.argv[2])

    # print("No coordinates provided. Move your mouse to the target point...")
    for i in range(2, 0, -1):
        print(f"  clicking in {i}...")
        time.sleep(1)
    pos = pyautogui.position()
    return pos.x, pos.y


if __name__ == "__main__":
    x, y = parse_coords()
    # print(f"Clicking at ({x}, {y}) with highlight. (Move mouse to a corner to abort.)")
    click_with_highlight(x, y)
    # pyautogui.click(1963, 615)
