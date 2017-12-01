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
        self.tradefedTool = ""
        self.deviceList = []
        self.currentSelDev = ""
        self.currentAbi = "Default"
        self.keyId = []

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

        self.lable_ABI = ttk.Label(self.frame,text="Test ABI")
        self.lable_ABI.grid(column=0,row=3,sticky=(N,W))

        self.testABICB = ttk.Combobox(self.frame)
        self.testABICB.bind('<<ComboboxSelected>>', self.set_Abi())
        self.testABICB['values'] = ["Default","armeabi-v7a","arm64-v8a"]
        self.testABICB.set("Default")
        self.testABICB.grid(column=0, row=4, sticky=(N, W, E))

        self.lable_ABI = ttk.Label(self.frame, text="Choose Device")
        self.lable_ABI.grid(column=0, row=5, sticky=(N, W))
        devicevar = StringVar()
        self.adbdeviceCB = ttk.Combobox(self.frame)
        self.adbdeviceCB.bind('<<ComboboxSelected>>', self.chooseTestDevices)
        self.adbdeviceCB['values'] = self.deviceList
        self.adbdeviceCB.grid(column=0, row=6, sticky=(N, W, E))

        self.root.resizable(False, False)
        self.root.mainloop()

    def set_Abi(self):
        self.currentAbi = self.testABICB.get()


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
        keys = sorted(self.Handler.totalFailedResultDicts.keys(),reverse=True)

        # clear Treeview item
        for it in self.keyId:
            self.tree.delete(it)
        self.keyId.clear()

        for key in keys:
            myid = self.tree.insert("", 0, text=key)
            self.keyId.append(myid)
            self.tree.item(myid, open=True)
            for item in self.Handler.totalFailedResultDicts[key]:
                self.tree.insert(myid, 0, text=item)
        self.tree.update()

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

    def checkAdbDevices(self):
        p = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, start_new_session=True)
        ret = p.stdout.readlines()
        lenth = len(ret)
        if lenth >= 3:
            self.deviceList.clear()
            newList = []
            for i in range(1,lenth-1):
                s = ret[i].decode().split('\t')[0]
                p=subprocess.Popen("adb"+" -s "+s+" shell getprop ro.product.device", shell=True, stdout=subprocess.PIPE)
                getPro = p.stdout.readline()
                newList.append(s+"-"+getPro.decode())
                #newList.append(s)
            self.deviceList = newList
            self.adbdeviceCB['values'] = self.deviceList
            if self.currentSelDev not in self.deviceList:
                self.adbdeviceCB.current(0)
                self.currentSelDev = self.adbdeviceCB.get()
            if len(self.deviceList) > 1 :
                messagebox.showinfo(message='More than One Device Connected')
        else:
            messagebox.showinfo(message='No device Connected !!!')
            self.deviceList.clear()
            self.adbdeviceCB['values'] = self.deviceList

    def chooseTestDevices(self,*args):
        selected = self.adbdeviceCB.get()
        self.currentSelDev = selected
        #if selected not in self.currentSelDev:
            #self.currentSelDev.append(selected)

    def executeCmd(self,cmd,isShell):
        if isShell == False:
            child = subprocess.Popen(["xterm", "-e", cmd], stdout=subprocess.PIPE, start_new_session=True)
        else:
            child = subprocess.Popen(cmd,shell=True)
        child.communicate()


    def createCtsSubPlan(self):
        pass

    def setTestSutiPath(self):
        self.tradefedTool = filedialog.askopenfilename()
        if self.tradefedTool == "" or self.tradefedTool == ():
            messagebox.showinfo(message='Tradefed too must be set!!!')

    def restartADB(self):
        self.executeCmd("adb kill-server", isShell=True)
        self.executeCmd("adb devices",isShell=True)


    def addMenu(self):
        menubar = Menu(self.root)
        fmenu = Menu(menubar)
        fmenu.add_command(label='Load cts result', command=self.loadCtsResult)
        fmenu.add_command(label='Export to Excel', command=self.exportToExcel)
        fmenu.add_command(label='Create subPlan', command=self.createCtsSubPlan)
        fmenu.add_command(label='Set cts&gts test suit',command=self.setTestSutiPath)
        fmenu.add_command(label='Restart ADB', command = self.restartADB)
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
                self.checkAdbDevices()
                if self.tradefedTool == "" or self.tradefedTool == ():
                    messagebox.showinfo(message='Tradefed tool must be set!!!')
                    return

                cmd = self.tradefedTool + " run cts"
                parentID = self.tree.parent(sitem)
                testPackage = self.tree.item(parentID, "text")
                testName = self.tree.item(sitem, "text")
                cmd = cmd + " -c " + testPackage + " -m " + testName
                #--serial to specify the device
                if self.currentSelDev != "":
                    cmd = cmd + " -s "+self.currentSelDev.split("-")[0]

                if self.isCTSSkipPreconditions == True:
                    cmd = cmd + " --skip-preconditions"

                if self.isCTSDisableReboot == True:
                    cmd = cmd + " --disable-reboot"
                print("cmd" + cmd)
                child = subprocess.Popen(["xterm", "-e", cmd], stdout=subprocess.PIPE, start_new_session=True)
                out = child.communicate()


        self.tree = ttk.Treeview(self.frame, height=30, selectmode="extended")

        #set treview width
        self.tree.column("#0", width=600)

        self.tree.bind("<Double-1>", onDBClick)
        self.tree.pack()

        vbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.tree.yview())
        self.tree.configure(yscrollcommand=vbar.set)
        self.tree.grid(row=0, column=0, sticky=(N,S,E,W))
        vbar.grid(row=0, column=1, sticky=(N,S,E,W))



if __name__ == "__main__":
    myApp = Main()
    myApp.run()