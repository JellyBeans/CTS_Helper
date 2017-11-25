from tkinter import *
root = Tk()
menubar = Menu(root)
fmenu = Menu(menubar)
for item in ['Export to Excel','Create subPlan','Exit']:
    fmenu.add_command(label = item)

aboutMenu = Menu(menubar)
for item in ['Copright']:
    aboutMenu.add_command(label = item)

menubar.add_cascade(label = "File",menu = fmenu)
menubar.add_cascade(label = "About",menu = aboutMenu)

root['menu'] = menubar
root.mainloop()