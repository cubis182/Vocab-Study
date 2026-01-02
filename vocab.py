from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from PyDictionary import PyDictionary
from googletrans import Translator
from datetime import datetime
#temp
import os

import textwrap

import xml.etree.ElementTree as ET

import sys
from datetime import date

print(os.getcwd())

sys.setrecursionlimit(3600*24)

MAX_UNDO = 100 #max number of actions you can undo (+ 1 because I am lazy)
SAVE_CHANGES_SHORTCUT = "<Mod1-Key-s>"
UNSPECIFIED_LANG = "unspecif"

#FILTERS
"""
To add a filter, you need to add a value at a correct key. 
Below are valid keys with their accepted value in parentheses next to it.
'in-term' (string)
'in-def' (string)
'before' (datetime)
'after' (datetime)
'language' (string)
"""
dictFilters = {} #Empty dictionary; we add filters by adding the correct keys

#The supported languages. Customizing this would be ideal. 
Languages = {
      "Unspecified":"unspecif",
      "Greek":"grc",
      "Latin":"lat"
}



"""

KEY INFO:
dict.xml is the guide for this project: it contains a list of all the vocab entries. It also has a schema, named ___________, which allows for validation.

The XML is loaded into memory by the program, and each element has an @id, which is the same as the IDs in the app's treeview, which is what the end user sees. The IDs are
invisible, but they are accessible by getting an item in the treeview and using ['text'] to get the ID from it. Each entry is a dictionary, in essence, so that's why it works.

NEVER CALL TO DICT.XML; dict.xml is the file that contains all the vocab, but it's in a different location depending on whether it's the python script or the packaged app. Use pathlib 
to get the file:
            from pathlib import Path
            Path(__file__).resolve().with_name("dict.xml")
__file__ is the current path, and usin



WISHLIST:

Wishlist Format:
-    ESSENTIAL: Must go into the program at some point for baseline usability
-    NICE TO HAVE: A good quality of life feature; probably a good idea to include it
-    NON-ESSENTIAL: The least important. Neither a big quality of life feature nor essential.

Ctrl + Z:
- How many steps to save? Every call to update_listbox would have to save the current xmlRoot somewhere. I guess it would be easy
- 

Add images using the file browser to an entry - ESSENTIAL
Add images to an entry using drag and drop - NICE TO HAVE
Store the language of each entry - ESSENTIAL
Remove filters - ESSENTIAL
Show current filters - NICE TO HAVE
Optional "Are you sure you want to delete?" dialogue on deleting an entry
Flashcard mode: opens up new window with just the word, based on the list in the current view mode (see below) - NICE TO HAVE
Combo box toggles view modes - ESSENTIAL
Each view mode has the ability to activate or deactivate certain buttons and features - ESSENTIAL
Customizable fonts - NICE TO HAVE
ESSENTIAL VIEW MODES:
- View All
- View by Date (comes with date range or single date option; also ascending / descending order option)

NICE TO HAVE VIEW MODES:
- Sort by Hardest (the most missed in Flashcard mode - depends on flashcard mode existing)

Rename everything referencing listboxes to treeview - ESSENTIAL
Give an option to 
Don't bother to ask to save on quit if the data hasn't been changed - NON-ESSENTIAL
Have a way of showing shortcuts on buttons and tooltips - NON-ESSENTIAL
Highlight required fields in some way - NICE TO HAVE
Option to resize text - ESSENTIAL
Customize the languages - NICE-TO-HAVE

ONGOING ISSUES:
How to handle when I change the XML and there are old versions left over? Let's say I add a language option, how will the program sort the entry if it has no language at all? 
And this would need to be done with the XML, not externally, like by having a different XML for each language. It would just be easier to have User Defined languages this way.
The reason being, all the vocab can go in one XML and they have a specific, computer-readable tag on them with the User Defined name. If I just renamed each document,
the computer doesn't really have an understanding that they are languages, nor is it able to get that data in a useful format.

      Best solution is to exit the program and throw an exception if the XML doesn't validate

)

COMPLETED FEATURES - Move here after they're finished from the wishlist
Be able to black out one side

"""

"""
class Entry:
  def __init__(self, term: str, defin :str):
        self.term = term
        self.defin = defin

  
  
  Adds principal parts to the class. Want to do this so the app can keep these separate in the future
  
  def __add_prin_parts__(self, parts :str):
        self.partsDict = {
              1:"",
              2:"",
              3:"",
              4:""
        }

  def __add_to_dict__(self):
        lTerms.append(self)

"""

#suggested in the Tkinter Cookbook on that one blog, so I'm using a class to initialize a new window
"""
class SelectTerms(tk.Toplevel):
      def __init__(self):
            self.
            self.list = tk.Listbox(self)
            self.list.grid(column=0, row=1)
"""





class Undo():
      def __init__(self):
            self.array = []
      
      def add(self, xmlRoot :ET.Element):
            if len(self.array) > MAX_UNDO:
                  self.array.pop(0)

            print(f"Length of the xmlRoot I'm adding to the undo buffer: {len(xmlRoot.findall("./*"))}")
            self.array.append(xmlRoot)

      """
      undo() replaces the current global variable xmlRoot with the last saved version. The function then pops
      the last one in the list, then updates the treeview.

      WISHLIST:
      There is an option to permanently disable the messagebox when you try to undo and just have it print to the
        console or something - NON-ESSENTIAL
      """
      def undo(self):
            global xmlRoot

            try:
                  xmlRoot = self.array[-2]
                  print(f"xmlRoot variable: {xmlRoot}. Undo list size: {len(self.array)}. xmlRoot size: {len(xmlRoot.findall("./*"))}. Undo size: {len(self.array[-2].findall("./*"))}")

                  self.array.pop()
                  update_listbox()
            except IndexError:
                  messagebox.showerror("Error! No progress to undo.")

undoFeature = Undo()

def control_z(event):
      global undoFeature

      print("Hit CTRL - Z")

      undoFeature.undo()

#Returns a valid value for the item ID
"""
WISHLIST:

Generate a new ID by finding the lowest available number, not the next highest, since that means the program will never reset. OR......
  Every now and then generate a new set of IDs
"""
"""

Features:

The language format used for the XML is a standard format - ESSENTIAL

ESCAPE CHARACTERS:
I investigated escape characters, and the XML library deals with the problem on its own.
"""
def create_entry(term :str, definition :str, num, lang=UNSPECIFIED_LANG) -> ET.Element:
    #Get today's date
    dateFormatted = date.today().isoformat() #Get the ISO format of the date, which is the default acceptable value

    #Create the entry element
    entry = ET.Element("entry", creationDate=dateFormatted, n=str(num), language=lang)

    print(entry.tag)

    termElem = ET.Element("term")
    termElem.text = term

    defElem = ET.Element("def")
    defElem.text = definition

    entry.append(termElem)
    entry.append(defElem)

    print(entry.tag)

    return entry
             



#BEGIN TK ROOT
        
  
root = tk.Tk()
root.title('Subito')
root.geometry('900x500')
root['bg'] = 'white'

DEBUG_MODE = tk.BooleanVar() #When true, extra debug features are enabled
HIDE_TERMS = tk.BooleanVar() #When true, hide all the terms in the left column (terms)
HIDE_DEFS = tk.BooleanVar() #When true, hide all the terms in the right column (definitions)

#an empty root which will eventually be used to override the original document
lTerms = ET.Element("root", attrib = {"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                      "xsi:noNamespaceSchemaLocation":"vocab.xsd"})



#Initialize a list of terms from a file (file must be backwards compatible; use XML?)
from pathlib import Path
dictFile = Path(__file__).resolve().with_name("dict.xml")

if (DEBUG_MODE):
      print(f"Opening dictionary from this path: {dictFile}")
#Need to make sure the path is correct, depending on whether it's a script or a distributable program created by PyInstall

#if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
#    dictFile = Path(__file__).resolve().with_name("dict.xml") #__file__ will get the whole path, whether this is in the temp folder or not

eTree = ET.parse(dictFile)
xmlRoot = eTree.getroot()

def assign_id(input = None) -> int:
      global xmlRoot
      
      allEntries = []

      for entry in xmlRoot.findall("./*"):
            allEntries.append(int(entry.attrib['n']))
      print(f"assign_id: Every ID found in the dict.xml document (i.e. the @n attribute): {allEntries}")

      return (max(allEntries) + 1)

#Make sure each element has a number ID:
for entry in xmlRoot.findall("./*"):
      try:
             entry.attrib['n']
      except AttributeError:
             entry = assign_id()
      else:
             continue

#END TK ROOT

#A list of all the <entry/> elements in the dict.xml file. The update_list, delete, and 
#other functions make use of this value, so I assign it to a variable here once.
eEntries = xmlRoot.findall("./*")




def add_to_xml(n = assign_id()):
       #Goal: gets the input in each entry and adds to the file

       #Get the strings
       term = entryA.get()
       definition = entryB.get()
       lang = Languages[language.get()]



       """
       !!!!
       ADD HERE: What happens when the text entry is empty

       ESSENTIAL: account for XML escape characters, like '=', '<', etc. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       """

       #Get the entry XML element
       entryElem = create_entry(term, definition, n, lang)

       print(f"Created XML entry {print(entryElem)}")

       #add the entry XML element to the oot
       global xmlRoot

       xmlRoot = add_entry(xmlRoot, entryElem)
       print("Reaching end of add_to_xml process")

def replace_in_xml():
       """
       Process:

       - Get the current selection in the combo box
       - Make sure only one is selected: throw an error message with a dialogue box otherwise
       - 
       """

def click_term():
      if (HIDE_TERMS.get()):
            HIDE_TERMS.set(False)
      else:
            HIDE_TERMS.set(True)
      update_listbox()

def click_definition():
      if (HIDE_DEFS.get()):
            HIDE_DEFS.set(False)
      else:
            HIDE_DEFS.set(True)
      update_listbox()
  
"""
The function that activates when the user presses "enter" on the two main entry boxes. Activated one of three ways:
  -Hit the "Enter" button underneath the boxes
  -Hit the return/enter key on the keyboad while focus is on the "Term" entry box
  -Hit the return/enter key on the keyboard while focus is on the "Definition" entry box
"""
def retrieve(entry = None):
        add_to_xml() #Modify later so this isn't just a function that wraps another function
        
#Function that activates when hitting the "Replace" button
def replace(entry = None):
      modify_entry(modifyEntry=True)

def handle_quitout():
        
        save_changes()
        print("Quitting...")
      
        
        root.destroy()

def save_changes(event = None):
      """
       !!!!
       ADD HERE: What happens when you hit enter twice; remove any duplicates on saving!

       Solution:

       iter = entry.itertext()


      """

      #Prompt user to keep or discard changes to the dictionary
      saveChanges = messagebox.askquestion("Save Changes", "Would you like to save your changes to the dictionary? \n All unsaved changes will be lost on quit out.")
      print(type(saveChanges))
      if saveChanges == "yes":
            try:
                  eTree.write(dictFile) #Write over the XML document with the modified tree
                  print("Save success!")
                  update_listbox()
            except FileNotFoundError:
                  print("Error! Could not find 'dict.xml' to write to.")
      else:
            print("Changes unsaved.")

      

def on_closing():
       handle_quitout()

#Root is the root element (tagged "root"). The function returns the new root; assign like this:
#########    root = add_entry(root, entry)
def add_entry(root :ET.Element, entry :ET.Element):
    #Add entry to the root
    root.append(entry)

    update_listbox()

    return root

        
        

#word = Label(root,text="Enter Word",bg="white",font=('verdana',10,'bold'))
#word.place(x=250,y=23)



##############

"""
OPTIONS WISHLIST:

Language option "Auto" will detect the letters used and change the language accordingly - ESSENTIAL

"""
frOptions = tk.Frame(root, width=100, height=50, padx=15, pady=10)
frOptions.grid(column=0, row=0)

langLabel = tk.Label(frOptions, text="Select Language...")
langLabel.pack()

a = tk.StringVar() 
language = ttk.Combobox(frOptions, width = 20, textvariable = a, state='readonly',font=('verdana',10,'bold'),) 
  


language['values'] = list(Languages.keys())
  
language.pack(side='left')
language.current(0) 

##################

frInput = tk.Frame(root)
frInput.grid(column=0,row=1)

entryA = Entry(frInput,width=50,borderwidth=2,relief=RIDGE)
entryA.pack(anchor='n')

entryA.bind("<Return>", retrieve)

entryB = Entry(frInput,width=50,borderwidth=2,relief=RIDGE)
entryB.pack(anchor='s')

entryB.bind("<Return>", retrieve)

############

frEntryCtrl = tk.Frame(root)
frEntryCtrl.grid(column=0, row=2)

replace = Button(frEntryCtrl, text="Replace", font=('verdana',10,'bold'),cursor="hand2",relief=RIDGE, command=replace)
replace.pack(side='left')

search = Button(frEntryCtrl,text="Enter",font=('verdana',10,'bold'),cursor="hand2",relief=RIDGE,command=retrieve)
search.pack(side='left')

quit =  Button(frEntryCtrl,text="Quit",font=('verdana',10,'bold'),cursor="hand2",relief=RIDGE,command=handle_quitout)
quit.pack(side='left')


#meaning = Label(root,text="Meaning",bg="black",font=('verdana',15,'bold'))
#meaning.grid(column=1,row=0)

"""
output = Text(root,height=8,width=40,borderwidth=2,relief=RIDGE)
output.place(x=230,y=160)

view = Text(root,height=8,width=40,borderwidth=2,relief=RIDGE)
view.place(x=460,y=160)
"""

#BEGIN LISTBOX

"""
ONGOING BUGS/ISSUES:
- Delete button sometimes runs into an "index out of range" error when deleting multiple items at once, but then sucessfully finishes deleting
after the first or second items are deleted
- There is no way I know of to get text wrapping done. Making style = ttk.Style(), style.configure("StyleName", rowheight = 40), and tree.config(style = "StyleName").
     However, this changes all the rows.

LISTBOX / TREEVIEW WISHLIST:

MAKE THE DEFINITION BOX BIGGER!!!!! THAT WAY, YOU CAN SEE A FULL TERM BY CLICKING ON IT. LET USERS CONFIGURE THE SIZE AS WELL
Clicking on a column adds a "Column Settings" cascading menu at the top - ESSENTIAL
Clickiong on a column selects all the items in that column, and only that column - ESSENTIAL
There is an arrow to sort the list at the top of each column - NICE TO HAVE
CONFLICTS WITH PREVIOUS WISH There is a setting for sorting a column by each attribute - ESSENTIAL
There is a way to black out the one attribute of an item (i.e. black out just a term, just a definition, or both) - ESSENTIAL
Update the treeview every time a column is resized; the detection works by checking the <<ButtonRelease-1>> event and using tree.identify_region(event.x, event.y) to
   determine that a "separator" was involved. - NICE TO HAVE
Clicking on an item in the list replaces all the fields with the properties of that entry, so you can edit it and replace values (so, currently, it would replace whatever
    was in the term and entry box with the selected term and entry in the list)
Auto assign language based on what type of alphabet is used - NON-ESSENTIAL
Entering an entry gives some feedback, maybe selecting the new entry so you can see it in the tree view - ESSENTIAL


"""

listFrame = Frame(root, background="white")
listFrame.grid(column=0,row=3)

#An unplaced Treeview which will be used for showing vocab
tree = ttk.Treeview(listFrame, columns=("Term", "Definition"), show="headings")
tree.column("Term", width=200, anchor="center", )
tree.heading("Term", text="Term", command=click_term)
tree.column("Definition", width=250, anchor="center")
tree.heading("Definition", text="Definition", command=click_definition)
#tree.heading("#0", text="Term")
#tree.heading("Definition", text="Definition")
tree.grid(column=0, row=0)

#tree.place(x=230, y=160)
#populate the treeview with the list from root.findall("./*")
#for eEntry in xmlRoot.findall("./*"):
#       term = eEntry.find("term").text
#       definition = eEntry.find("def").text
#
#       print(f"Term: {term}; Def: {definition}")
#       tree.insert('', 'end', values=(str(term), str(definition)))

#listbox = Listbox(listFrame, width=55,
#                  bg = "grey",
#                  activestyle = 'dotbox', 
#                  font = "Helvetica",
#                  fg = "yellow")
#listbox.grid(row=0, column=0)



#start listbox scrollbars
listScrollbarA = Scrollbar(listFrame, orient=tk.HORIZONTAL)
listScrollbarA.grid(row=1, column=0, sticky="we")

listScrollbarB = Scrollbar(listFrame, orient=tk.VERTICAL)
listScrollbarB.grid(row=0, column=1, sticky="ns")

tree.config(xscrollcommand=listScrollbarA.set)
listScrollbarA.config(command=tree.xview)

tree.config(yscrollcommand=listScrollbarB.set)
listScrollbarB.config(command=tree.yview)
#end listbox scrollbars

def check_filter(eEntry: ET.Element) -> bool:
      """
      DEPENDENT OF UPDATE_LISTBOX:
      This means it runs every time the treeview is updated

      This function returns True or False. 

      It returns True if the Entry matches the filter criteria.
      These filter criteria are added on as new ideas and tools go into the workflow. 
      If you create a new filter, you need to create new code here which returns "True" when the condition is met.

      These are the conditions, as listed at the top of the file under #FILTERS

      'in-term' (string)
      'in-def' (string)
      'before' (datetime)
      'after' (datetime)
      'language' (string)
      """

      global dictFilters

      #NOTE: all following bools default to "True" so that, when there isn't a filter, the category always returns True
      boolTermHasSubstring = True
      if 'in-term' in dictFilters.keys():
            boolTermHasSubstring = dictFilters['in-term'] in eEntry.find('term').text

      boolDefHasSubstring = True
      if 'in-def' in dictFilters.keys():
            boolDefHasSubstring = dictFilters['in-def'] in eEntry.find('entry').text

      boolIsBeforeDatetime = True
      if 'before' in dictFilters.keys():
            #Boolean: returns True if the date is 
            boolIsBeforeDatetime = datetime.fromisoformat(eEntry.attrib['creationDate']) <= dictFilters['before']

      boolIsAfterDatetime = True
      if 'after' in dictFilters.keys():
            boolIsAfterDatetime = datetime.fromisoformat(eEntry.attrib['creationDate']) >= dictFilters['after']

      boolIsLanguage = True
      if 'language' in dictFilters.keys():
            boolIsLanguage = eEntry.attrib['language'] == dictFilters['language']

      return (boolTermHasSubstring & boolDefHasSubstring & boolIsBeforeDatetime & boolIsAfterDatetime & boolIsLanguage)

      


def update_listbox():
      #listbox.delete(0, (listbox.size() - 1)) #Before updating, delete the old values

      #delete the old items
      for item in tree.get_children():
             tree.delete(item)
      
      global undoFeature
      global xmlRoot
      undoFeature.add(xmlRoot)

      #organize the list of elements by ID
      eEntries = sorted(xmlRoot.findall("./*"), key=lambda entry: int(entry.attrib['n']))

      print("update_listbox: Sorting the entries:")

      #Go through each entry and add it to the treeview
      for eEntry in eEntries:
            if check_filter(eEntry):
                  print(f"update_listbox: Index of entry = {eEntry.attrib['n']}")
                  #Get the term, then check if it needs to be blocked out
                  term = eEntry.find("term").text
                  if HIDE_TERMS.get():
                        term = "**********"
                  

                  definition = eEntry.find("def").text
                  if HIDE_DEFS.get():
                        definition = "**********"
                  #defWidth = tree.column("Definition", option="width")
                  #defWidth = int(defWidth / 16)
                  #definition = textwrap.fill(definition, defWidth)

                  fTerm = f"Term: {term}; Def: {definition}"
                  #listbox.insert(tk.END, fTerm)
                  tree.insert('', "end", text=eEntry.attrib['n'], values=(term, definition))
      #Might not be a good idea to update every two seconds,
      #it resets the scrollbar every time
      #root.after(2000, update_listbox)

def print_xml():
       for entry in eEntries:
              print(f"Term: {entry.find("term").text}, Def: {entry.find("def").text}")


#     MOVE THIS UP!!!!
def entryToXml(entry: tk.Entry):
      """
      Return the XML node that's the source of an entry in the treeview
      """
      global tree

      num = tree.item(entry)['text']
      
      if DEBUG_MODE:
            print(f"{num} is the number of the entry")
            print(f"./*[@n='{num}']")
            for entry in xmlRoot.findall("./*"):
                  print(entry.attrib)
      
      entryElem = xmlRoot.findall(f"./*[@n='{num}']")
      #append a [0] in case there is an issue and multiple have the same ID
      entryElem = entryElem[0]

      if DEBUG_MODE: 
            print(entryElem)

            print(f"entryToXml: xmlRoot is {type(xmlRoot)}; entryElem is {type(entryElem[0])} and size {len(entryElem)}")

      return (entryElem)

def indexOfEntry(entry: tk.Entry):
      global tree
      return tree.index(entry)


#Deletes the selected item, unless "modifyEntry" is set to True, in which case it replaces an earlier entry
def modify_entry(modifyEntry = False):

      global xmlRoot
      
      #indices = listbox.curselection()
      print("Before delete: \n")
      print_xml()

      oldID = 0

      for item in tree.selection():
            entryElem = entryToXml(item)

            oldID = int(entryElem.attrib['n'])
            xmlRoot.remove(entryElem)

      if modifyEntry:
            add_to_xml(oldID)
      print("After delete: \n")

      #Final: use "tree.yview_moveto()" to get to the right spot after every delete. It's a float from 0.0f to 1.0f. 
      #How to get there: We need this info to figure out where to scroll: # of entries, and height of entries. Height of entries is harder
      #
      update_listbox()




deleteEntry = Button(listFrame, text="Delete", state=tk.DISABLED, command=modify_entry)

deleteEntry.grid(column=0, row=2)

#END LIST BOX

#Menu bar at top
menubar = Menu(root)
fileMenu = Menu(root, tearoff=0)

#save button
fileMenu.add_command(label="Save List")
#add tooltip to save button

fileMenu.add_checkbutton(label="Debug Mode", variable=DEBUG_MODE, onvalue=True, offvalue=False)
menubar.add_cascade(label="File", menu=fileMenu)

def __debug_mode__():
      global root
      global xmlRoot
      global menubar

      debugMenu = Menu(root, tearoff=0)
      debugMenu.add_command(label="Test assign_id", command=lambda: assign_id())
      menubar.add_cascade(label="DEBUG", menu=debugMenu)

      tree.config(show="tree headings")


def check_debug():
      global root

      if DEBUG_MODE.get():
              try:
                  menubar.index("DEBUG")
              except TclError:
                  __debug_mode__()
      else:
              try:
                  menubar.delete("DEBUG") #Need some sort of reverse debug method
                  tree.config(show="headings")

              except TclError:
                  pass
      root.after(300, check_debug)

      

#Add menubar to the root
root.config(menu=menubar)


"""
Handles all the events that take place when an item in the treeview is selected.

Add:
 - Activates the Delete button

 Edit:
"""
def activate_delete(event):
      deleteEntry['stat'] = tk.ACTIVE

#Get the text from the selection in the treeview. Activates in some unexpected
#circumstances: might be good to read up on what actually causes the "select" to trigger
def tree_select(event):

      global language
      items = tree.selection()

      #NOTE: these next two lines necessary. If I delete an item, then there is nothing selected but this function runs anyway. Trying to access "items[0]" below
      #throws an error as a result
      if(len(items) == 0):
            return
 
      selected = tree.item(items[0]) #Only grab the first selection
      print(selected)
      replace_text(entryA, selected["values"][0])
      replace_text(entryB, selected['values'][1])

      ####This section: get the index we want to set for the combobox
      entryXml = entryToXml(items[0])

      #get the language attribute:
      lang = entryXml.attrib['language']

      try:
            index = list(Languages.values()).index(lang)
      except (ValueError):
            print(f"FUNCTION tree_select: Value Error. Language ({lang}) in the XML entry doesn't match any values set in the program's defaults (see beginning of program)")
            index = 0

      #set the combo box language
      language.set(list(Languages.keys())[index])

      if DEBUG_MODE:
            print(f"Filter Lang Combobox: {filterLangs.get()} and its type: {type(filterLangs.get())}")



def replace_text(entry :tk.Entry, text :str):
      entry.delete(0, len(entry.get()))
      entry.insert(0, text)

def deactivate_delete(event):
       deleteEntry['stat'] = tk.DISABLED




tree.bind("<FocusIn>", activate_delete)
tree.bind("<<TreeviewSelect>>", tree_select)
tree.bind("<FocusOut>", deactivate_delete)

root.bind("<Mod1-Key-z>", control_z)
root.bind(SAVE_CHANGES_SHORTCUT, save_changes)

"""
Filters

Add filters to the treeview.

Also includes a button linking to an "Add to list" dialogue. Should also have a shortcut for adding all of today's vocab to one list and giving it a name

Also needs a button which clears filters on the treeview and all the fields

The following are planned:
- Date: Fromats: 1/1/2000 | 01/01/2000 | 2000-01-01 | 2000-1-1
- Language
-

Date Format: 1 box for month and day, another for year.

MY NOTES:

The ideal scenario is for the update_Listbox method to take the filters into account on every item. Update listbox works directly with the
XML, so keep that in mind. What's the easiest algorithm? Toughest thing to check is a range of dates, but that shouldn't be a problem with datetime.

WISHLIST:
The currently active filters are shown onscreen at all times - ESSENTIAL
"""

from datetime import datetime

def parse_date(entryXml: ET.Element) -> datetime:
      """
      Returns a date as a datetime object
      """

      return datetime.strptime(entryXml.attrib['creationDate'], "%Y%m%d")


def apply_filters():
      #must use global keyword so this function is able to modify the original variable
      global dictFilters

      #If the combobox is empty, we signal that we need to delete the filter
      if (filterLangs.get() == ''): 
            try: 
                  del dictFilters['language']
            except(KeyError):
                  print("Removing filter...no filter found. Continuing...")
      else:
            try:
                  #Get the language in its XML-ready version (on the right side of the assignment below), since the Combobox values aren't ever the same as the ones in the XML
                  dictFilters['language'] = Languages[filterLangs.get()]            
            except(KeyError):
                  messagebox.showerror("KeyError", f"Please select or enter a valid language into the combo box. Valid languages include: {(Languages.keys())}")

      update_listbox()



#set up the Frame to the right
frFilters = tk.Frame(root)
frFilters.grid(column=1, row=1)

filterLangs = ttk.Combobox(frFilters)
filterLangs.pack(anchor="n")
filterLangs['values'] = list(Languages.keys())

filterApply = tk.Button(frFilters, text="Apply Filters", command=apply_filters)
filterApply.pack()






"""
!!!
NOTE: here you need to figure out how to get the treeview to re-update every tick
"""

check_debug()

#Starts the on_closing() function when the window is destroyed (by hitting the X button, )
# Register the on_closing function to be called when the WM_DELETE_WINDOW protocol is invoked
root.protocol("WM_DELETE_WINDOW", on_closing)

update_listbox() #adds the terms to the listbox based on the xmlRoot

root.mainloop()