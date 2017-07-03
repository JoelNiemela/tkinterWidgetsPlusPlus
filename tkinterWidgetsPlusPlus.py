from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

#TkinterWidgetsPlusPlus
class Dialog(Toplevel):
	def __init__(self, parent, title=None, frame=None, topmost=True, closable=False):
		top = Toplevel.__init__(self, parent)
		if not closable:
			self.protocol("WM_DELETE_WINDOW", lambda: print("Can't close window"))
		if not title == None:
			self.title(title)
			if topmost:
				self.wm_attributes("-topmost", 1)

class ToolTip(object):
	def __init__(self, widget, text=None, wraplength=None):
		self.widget = widget
		self.text = text
		self.widget.bind("<Enter>", self.enter)
		self.widget.bind("<Leave>", self.leave)
		self.widget.bind("<ButtonPress>", self.leave)
		self.widget.bind("<Motion>", self.motion)
		self.top = None
		self.id = None
		self.x = None
		self.y = None
		self.wraplength = wraplength

	def motion(self, event):
		self.x, self.y = event.x, event.y
		#print(self.x, self.y)

	def enter(self, event):
		self.id = self.widget.after(500, self.show_tooltip)

	def leave(self, event):
		top = self.top
		self.top = None
		if top:
			top.destroy()
		id = self.id
		self.id = None
		if id:
			self.widget.after_cancel(id)
	
	def show_tooltip(self):
		x = y = 0
		x, y, cx, cy = self.widget.bbox("insert")
		x += self.widget.winfo_rootx() + self.x + 5
		y += self.widget.winfo_rooty() + self.y - 5
		# creates a toplevel window
		self.top = Toplevel(self.widget)
		# Leaves only the label and removes the app window
		self.top.wm_overrideredirect(True)
		self.top.wm_geometry("+%d+%d" % (x, y))
		label = Label(self.top, text=self.text, justify='left', bg="gray90", relief='solid', bd=1, wraplength=self.wraplength)
		label.pack(ipadx=1)

class SideMenu(Frame):
	def __init__(self, parent, orient=VERTICAL, frame=None):
		Frame.__init__(self, parent, bd=1, relief=RAISED, )
		self.orient = orient
		self.parent = parent
		#self.shortcutKey = shortcutKey
		self.menus = []
		self.frame = Frame(self)
		self.contentframe = None

	def add_menu(self, label=None, tearoff=True, underline=None):
		menuButton = Menubutton(self, text=label, underline=underline)
		menu = Menu(menuButton, tearoff=tearoff)
		menuButton.config(menu=menu)
		if self.orient == HORIZONTAL:
			menuButton.pack(side=RIGHT, fill=BOTH)
		if self.orient == VERTICAL:
			menuButton.pack(side=TOP, fill=BOTH)
		self.menus.append(menu)
		return menu

	def add_command(self, label=None, command=None, relief=FLAT, underline=None):
		commandButton = Button(self, text=label, command=command, relief=relief, underline=underline)
		if self.orient == HORIZONTAL:
			commandButton.pack(side=RIGHT, fill=BOTH)
		if self.orient == VERTICAL:
			commandButton.pack(side=TOP, fill=BOTH)
		if not underline == None:
			self.parent.bind("<Alt-" + label[underline].lower() + ">", lambda event: commandButton.event_generate('<<Invoke>>'))
			self.parent.bind("<Alt-" + label[underline].upper() + ">", lambda event: commandButton.event_generate('<<Invoke>>'))
		return commandButton

	def add_frame(self, frame):
		self.contentframe = frame
		self.contentframe.pack(side=LEFT, fill=BOTH)
