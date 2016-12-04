import sys
import wx

import threading
import time

class RedirectText(object):
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)

class Concur(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.iterations = 0
        self.daemon = True  # OK for main to exit even if instance is still running
        self.paused = True  # start out paused
        self.state = threading.Condition()

    def run(self):
        self.resume() # unpause self
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified
            # do stuff
            time.sleep(.1)
            self.iterations += 1
            print(self.iterations)

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait

class KeepRunning(object):
    def __init__(self, seconds=10):
        self.run_time = seconds
        self.start_time = time.time()

    @property
    def condition(self):
        return time.time()-self.start_time < self.run_time

class elementsWindow(wx.Frame):
    running = KeepRunning()
    concur = Concur()

    iterations = ''

    def __init__(self, *args, **kwargs):
        super(elementsWindow, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        logMultiline = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        hbox1.Add(logMultiline, flag=wx.RIGHT, border=10)

        # 6th: Buttons Container
        buttonsContainer = wx.BoxSizer(wx.HORIZONTAL)

        startButton = wx.Button(panel, label='Start', size=(70, 30))
        startButton.Bind(wx.EVT_BUTTON, self.OnStart)
        buttonsContainer.Add(startButton)

        pauseButton = wx.Button(panel, label='Pause', size=(70, 30))
        pauseButton.Bind(wx.EVT_BUTTON, self.OnPause)
        buttonsContainer.Add(pauseButton)

        resumeButton = wx.Button(panel, label='Resume', size=(70, 30))
        resumeButton.Bind(wx.EVT_BUTTON, self.OnResume)
        buttonsContainer.Add(resumeButton)

        quitButton = wx.Button(panel, label='EXIT', size=(70, 30))
        quitButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        buttonsContainer.Add(quitButton, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(buttonsContainer, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)
        panel.SetSizer(vbox)

        redir = RedirectText(logMultiline)
        sys.stdout = redir

        self.SetSize((600, 600))
        self.Center()
        self.Show(True)

    def OnStart(self, e):
        self.concur.start()
        # self.iterations = self.concur.iterations

    def OnPause(self, e):
        self.concur.pause()
        # self.iterations = self.concur.iterations

    def OnResume(self, e):
        self.concur.resume()
        # self.iterations = self.concur.iterations

    def OnQuit(self, e):
        self.Close()

def main():
    app = wx.App()
    elementsWindow(None, title='Threading Test')
    app.MainLoop()

if __name__ == '__main__':
    main()


