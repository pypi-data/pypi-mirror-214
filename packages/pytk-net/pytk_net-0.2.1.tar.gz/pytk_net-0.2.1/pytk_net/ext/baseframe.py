from tkinter.ttk import Frame


class BaseFrame(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack_propagate(False)
