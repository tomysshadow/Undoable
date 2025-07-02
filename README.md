# Tkinter Undo and Redo undoable widgets

This is a Python conversion of the script [Undo and Redo undoable widgets,](https://wiki.tcl-lang.org/page/Undo+and+Redo+undoable+widgets) originally written by an anonymous contributor to Tcler's Wiki. I fixed any definite bugs that I happened to encounter while converting it but otherwise left the original behaviour intact. This script does not support any of the modern TTK widgets so it is not a drop-in solution for new Tkinter applications but it may serve as a useful base for your own undo/redo feature. Note that if you are only concerned about text editing, the Text widget already has a [built-in undo/redo stack](https://tkdocs.com/shipman/text-undo-stack.html) that you should use instead.

## Original Description

What follows is the description provided for the original Tcl script.

> Undoing events. Almost all modern programs use an undoing mechanism - so here is one for Tk.
> 
> Use the Undo - Redo or Control-z, Control-y to undo/redo the events you perform on the widgets in the interface created. Press any button, menu item, enter text in the text widget, use the spinbox move the sliders with either left drag or right-click - all these options are undoable.
> 
> The new 'class' is the undoable - its history of events can be regressed to an earlier state or progressed to recover a state which had been undone. The key is the "-kind XXX" where XXX is any Tk widget; undo operations are provided for entry, scale, spinbox widgets. Buttons (checkbox, radio button) may require some user code. Any widget can have an undocommand - a script that is exercised after a widget's state has been undone.
> 
> Each implementation of a widget may require special undo operations - for example if we have 30 objects, all red or yellow then a button changes the yellow objects to red then the undo for this button is NOT change all the red objects (back to) yellow, but change back all the objects which were previously changed. The implementation below provides an '-undocommand' option for each undoable widget; this must be created by the user to provide an exact undo mechanism. Typically each widget would be extended by the user to include a history of the effects of the widget, and then when its 'undo' command is called the last history event would be undone.