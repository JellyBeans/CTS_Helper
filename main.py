from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from sax_parser import CtsTestResultHandler
from tkinter import messagebox
import subprocess
import xml.sax
import xml.sax.handler
import Excel_writer
import os


class Main():
    def __init__(self):
        self.tradefedTool = ""
        self.deviceList = []
        self.currentSelDev = ""
        self.currentAbi = "Default"
        self.keyId = []
        os.environ['PATH'] = \
            ':'.join(("/home/tools/android-sdk-linux_x86/build-tools/23.0.1/",
                      os.getenv('PATH'),))

    def addMenu(self):
        menubar = Menu(self.root)

        fmenu = Menu(menubar)
        fmenu.add_command(label='Load cts result', command=self.loadCtsResult)
        fmenu.add_command(label='Export to Excel', command=self.exportToExcel)
        fmenu.add_command(label='Create subPlan', command=self.createCtsSubPlan)
        fmenu.add_command(label='Set cts&gts test suit', command=self.setTestSutiPath)
        fmenu.add_command(label='Restart ADB', command=self.restartADB)
        fmenu.add_command(label='Exit', command=self.root.quit)

        # tool menu
        toolMenu = Menu(menubar)
        toolMenu.add_command(label="Check Apk CERT", command=self.checkApkCert)

        aboutMenu = Menu(menubar)
        for item in ['Copright']:
            aboutMenu.add_command(label=item)

        menubar.add_cascade(label="File", menu=fmenu)
        menubar.add_cascade(label="Tool", menu=toolMenu)
        menubar.add_cascade(label="About", menu=aboutMenu)

        self.root['menu'] = menubar

    def initUI(self):
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

        self.lable_ABI = ttk.Label(self.frame,text="Test ABI")
        self.lable_ABI.grid(column=0,row=3,sticky=(N,W))

        self.testABICB = ttk.Combobox(self.frame)
        self.testABICB['values'] = ["Default","armeabi-v7a","arm64-v8a"]
        self.testABICB.set("Default")
        self.testABICB.bind('<<ComboboxSelected>>', self.set_Abi())
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
        print("set abi to "+self.currentAbi)


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
            result_file_name = self.Handler.buildDevice + "_" + self.Handler.deviceFingerPrint.split("-")[0].split("/")[4] + "_" + self.Handler.testSuitName+"_"+self.Handler.suitVersion+"_"+"test_result.xls"
            options = {}
            options['defaultextension'] = '.xls'
            options['filetypes'] = [('Excel file', '.xls')]
            options['initialfile'] = result_file_name
            options['title'] = 'Save File'
            filename = filedialog.asksaveasfilename(**options)
            Excel_writer.writeToExcel(self.Handler.testSuitName,self.Handler.suitVersion,self.Handler.deviceFingerPrint,self.Handler.totalFailedResultDicts,filename)

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
            print(cmd)
            child = subprocess.Popen(["konsole", "-e", cmd], stdout=subprocess.PIPE, start_new_session=True)

        else:
            child = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
            ret = child.stdout.readlines()
            str = ""
            for it in ret:
                str += it.decode()
            print(str)
            # messagebox.showinfo(message=str)
            tl = Toplevel(self.root,height=200, width=400)
            # Make topLevelWindow remain on top until destroyed, or attribute changes.
            tl.attributes('-topmost', 'true')
            Label(tl, text=str, justify=LEFT).pack()



    def createCtsSubPlan(self):
        pass

    def setTestSutiPath(self):
        self.tradefedTool = filedialog.askopenfilename()
        if self.tradefedTool == "" or self.tradefedTool == ():
            messagebox.showinfo(message='Tradefed too must be set!!!')

    def restartADB(self):
        self.executeCmd("adb kill-server", isShell=True)
        self.executeCmd("adb devices",isShell=True)


    def addTreeView(self):

        def onDBClick(event):
            if self.keyId == []:
                print("No element")
                return
            sitem = self.tree.selection()[0]
            if self.tree.parent(sitem) == "":
                print("it's package")
            else:
                self.checkAdbDevices()
                if self.tradefedTool == "" or self.tradefedTool == ():
                    messagebox.showinfo(message='Tradefed tool must be set!!!')
                    return

                cmd = self.tradefedTool
                if self.Handler.testSuitName == "GTS":
                    cmd = cmd + " run gts"
                else:
                    cmd = cmd + " run cts"

                parentID = self.tree.parent(sitem)
                if self.Handler.testSuitClass == "1":
                    testPackage = self.tree.item(parentID, "text")
                else:
                    testPackage = self.tree.item(parentID,"text").split("-")[0]

                testName = self.tree.item(sitem, "text")
                if self.Handler.testSuitClass == "1":
                    cmd = cmd + " -c " + testPackage + " -m " + testName
                else:
                    cmd = cmd + " -m " + testPackage + " -t " + testName

                #--serial to specify the device
                if self.currentSelDev != "":
                    cmd = cmd + " -s "+self.currentSelDev.split("-")[0]

                if self.isCTSSkipPreconditions == True:
                    cmd = cmd + " --skip-preconditions"

                if self.isCTSDisableReboot == True:
                    cmd = cmd + " --disable-reboot"
                if self.currentAbi != "Default":
                    print(self.currentAbi)
                    cmd = cmd + " --abi "+self.currentAbi

                print("cmd" + cmd)
                env = os.environ.copy()
                print(env["PATH"])
                child = subprocess.Popen(["xterm", "-e", cmd],stdout=subprocess.PIPE, start_new_session=True,env=env)
                out = child.communicate()
                print(out)


        self.tree = ttk.Treeview(self.frame, height=30, selectmode="extended")

        #set treview width
        self.tree.column("#0", width=600)

        self.tree.bind("<Double-1>", onDBClick)
        self.tree.pack()

        vbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.tree.yview())
        self.tree.configure(yscrollcommand=vbar.set)
        self.tree.grid(row=0, column=0, sticky=(N,S,E,W))
        vbar.grid(row=0, column=1, sticky=(N,S,E,W))

    def checkApkCert(self):
        options = {}
        options['defaultextension'] = '.apk'
        options['filetypes'] = [('Android APK', '.apk')]
        options['title'] = 'Open Apk'
        apkfilename = filedialog.askopenfilename(**options)
        if apkfilename == "" or apkfilename == ():
            # user has canceled the choosing of file dialog
            return
        cmd = "keytool -printcert -jarfile " + apkfilename
        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        ret = child.stdout.readlines()
        str = ""
        for it in ret:
            str += it.decode()
        tl = Toplevel(self.root, height=200, width=400)
        tl.title(apkfilename)
        # Make topLevelWindow remain on top until destroyed, or attribute changes.
        tl.attributes('-topmost', 'true')
        Label(tl, text=str, justify=LEFT).pack()


if __name__ == "__main__":
    myApp = Main()
    myApp.run()

