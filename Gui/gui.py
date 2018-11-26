"""
All gui related work is located and handled here.

File Name: gui.py
File Version: 0.0.1
Updated: 26/11/2018
"""

import tkinter as tk
import tkinter.ttk as ttk

UPDATE_RATE = 1000


class Gui:
    def __init__(self, master):
        self.master = master
        self.gui = None
        self.create(master)
        self.updater()

    def updater(self):
        self.master.after(UPDATE_RATE, self.updater)

    def bringtoFront(self, root):
        root.attributes("-topmost", True)
        root.focus_force()

    def create(self, root):
        """
        Declare and position all widgets.
        :return: None
        """
        frame = VerticalScrolledFrame(root)
        frame.pack()
        self.gui = frame.interior
        """
        Create Menu
        """
        menuBar = tk.Menu(root)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New Session", command=lambda: self.data.newProject(self.master,
                                                                                       frame.interior,
                                                                                       self.config,
                                                                                       self.data))
        fileMenu.add_command(label="Open Session", command=lambda: self.data.load(self.master, frame.interior,
                                                                                  settings=self.config,
                                                                                  project=True))
        fileMenu.add_command(label="Close Session", command=None)
        fileMenu.add_separator()
        fileMenu.add_command(label="Settings", command=lambda: self.data.dataMap(frame.interior, new=True))
        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=root.quit)

        menuBar.add_cascade(label="File", menu=fileMenu)

        root.config(menu=menuBar)

        """
        Create Status Bar
        """
        statusBar = tk.Label(root, text="Ready", bd=3, relief=tk.RIDGE)
        statusBar.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.TRUE)

        """
        Prepare canvas.
        """
        frame1 = tk.Frame(frame.interior, padx=10, pady=10)
        frame1.pack()
        frame1 = ttk.Notebook(root)
        frame1.pack()


# FIXME: Crashes when used in the macOS environment.
class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    * Code fetched from https://gist.github.com/EugeneBakin/76c8f9bcec5b390e45df
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, scrollregion=(0, 0, 800, 600), width=800, height=600, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        def _on_mousewheel(event):
            canvas.yview_scroll(-1 * event.delta, 'units')

        #canvas.bind_all('<MouseWheel>', _on_mousewheel)
