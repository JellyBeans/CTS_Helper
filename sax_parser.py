import xml.sax
import xml.sax.handler
import Excel_writer
import myTreeView

class CtsTestResultHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.testSuitVersion = 2 # default is new V2
        self.currentTag = ""
        #for v1
        self.testSuitsV1 = []
        self.testCaseV1 = ""

        #for v2
        self.testModule = ""
        self.testCaseV2 = ""

        self.failedCaseName = []
        self.deviceFingerPrint = ""
        self.ctsVersion = ""
        self.totalFailedResultDicts = {}

    def startElement(self,tag,attributes):
        #We will meet this two kind of tag for both two version test suits.
        #We use this to control our pars logic
        self.currentTag = tag
        if tag == "TestResult":#this tag indicates this is V2 test suit,include GTS & CTS
            self.testSuitVersion = 1
        elif tag == "Result":#this tag indicates this is V1 test suit.
            self.testSuitVersion = 2

        #yeah, this is ugly, but jut for work
        if self.testSuitVersion == 1:
            #for V1
            if tag == "TestSuite":
                self.testSuitsV1.append(attributes["name"])
            elif tag == "testCase":
                self.testCaseV1 = attributes["name"]
            elif tag == "Test":
                if attributes["result"] == "fail":
                    self.failedCaseName.append(attributes["name"])

            elif tag == "BuildInfo":
                self.deviceFingerPrint = attributes["build_fingerprint"]
                self.buildDevice = attributes["build_device"]
            elif tag == "Cts":
                self.ctsVersion = attributes["version"]
        else:
            #for V2
            if tag == "Module":
                self.testModule = attributes["name"]
                self.abi = attributes["abi"]
            elif tag == "TestCase":
                self.testCaseV2 = attributes["name"]
            elif tag == "Test":
                if attributes["result"] == "fail":
                    self.failedCaseName.append(self.testCaseV2 + "#"+attributes["name"])



    def endElement(self,tag):
        if self.testSuitVersion == 1:
            if tag == "TestPackage":
                self.currentTag = ""
                self.testPackage = ""
                self.testSuitsV1.clear()
                #self.failedCaseName.clear()
            elif tag == "TestSuite":
                self.testSuitsV1.pop()
            elif tag == "TestCase":
                if len(self.failedCaseName) > 0:
                    packageName = ""
                    for name in self.testSuitsV1:
                        packageName =packageName+name+"."
                    packageName = packageName+self.testCaseV1
                    for it in self.failedCaseName:
                        self.totalFailedResultDicts.setdefault(packageName,[]).append(it)
                    self.failedCaseName.clear()

        else:
            if tag == "Module":
                if len(self.failedCaseName) > 0:
                    testModule = self.testModule+"-"+self.abi
                    for it in self.failedCaseName:
                        self.totalFailedResultDicts.setdefault(testModule,[]).append(it)
                    self.failedCaseName.clear()



  #  def characters(self,content):
        #print("content",content)

    def endDocument(self):
        pass
        #for (k,v) in self.totalFailedResultDicts.items():
            #print(k,v)
            #Excel_writer.writeToExcel(self.ctsVersion, self.deviceFingerPrint, self.totalFailedResultDicts)
        #myTreeView.showTreveiw(self.totalFailedResultDicts)
        #self.totalFailedResultDicts.clear()

if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces,0)
    Handler = CtsTestResultHandler()
    parser.setContentHandler(Handler)

    parser.parse("testResult.xml")
