from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from sax_parser import CtsTestResultHandler
from tkinter import messagebox
import subprocess
import xml.sax
import xml.sax.handler
import Excel_writer


class Main():
    def __init__(self):
        pass

    def run(self):
        self.isCTSSkipPreconditions = False
        self.isCTSDisableReboot = False
        self.root = Tk()
        self.root.title("Cts Helper")
        self.addMenu()
        self.frame = ttk.Frame(self.root, padding=(3, 3, 3, 3))
        self.frame.grid(column=0, row=0, sticky=(N, S, E, W))
        self.addTreeView()
        self.var_check = StringVar()
        self.check_skipprecondition = ttk.Checkbutton(self.frame, text='--skip-preconditions',variable=self.var_check,
                                                      command=self.change_option, onvalue='on', offvalue='off')
        self.check_skipprecondition.grid(column=0,row=1,sticky=W)
        self.var_reboot = StringVar()
        self.check_skipprecondition = ttk.Checkbutton(self.frame, text='--disable-reboot', variable=self.var_reboot,
                                                      command=self.change_option, onvalue='on', offvalue='off')
        self.check_skipprecondition.grid(column=0, row=2,sticky=W)

        self.root.resizable(False, False)
        self.root.mainloop()

    def change_option(self):
        if self.var_check.get() == "on":
            self.isCTSSkipPreconditions = True
        else:
            self.isCTSSkipPreconditions = False

        if self.var_reboot.get() == "on":
            self.isCTSDisableReboot = True
        else:
            self.isCTSDisableReboot = False

    def loadCtsResult(self):
        self.filename = filedialog.askopenfilename()
        self.parseCtsResult()
        self.fillTreview()


    def fillTreview(self):
        for key in self.Handler.totalFailedResultDicts:
            myid = self.tree.insert("", 0, text=key)
            self.tree.item(myid, open=True)
            for item in self.Handler.totalFailedResultDicts[key]:
                self.tree.insert(myid, 0, text=item)

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
            sitem = self.tree.selection()[0]
            if self.tree.parent(sitem) == "":
                print("it's package")
            else:
                cmd = "/home/ray/Dev/CTS/6.0_r24/android-cts/tools/cts-tradefed run cts"
                parentID = self.tree.parent(sitem)
                testPackage = self.tree.item(parentID, "text")
                cmd = cmd + " -c " + testPackage + " -m " + self.tree.item(sitem, "text")
                if self.isCTSSkipPreconditions == True:
                    cmd = cmd + " --skip-preconditions"
                if self.isCTSDisableReboot == True:
                    cmd = cmd + " --disable-reboot"
                #print("cmd" + cmd)
                child = subprocess.Popen(["xterm", "-e", cmd], stdout=subprocess.PIPE, start_new_session=True)
                out = child.communicate()


        self.tree = ttk.Treeview(self.frame, height=30, selectmode="extended")

        #set treview width
        self.tree.column("#0", width=400)

        self.tree.bind("<Double-1>", onDBClick)
        self.tree.pack()

        vbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.tree.yview())
        self.tree.configure(yscrollcommand=vbar.set)
        self.tree.grid(row=0, column=0, sticky=(N,S,E,W))
        vbar.grid(row=0, column=1, sticky=(N,S,E,W))



if __name__ == "__main__":
    myApp = Main()
    myApp.run()