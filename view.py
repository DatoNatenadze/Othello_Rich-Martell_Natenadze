from tkinter import *
from pygame import mixer
from controller import *
import os

## getting resources after building.
# def resource_path(relative_path):
#     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
#     return os.path.join(base_path, relative_path)
nodes = 0
depth = 4
moves = 0
root = Tk()
root.iconbitmap('resources/LOGO_CHAMPOLLION.ico')
screen = Canvas(root, width=500, height=600, background="#000000",highlightthickness=0)
screen.pack()
CHOOSING = True
RUNNING = False
VSAI = False
mixer.init()

choose_style(screen)
data = {'root': root, "choosing": CHOOSING, "running": RUNNING, "VSAI":VSAI, 'screen': screen, 'mixer':mixer, 'depth': depth}
screen.bind("<Button-1>", lambda event, arg=data: handle_mouse(event, arg))
screen.bind("<Key>",lambda event, arg=data: key_handling(event, arg))
screen.focus_set()

root.wm_title("Othello")
root.mainloop()
