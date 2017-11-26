import xml.sax
import xml.sax.handler

class CtsTestResultHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.currentTag = ""
        self.testPackage = ""
        self.testSuits = []
        self.testCase = ""
        self.testNames = []
        self.failReuslts =[]

    def startElement(self,tag,attributes):
        self.currentTag = tag
        if tag == "TestPackage":
            #print("--->begin new package",attributes["name"])
            self.testPackage = attributes["name"]
        elif tag == "TestSuite":
            #print("--->suit",attributes["name"])
            self.testSuits.append(attributes["name"])
        elif tag == "TestCase":
            #print("===>testCase",attributes["name"])
            self.testCase = attributes["name"]
        elif tag == "Test":
            #print("--->tag",attributes["name"])
            if attributes["result"] == "fail":
                #print("find")
                self.testNames.append(attributes["name"])


    def endElement(self,tag):
        if tag == "TestPackage":
            self.currentTag = ""
            self.testPackage = ""
            self.testSuits.clear()
            self.testNames.clear()
        elif tag == "TestCase":
            if len(self.testNames) > 0:
                module = ""
                for name in self.testSuits:
                    #print(name+".",end="")
                    module =module+name+"."
                #print(self.testCase)
                module = module+self.testCase
                self.failReuslts.append(module)
                for it in self.testNames:
                    #print(it)
                    self.failReuslts.append(it)
                self.testNames.clear()
                #print("=======================")
                self.failReuslts.append("================")


  #  def characters(self,content):
        #print("content",content)

    def endDocument(self):
        for it in self.failReuslts:
            print(it)
        self.failReuslts.clear()

if __name__ == "__main__":
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces,0)
    Handler = CtsTestResultHandler()
    parser.setContentHandler(Handler)

    parser.parse("testResult.xml")
