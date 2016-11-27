import wx

from scrapy.crawler import CrawlerProcess
from recursiveCrawling.recursiveCrawling.spiders import Spider

class elementsWindow(wx.Frame):

    spider = Spider.TestSpider()
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    domain = '';

    def __init__(self, *args, **kwargs):
        super(elementsWindow, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        # build a menu
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

        # 1st: build a panel
        panel = wx.Panel(self)
        # 2nd: build a vertical box
        vbox = wx.BoxSizer(wx.VERTICAL)
        # 3rd: build a horizontal box inside the vertical one
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        # set a label
        label1 = wx.StaticText(panel, label='Set Domain')

        # set a scanner right to the static label
        hbox1.Add(label1, flag=wx.RIGHT, border=10)

        urlField = wx.TextCtrl(panel, value='Enter your url')
        self.Bind(wx.EVT_TEXT, self.OnTypeText, id=urlField.GetId())

        hbox1.Add(urlField, proportion=5)

        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        vbox.Add((-1, 10))

        # 4th: build another horizontal box inside the vertical one
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        label2 = wx.StaticText(panel, label='Result')
        hbox2.Add(label2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        # 5th: add multiple lines
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        scanner2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(scanner2, proportion=5, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=5, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)

        vbox.Add((-1, 10))

        # 6th: Buttons Container
        buttonsContainer = wx.BoxSizer(wx.HORIZONTAL)

        parseButton = wx.Button(panel, label='Parse', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.OnParse, id=parseButton.GetId())

        buttonsContainer.Add(parseButton)

        quitButton = wx.Button(panel, label='EXIT', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.OnQuit, id=quitButton.GetId())

        buttonsContainer.Add(quitButton, flag=wx.LEFT | wx.BOTTOM, border=5)

        vbox.Add(buttonsContainer, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)
        # set the size of the panel according to the vbox
        panel.SetSizer(vbox)
        # set size of the panel
        self.SetSize((600, 600))
        # center and show the window
        self.Center()
        self.Show(True)

    def OnQuit(self, e):
        self.Close()
        self.process._graceful_stop_reactor();

    def OnParse(self, e):
        self.SetTitle(self.domain)

        #TODO add domain sanity check
        self.process.crawl(self.spider, start_urls=self.domain)
        self.process.start()

    def OnTypeText(self, e):
        self.domain = e.EventObject.Value;

def main():
    app = wx.App()
    elementsWindow(None, title='Demica WebArchiver')
    app.MainLoop()

if __name__ == '__main__':
    main()