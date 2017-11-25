from tkinter import *
from tkinter.ttk import *
def check_fun():
    val = v.get()
    if val ==  0:
        print("UnCheck!")
    else:
        print("Checked!")


root = Tk()
Label(root, text = "count:").grid(row = 0, sticky = W)
Entry(root).grid(row = 0, column = 1,sticky = E)

Label(root,text = "pwd:").grid(row = 1, sticky = W)
Entry(root).grid(row=1, column = 1, sticky = E)

Button(root,text = "login").grid(row=2,column = 1,sticky = E)
v = IntVar()
c = Checkbutton(root,variable = v,text ="rember me?",command = check_fun)
c.invoke()
c.grid(row = 2,column= 0, sticky = W)
root.mainloop()