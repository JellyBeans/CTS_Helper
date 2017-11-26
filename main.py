from tkinter import *
from tkinter import ttk
import subprocess
from tkinter import filedialog
from sax_parser import CtsTestResultHandler
import xml.sax
import xml.sax.handler
import Excel_writer
from tkinter import messagebox


class Main():
    def __init__(self):
        pass

    def Run(self):
        self.root = Tk()
        self.root.title("Cts Helper")
        self.addMenu()
        self.frame = ttk.Frame(self.root, padding=(3, 3, 12, 12))
        self.frame.grid(column=0, row=0, sticky=(N, S, E, W))
        self.addTreeView()


        btn = ttk.Button(self.frame, text="Choices")
        btn.grid(column=1, row=1)

        self.root.mainloop()
    def loadCtsResult(self):
        self.filename = filedialog.askopenfilename()
        self.parseCtsResult()
        self.fillTreview()


    def fillTreview(self):
        for key in self.Handler.totalFailedResultDicts:
            myid = self.tree.insert("", 0, key, text=key)
            self.tree.item(key, open=True)
            for item in self.Handler.totalFailedResultDicts[key]:
                self.tree.insert(myid, 0, item, text=item)

    def parseCtsResult(self):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.Handler = CtsTestResultHandler()
        parser.setContentHandler(self.Handler)
        parser.parse(self.filename)


    def exportToExcel(self):
        if "Handler" not in dir(self):
            messagebox.showinfo(message='Please Load Cst result first!!!')
        else:
            result_file_name = self.Handler.buildDevice + "_" + self.Handler.deviceFingerPrint.split("-")[0].split("/")[4] + "_" + self.Handler.ctsVersion+"_"+"test_result.xls"
            options = {}
            options['defaultextension'] = '.xls'
            options['filetypes'] = [('Excel file', '.xls')]
            options['initialfile'] = result_file_name
            options['title'] = 'Save File'
            filename = filedialog.asksaveasfilename(**options)
            Excel_writer.writeToExcel(self.Handler.ctsVersion,self.Handler.deviceFingerPrint,self.Handler.totalFailedResultDicts,filename)


    def createCtsSubPlan(self):
        pass

    def addMenu(self):
        menubar = Menu(self.root)
        fmenu = Menu(menubar)
        fmenu.add_command(label='Load cts result', command=self.loadCtsResult)
        fmenu.add_command(label='Export to Excel', command=self.exportToExcel)
        fmenu.add_command(label='Create subPlan', command=self.createCtsSubPlan)
        fmenu.add_command(label='Exit', command=self.root.quit)


        aboutMenu = Menu(menubar)
        for item in ['Copright']:
            aboutMenu.add_command(label=item)

        menubar.add_cascade(label="File", menu=fmenu)
        menubar.add_cascade(label="About", menu=aboutMenu)

        self.root['menu'] = menubar

    def addTreeView(self):

        def onDBClick(event):
            item = self.tree.selection()[0]
            if self.tree.parent(item) == "":
                print("it's package")
            else:
                cmd = "/home/ray/Dev/CTS/6.0_r24/android-cts/tools/cts-tradefed run cts"
                parentID = self.tree.parent(item)
                testPackage = self.tree.item(parentID, "text")
                cmd = cmd + " -c " + testPackage + " -m " + self.tree.item(item, "text") + " --skip-preconditions"
                #print("cmd" + cmd)
                child = subprocess.Popen(["xterm", "-e", cmd], stdout=subprocess.PIPE, start_new_session=True)
                out = child.communicate()


        self.tree = ttk.Treeview(self.frame, height=30, selectmode="extended")

        #set treview width
        self.tree.column("#0", width=400)

        self.tree.bind("<Double-1>", onDBClick)
        self.tree.pack()

        vbar = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview())
        self.tree.configure(yscrollcommand=vbar.set)
        self.tree.grid(row=0, column=0, sticky=NSEW)
        vbar.grid(row=0, column=1, sticky=NS)



if __name__ == "__main__":
    myApp = Main()
    myApp.Run()