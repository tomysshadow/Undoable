import tkinter as tk
from tkinter import messagebox
from abc import ABC
import sys


def dbg(args):
  messagebox.showinfo(message=str(args))


def testop(s, S, P, V):
  print(f"testop validating {s} {S} -> {P} type {V}")
  return True # or False if not OK!


def undomenu(menubtn, menu):
  print(f"Undoing {menubtn} {menu} [{menubtn.cget('text')}]")


def scalevalue(w, v):
  print(f"scale {w} set to value {v}")


def test_undo():
  # create an interface using "undoable" Tk items.
  window = tk.Tk()
  
  fr = tk.Frame(window)
  fr.pack()
  
  undo = tk.Button(fr, text="Undo", command=undolast)
  undo.pack(side=tk.LEFT)
  
  redo = tk.Button(fr, text="Redo", command=redolast)
  redo.pack(side=tk.LEFT)
  
  window.bind("<Control-z>", lambda e: undolast())
  window.bind("<Control-y>", lambda e: redolast())
  
  undos = tk.Button(fr, text="Show Undos", command=showundos)
  undos.pack(side=tk.LEFT)
  
  redos = tk.Button(fr, text="Show Redos", command=showredos)
  redos.pack(side=tk.LEFT)
  
  exit_ = tk.Button(fr, text="Exit", command=sys.exit)
  exit_.pack(side=tk.LEFT)
  
  testfr = tk.Frame(window)
  testfr.pack()
  
  e1 = UndoableEntry(testfr, validate="focus")
  e1.pack(side=tk.TOP)
  
  vcmd_testop = (testfr.register(testop), "%s", "%S", "%P", "%V")
  
  e2 = UndoableEntry(testfr, vcmd=vcmd_testop, validate="all")
  e2.pack(side=tk.TOP)
  
  sp2 = UndoableSpinbox(testfr, from_=1, to=12, vcmd=vcmd_testop, validate="all")
  sp2.pack(side=tk.TOP)
  
  menval = tk.StringVar()
  menval.set("Number")
  
  b1 = tk.Menubutton(testfr, bg="red", textvariable=menval, bd=2, relief=tk.RAISED)
  b1.pack(side=tk.TOP)
  
  b1_menu1 = UndoableMenu(b1, tearoff=0, undocommand=lambda: undomenu(b1, b1_menu1))
  b1["menu"] = b1_menu1
  
  def b1_choose_item(num):
    print(f"menu item {num} chosen")
    menval.set(num)
  
  for num in ("One", "Two", "Three"):
    b1_menu1.add("command", label=num, command=lambda num=num: b1_choose_item(num))
  
  b1_menu1_cascade = UndoableMenu(b1_menu1, tearoff=0,
    undocommand=lambda: print(f"Undoing {b1_menu1_cascade}"))
  
  b1_menu1.add("cascade", label="Roman", menu=b1_menu1_cascade)
  
  for num in ("I", "II", "III"):
    b1_menu1_cascade.add("command", label=num, command=lambda num=num: b1_choose_item(num))
  
  def bmen1_choose_item(num):
    print(f"menu item {num} chosen")
  
  bmen1 = tk.Menubutton(testfr, text="Dropdown Menu", bd=2, relief=tk.RAISED)
  bmen1.pack(side=tk.TOP)
  
  bmen1_menu1 = UndoableMenu(bmen1, tearoff=0,
    undocommand=lambda: undomenu(bmen1, bmen1_menu1))
  
  bmen1["menu"] = bmen1_menu1
  
  for num in ("One", "Two", "Three"):
    bmen1_menu1.add("command", label=num,
      command=lambda num=num: bmen1_choose_item(num))
  
  bmen1_menu1_cascade = UndoableMenu(bmen1_menu1, tearoff=0,
    undocommand=lambda: print(f"Undoing {bmen1_menu1_cascade}"))
  
  bmen1_menu1.add("cascade", label="Roman", menu=bmen1_menu1_cascade)
  
  for num in ("I", "II", "III"):
    bmen1_menu1_cascade.add("command", label=num,
      command=lambda num=num: bmen1_choose_item(num))
  
  b2 = UndoableButton(
    testfr,
    text="Press Me",
    command=lambda: print("Button pressed"),
    undocommand=lambda: print("Button press undone")
  )
  
  b2.pack(side=tk.TOP)
  
  b3 = UndoableCheckbutton(
    testfr,
    text="Check Me",
    command=lambda: print("checkButton pressed"),
    undocommand=lambda: print("checkButton press undone")
  )
  
  b3.pack(side=tk.TOP)
  
  b4 = UndoableRadiobutton(
    testfr,
    text="Check Me",
    command=lambda: print("radioButton pressed"),
    undocommand=lambda: print("radioButton press undone")
  )
  
  b4.pack(side=tk.TOP)
  
  def validate_e3(s, S, P, V):
    print(f"validating {s} {S} -> {P} type {V}")
    return True
  
  e3 = UndoableEntry(testfr,
    vcmd=(testfr.register(validate_e3), "%s", "%S", "%P", "%V"),
    validate="all"
  )
  
  e3.pack(side=tk.TOP)
  
  s1 = UndoableScale(testfr, from_=100, to=200,
    command=lambda v: scalevalue(s1, v), orient=tk.HORIZONTAL)
  
  s1.pack(side=tk.TOP)
  
  s2 = UndoableScale(testfr, from_=0, to=120,
    command=lambda v: scalevalue(s2, v), orient=tk.HORIZONTAL)
  
  s2.pack(side=tk.TOP)
  
  lb2 = UndoableListbox(testfr, command=lambda: print("Listbox Selected"),
    undocommand=lambda: print("Listbox undone"))
  
  lb2.pack(side=tk.TOP)
  
  for fruit in ("Apple", "Peach", "Pear", "Banana", "Strawberry",
    "Lingonberry", "Blackberry", "Damson", "Plum"):
    lb2.insert(tk.END, fruit)
  
  tx1 = UndoableText(testfr, undo=True)
  tx1.pack(side=tk.TOP)
  
  window.mainloop()


"""
This is the important part - a list of undoable events, and a redo list (in case you undid
an event and realised it should not have been undone).

Each undo event has two parts (it is a list) - the record of old values needing to be undone,
and the redo event (a copy of the original event).

The class undoable is a [polymorphism%|%polymorphic] or Template class which records the actions
of any Tk widget and can 'undo' these actions.

Records events in all undoable widgets as a list, then you can undo the list
(and possibly redo). All Tk widgets (except canvas?) can be used as undoables.
"Polymorphism" means that the undoable widget can inherit from any of the Tk widgets.
It should also be able to represent an Iwidget or BWidget.

Usually 'entry' 'menu' and 'scale' widgets won't need an undocommand as they call the
return the value of the widget to its previous value, which calls the standard        
'item changed command' for the widget (which should cause all changes to be reset
as if the menu/entry/scale had been set manually).

undoableCmd is the place where the undo events are coded and interpreted.
"""

undoings = [] # list of undoable things - each is a 2 part list
        # first the arguments to undo the operation;
        # then the arguments to redo the operation.
redoings = [] # list of redoable things - copy of those undoings which have been undone.


def showundos(): # display list of undo operations.
  for un, re in undoings:
    print(f"Undo:: {un} ::redo:: {re}")


def showredos(): # display list of redo operations.
  for re, un in redoings:
    print(f"Redo:: {re} ::undo:: {un}")


def undolast(): # undoes last undoable operation.
  if not undoings:
    print("No more undoable events")
    return
  
  undothis = undoings.pop()
  undocommand = undothis[0]
  widget = undocommand[0]
  widget.undo(undocommand)
  
  redoings.append(undothis)


def redolast():
  if not redoings: return
  
  redothis = redoings.pop()
  redocommand = redothis[1]
  widget = redocommand[0]
  widget.undo(redocommand)
  widget.update_idletasks()
  
  undoings.append(redothis)


# an undoable is a widget
# and allows new smooth shaped buttons.
class Undoable(ABC):
  # define the option list and default values
  # undoing is true if we are in an undo operation (does not get put on the undoable list)
  # undocommand may be supplied for items such as buttons which may invoke complex operations
  #  and hence require a complex undo operation.
  def __init__(self, master=None, undoing=False, undocommand=None, command=None,
    validatecommand=None, vcmd=None, oldvalue=0, **kw):
    # a dictionary of options specific to the undoable class
    self.props = {
      "undoing": undoing,
      "undocommand": undocommand,
      "command": command,
      "oldvalue": oldvalue,
      "vcmd": validatecommand if validatecommand else vcmd
    }
    
    self._registered_commands = {}
    
    # make the base widget
    super().__init__(master, **kw)
    
    try: super().configure(command=self._undocmd)
    except tk.TclError: pass
    
    try: super().configure(vcmd=self._register_vcmd())
    except tk.TclError: pass
  
  def _register_command(self, command):
    registered_commands = self._registered_commands
    if command in registered_commands: return registered_commands[command]
    
    command_cbname = self.register(command) if callable(command) else command
    registered_commands[command] = command_cbname
    return command_cbname
  
  def _register_vcmd(self):
    result = (self.register(self._undovcmd), "%P")
    
    try: return result + self.props["vcmd"][1:]
    except TypeError: return result
  
  def _call_command(self, command):
    command_cbname = self._register_command(command)
    return self.tk.call(command_cbname) if command_cbname else None
  
  def _undocmd(self, *args):
    # assemble complete validation command - saves history of behaviours
    command_cbname = self._register_command(self.props["command"])
    if not command_cbname: return None
    
    self.undooptions(*args)
    return self.tk.call(command_cbname, *args)
  
  def _undovcmd(self, P, *args):
    # assemble complete Entry validation command - saves history of behaviours
    self.undooptions(P)
    
    try: vcmd_cbname = self.props["vcmd"][0]
    except TypeError: return True
    
    return self.tk.call(vcmd_cbname, *args) if vcmd_cbname else True
  
  def configure(self, cnf={}, **kw):
    kw = cnf | kw
    kw_len = len(kw)
    
    # 3 scenarios:
    #
    # kw is empty -> return all options with their values
    # kw is one element -> return current values
    # kw is 2+ elements -> configure the options
    #print(f"Config comd {self} {kw} {kw_len}")
    
    if kw_len == 0: # return all options
      return super().configure()
    
    if kw_len == 1 and next(iter(kw.values())) is None: # return argument values
      return super().configure(**kw) | self.props
    
    cnf = {}
    
    for option, value in kw.items(): # >1 arg - an option and its value
      # go through each option:
      if option == "validatecommand": option = "vcmd"
      
      if option in self.props:
        self.props[option] = value
        
        if option == "vcmd":
          cnf["vcmd"] = self._register_vcmd()
        
        continue
      
      cnf[option] = value
      
    return super().configure(**cnf)
  
  def cget(self, key):
    if key == "validatecommand": key = "vcmd"
    
    try: return self.props[key]
    except KeyError: return super().cget(key)
  
  def undooptions(self, *args): # save undooptions sufficient to undo and redo an action
    if not self.cget("undoing"):
      # store state before and after event change.
      #for un in undoings: print(f"Undo:: {un}")
      
      # not in an undo so save event.
      undoings.append(self._data(args))
      redoings.clear()
    else:
      #print(f"In undo dont save event {args}")
      pass
    
    self.props["oldvalue"] = self.oldvalue() # saved for redo record.
  
  def _data(self, args):
    undodata = (self, f"Dont know how to undo {self.winfo_class()}")
    
    try: dodata = args[-1] # and record the redo event
    except KeyError: dodata = None
    
    return (undodata, dodata)
  
  def undo(self, args):
    # the action invoked by an undo
    self.props["undoing"] = True
    
    try:
      self._revert(args)
      self._call_command(self.cget("undocommand"))
      self.update_idletasks() # updates all the -vcmds etc before setting the undo flag
    finally:
      self.props["undoing"] = False # start collecitng widget events for undoing again
  
  def _revert(self, args):
    print(f"? undo {self.winfo_class()} event {args}")
  
  def oldvalue(self):
    return ""

class UndoableMenu(Undoable, tk.Menu):
  def _data(self, args):
    # self.master is the menu parent - button or cascade
    menubutt = self.master
    
    while menubutt.winfo_class() != "Menubutton":
      # ascend tree to an actual menubutton.
      menubutt = menubutt.master
    
    tvar = menubutt.cget("text")
    return ((self, menubutt, tvar), (self, menubutt, args))
  
  def _revert(self, args): # here we want to perform some undoing mechanism
    tvar = tk.Variable(name=args[1].cget("textvariable"))
    if tvar: tvar.set(args[2])
    
    print(f"menu {self} undo {self.winfo_class()} event {args}")
  
  def add(self, itemType, cnf={}, **kw):
    # for type menu add an option (command etc) means add an undoable menu item
    kw = cnf | kw
    
    try:
      pog = kw["label"]
      command = kw["command"]
    except KeyError: return super().add(itemType, **kw)
    
    command_cbname = self._register_command(command)
    
    def undocmd():
      if not command_cbname: return None
      
      self.undooptions(pog)
      return self.tk.call(command_cbname)
    
    kw["command"] = undocmd
    return super().add(itemType, **kw)

class UndoableButtonBase(ABC):
  def _data(self, args):
    undodata = (self, args)
    return (undodata, undodata)
  
  def _revert(self, args): # these Tk items usually need their own undocommand
    print(f"Undoing {self.winfo_class()} called {self}")

class UndoableButton(UndoableButtonBase, Undoable, tk.Button): pass
class UndoableCheckbutton(UndoableButtonBase, Undoable, tk.Checkbutton): pass
class UndoableRadiobutton(UndoableButtonBase, Undoable, tk.Radiobutton): pass

class UndoableEntry(Undoable, tk.Entry):
  def _data(self, args):
    return ((self, self.oldvalue()), (self, args[0]))
  
  def _revert(self, args):
    self.selection_range(0, tk.END)
    
    if self.selection_present():
      self.delete("%s.%s" % (tk.SEL, tk.FIRST), "%s.%s" % (tk.SEL, tk.LAST))
    
    self.insert(tk.INSERT, args[1]) # insert
  
  def oldvalue(self):
    return self.get()

class UndoableScale(Undoable, tk.Scale):
  def _data(self, args):
    oldvalue = self.oldvalue()
    cget_oldvalue = self.cget("oldvalue")
    
    print(f"Undo scale save {self} {oldvalue} {cget_oldvalue}")
    return ((self, cget_oldvalue), (self, oldvalue))
  
  def _revert(self, args): # scale set should call its own -command option
    self.set(args[1])
  
  def oldvalue(self):
    return self.get()

class UndoableListbox(Undoable, tk.Listbox):
  def __init__(self, master=None, **kw):
    super().__init__(master, **kw)
    
    self.bind("<ButtonPress-1>", lambda e: self.select(e.y))
  
  def _data(self, args):
    return ((self, self.curselection()), (self, args[0]))
  
  def _revert(self, args):
    self.selection_clear(0, tk.END)
    selection = args[1]
    
    if selection:
      self.selection_set(selection)
      print(f"Undo {args[0]} oldvalues {args[1]}")
  
  def select(self, y): # in Listbox - no automatic setting of current selection in Tk(!)
    y = self.nearest(y)
    self.undooptions(y)
    self.selection_set(y)
    self._call_command(self.props["command"])

class UndoableText(Undoable, tk.Text):
  def __init__(self, master=None, **kw):
    super().__init__(master, **kw)
    
    def text_savepoint(e):
      self.text_savepoint()
    
    self.bind("<Enter>", text_savepoint)
    self.bind("<Leave>", text_savepoint)
  
  def _data(self, args): # NB this records undo state when mouse enters into text widget
    undodata = (self, self.oldvalue())
    return (undodata, undodata)
  
  def _revert(self, args):
    self.delete("1.0", tk.END)
    self.insert(tk.END, args[1])
  
  def text_savepoint(self): # mouse has entered or left text - create an undo event
    self.undooptions()
  
  def oldvalue(self):
    return self.get("1.0", tk.END)

class UndoableSpinbox(Undoable, tk.Spinbox):
  def _data(self, args):
    return ((self, self.get()), (self, args[0]))
  
  def _revert(self, args):
    self.tk.call(str(self), "set", args[1])

if __name__ == "__main__":
  test_undo() # call the test routine
