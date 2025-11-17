import xml.etree.ElementTree as ET
from datetime import date

tree = ET.parse('dict.xml')
xmlRoot = tree.getroot()

#NOTE: any changes to the elements apply backwards to the original tree, so you can just write the whole tree back to the document after working with the elements directly

#For example, modifying the first entry in the code below, then using tree.write(), correctly adds the attribute to the document.

xmlRoot.find("entry").attrib["creationDate"] = "2025-06-30"

tree.write('dict.xml')

#Step 2: make any additions to the document

def create_entry(term :str, definition :str) -> ET.Element:
    #Get today's date
    dateFormatted = date.today().isoformat() #Get the ISO format of the date, which is the default acceptable value

    #Create the entry element
    entry = ET.Element("entry", attrib = {"creationDate":dateFormatted})

    termElem = ET.Element("term")
    termElem.text = term

    defElem = ET.Element("def")
    defElem.text = definition

    entry.append(termElem)
    entry.append(defElem)

    return entry

#Root is the root element (tagged "root"). The function returns the new root; assign like this:
#########    root = add_entry(root, entry)
def add_entry(root :ET.Element, entry :ET.Element):
    #Add entry to the root
    root.append(entry)

    return root



