from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
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

w = Tk()
w.title("Notepad")
text = Text(width=1, height=1)
yscroll = Scrollbar(w, command=text.yview)
text.config(yscrollcommand=yscroll.set)

#Variables
openfilename = None
saved = True

def new(event=None):
	global openfilename
	global saved
	if not saved:
		if messagebox.askyesno("File not saved", str(str(openfilename).split("/")[len(str(openfilename).split("/")) - 1]) + " is not saved.\nAre you sure you want to continue?"):
			text.delete(1.0, END)
			openfilename = None
	else:
		text.delete(1.0, END)
		openfilename = None

def openfile(event=None):
	global openfilename
	global saved
	file = filedialog.askopenfile(parent=w, mode="rb", title="Select a file")
	if file != None:
		if not saved:
			if messagebox.askyesno("File not saved", str(str(openfilename).split("/")[len(str(openfilename).split("/")) - 1]) + " is not saved.\nAre you sure you want to continue?"):
				saved = True
				contents = file.read()
				openfilename = file.name
				text.delete(1.0, END)
				text.insert("1.0",contents)
				file.close()
		else:
			saved = True
			contents = file.read()
			openfilename = file.name
			text.delete(1.0, END)
			text.insert("1.0",contents)
			file.close()

def saveas(event=None):
	global openfilename
	global saved
	file = filedialog.asksaveasfile(mode="w")
	if file != None:
		saved = True
		openfilename = file.name
		data = text.get("1.0", END+'-1c')
		file.write(data)
		file.close()

def save(event=None):
	global openfilename
	global saved
	if openfilename == None:
		saveas()
	else:
		saved = True
		file = open(str(openfilename), "w")
		data = text.get("1.0", END+'-1c')
		file.write(data)
		file.close()

def close(event=None):
	if messagebox.askyesno("Quit", "Do you really want to quit?"):
		exit()

def not_saved(event):
	global saved
	if event.keysym != "Control_L":
		saved = False

def settings():
	global v
	top = Toplevel()
	top.lift()
	top.title("Options")

	textColor = StringVar(top)
	textColor.set("White")

	w = OptionMenu(top, textColor, "White", "two", "three")
	w.pack()

#Create Menu Bar
menu = Menu(w, tearoff=False)
w.config(menu=menu)
#Add menus to the Menu Bar
filemenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=filemenu, underline=0)
editmenu = Menu(menu, tearoff=False)
menu.add_cascade(label="Edit", menu=editmenu, underline=0)
optionsmenu = Menu(menu, tearoff=False)
menu.add_cascade(label="Options", menu=optionsmenu, underline=0)
menu.add_command(label="+", command=lambda: sideMenu.pack(side=RIGHT, fill=BOTH, anchor=N))
#Add buttons to the file menu
filemenu.add_command(label="New", command=new, underline=0, accelerator="Ctrl+n")
filemenu.add_command(label="Open...", command=openfile, underline=0, accelerator="Ctrl+o")
filemenu.add_command(label="Save", command=save, underline=0, accelerator="Ctrl+s")
filemenu.add_command(label="Save As...", command=saveas, accelerator="F12")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=close, underline=1, accelerator="Ctrl+x")
#Add buttons to the options menu
optionsmenu.add_command(label="Settings", command=settings, underline=0)
#Add buttons to the edit menu
editmenu.add_command(label="Undo", command=text.edit_undo, underline=0, accelerator="Ctrl+z")
editmenu.add_command(label="Redo", command=text.edit_redo, underline=0, accelerator="Ctrl+y")

#Create Side Menu bar
sideMenu = SideMenu(w, orient=VERTICAL)
#Add menus to the Side Menu Bar
sideMenu.add_command(label="-", command=lambda: sideMenu.pack_forget())
editmenu = sideMenu.add_menu(label="Edit", underline=0, tearoff=False)
filemenu = sideMenu.add_menu(label="file", underline=0, tearoff=False)
#Add buttons to the edit menu
editmenu.add_command(label="New")
#pack widgets
yscroll.pack(side=RIGHT, fill=Y)
text.pack(side=LEFT, fill=BOTH, expand=YES)
sideMenu.pack(side=RIGHT, fill=BOTH, anchor=N)
sideMenu.pack_forget()

w.update()
w.minsize(w.winfo_width(), w.winfo_height())
w.update()
w.geometry('{}x{}'.format(800, 400))

def tick():
	global saved
	global openfilename
	if saved:
		if openfilename == None:
			w.title("Notepad Untitled")
		else:
			w.title("Notepad " + str(openfilename))
	else:
		if openfilename == None:
			w.title("Notepad Untitled *")
		else:
			w.title("Notepad " + str(openfilename) + " *")
	w.after(100, tick)

text.bind("<Key>", not_saved)
w.bind("<Control-s>", save)
w.bind("<Control-o>", openfile)
w.bind("<Control-n>", new)
w.bind("<Control-x>", close)
w.bind("<F12>", saveas)
w.after(100, tick)
w.mainloop()
