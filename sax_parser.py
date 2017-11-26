import xml.sax
import xml.sax.handler
import Excel_writer
import myTreeView

class CtsTestResultHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.currentTag = ""
        self.testSuits = []
        self.testCase = ""
        self.failedCaseName = []
        self.deviceFingerPrint = ""
        self.ctsVersion = ""
        self.totalFailedResultDicts = {}

    def startElement(self,tag,attributes):
        self.currentTag = tag
        if tag == "TestSuite":
            self.testSuits.append(attributes["name"])
        elif tag == "TestCase":
            self.testCase = attributes["name"]
        elif tag == "Test":
            if attributes["result"] == "fail":
                self.failedCaseName.append(attributes["name"])
        elif tag == "BuildInfo":
            self.deviceFingerPrint = attributes["build_fingerprint"]
            self.buildDevice = attributes["build_device"]
        elif tag == "Cts":
            self.ctsVersion = attributes["version"]



    def endElement(self,tag):
        if tag == "TestPackage":
            self.currentTag = ""
            self.testPackage = ""
            self.testSuits.clear()
            self.failedCaseName.clear()
        elif tag == "TestSuite":
            self.testSuits.pop()
        elif tag == "TestCase":
            if len(self.failedCaseName) > 0:
                packageName = ""
                for name in self.testSuits:
                    packageName =packageName+name+"."
                packageName = packageName+self.testCase
                for it in self.failedCaseName:
                    self.totalFailedResultDicts.setdefault(packageName,[]).append(it)
                self.failedCaseName.clear()



  #  def characters(self,content):
        #print("content",content)

    def endDocument(self):
        for (k,v) in self.totalFailedResultDicts.items():
            print(k,v)
            #Excel_writer.writeToExcel(self.ctsVersion, self.deviceFingerPrint, self.totalFailedResultDicts)
        #myTreeView.showTreveiw(self.totalFailedResultDicts)
        #self.totalFailedResultDicts.clear()

if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces,0)
    Handler = CtsTestResultHandler()
    parser.setContentHandler(Handler)

    parser.parse("testResult.xml")
