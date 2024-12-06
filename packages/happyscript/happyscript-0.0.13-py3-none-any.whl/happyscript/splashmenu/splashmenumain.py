import os
class SplashMenu():
    def __init__(self, mainfilename, num_x, num_y, border = 50):
        import wx
        from .splashmenuform import SplashMenuForm
        self.mainfile = mainfilename
        self.maindir = os.path.dirname(os.path.abspath(mainfilename))
        self.app = wx.App()
        self.top = SplashMenuForm(num_x, num_y, border)
    def set_button(self, x, y, image, program, arguments=None):
        imgfile = os.path.join(self.maindir, image)
        if not os.path.exists(imgfile):
            imgfile = os.path.abspath(image)
            if not os.path.exists(imgfile):
                raise ValueError( f"Could not find file {image}")
        progfile = os.path.join(self.maindir, program)
        if not os.path.exists(progfile):
            progfile = os.path.abspath(program)
            if not os.path.exists(progfile):
                raise ValueError( f"Could not find file {program}")
        if arguments is None:
            arguments = list()
        elif type(arguments) is not list:
            arguments = [ arguments ]
        for i in range(0,len(arguments)):
            if type(arguments[i]) is not str:
                arguments[i] = str(arguments[i])
        self.top.set_button(x, y, imgfile, progfile, arguments)
    def run(self):
        self.top.Show()
        self.app.MainLoop()
