import xml.dom.minidom as xml
import os
import types

def defineInnerHTML(self, text = None):
    if text is None:
        return next(
            (
                child.data
                for child in self.childNodes
                if child.nodeType == child.TEXT_NODE
            ),
            "",
        )

    for child in self.childNodes:
        if child.nodeType == child.TEXT_NODE:
            child.data = text
            return True

    nodeToAdd = self.documentNode.createTextNode(text)
    self.appendChild(nodeToAdd)


class XMLParser ():
    def __init__ (self, xmlFile, version = "1.0", encoding = "UTF-8"):
        self.xmlFile = xmlFile
        self.version = version
        self.encoding = encoding

    def create (self, rootElement = "root"):
        xmlString = f"<?xml version=\"{self.version}\" encoding=\"{self.encoding}\"?>"
        xmlString += f"<{rootElement}></{rootElement}>"

        self.xml = xml.parseString(xmlString)
        self.rootElement = self.xml.firstChild

        return True

    def open (self):
        assert (os.path.isfile(self.xmlFile))

        with open(self.xmlFile, "r") as file:
            self.xml = file.read()
            self.xml = xml.parseString(self.xml)
            self.rootElement = self.xml.firstChild

        return True
    
    def getElementById(self, id):
        return self.select(f"#{id}", _all = True)

    def select(self, selector, _all = False):
        sel = selector[0]

        if sel != "#":
            return False
        if _all:
            return self.xml.getElementById(selector)
        else:
            return self.xml.getElementById(selector)[0]

    def createElement(self, element, parent = None, attributes = {}):
        if parent is None:
            parent = self.rootElement

        element = self.xml.createElement(element)

        for [key, value] in attributes.items():
            element.setAttribute(key, value)

        parent.appendChild(element)

        element.documentNode = self.xml
        element.rootElement = self.rootElement
        element.innerHTML = types.MethodType(defineInnerHTML, element)

        return element

    def save(self, saveName = None):
        if saveName is None:
            saveName = self.xmlFile

        with open(saveName, "w") as file:
            file.write(self.xml.toprettyxml(indent = "\t", newl = "\n", encoding = self.encoding).decode(self.encoding))

    def getString (self):
        return self.xml.toprettyxml(indent = "\t", newl = "\n", encoding = self.encoding).decode(self.encoding)

if __name__ == "__main__":
    parser = XMLParser("./test.xml")
    
    try:
        parser.open()
    except Exception as e:
        parser.create()

    elem = parser.createElement("test")
    elem.innerHTML("Success!")

    print(parser.getString())
    parser.save()