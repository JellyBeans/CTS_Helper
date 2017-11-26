from tkinter import *
from tkinter import ttk
import subprocess

def showTreveiw(listItem):
    isRunning = False
    def onDBClick(event):
        item = tree.selection()[0]
        if tree.parent(item) == "":
            print("it's package")
        else:
            print("----->")
            cmd = "/home/ray/Dev/CTS/6.0_r24/android-cts/tools/cts-tradefed run cts"
            pid = tree.parent(item)
            testPackage = tree.item(pid,"text")
            cmd = cmd + " -c " + testPackage + " -m " + tree.item(item,"text") + " --skip-preconditions"
            print("cmd"+cmd)
            child = subprocess.Popen(["xterm", "-e",cmd],stdout=subprocess.PIPE, start_new_session=True)
            out = child.communicate()
            print("---->", out)

    root = Tk()
    tree = ttk.Treeview(root,height=30,selectmode="extended")
    tree.column("#0",width=400)
    for key in listItem:
        myid=tree.insert("",0,key,text = key)
        tree.item(key,open=True)
        for item in listItem[key]:
            id = tree.insert(myid,0,item,text = item)

    tree.bind("<Double-1>", onDBClick)
    tree.pack()

    vbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview())
    tree.configure(yscrollcommand=vbar.set)
    tree.grid(row=0,column=0,sticky=NSEW)
    vbar.grid(row=0,column=1,sticky=NS)


    root.mainloop()