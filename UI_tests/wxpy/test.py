import wx

class ChatPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        main_layout = wx.BoxSizer(wx.VERTICAL)

        chat_layout = wx.BoxSizer(wx.HORIZONTAL)
        
        chat_messages = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        connected_list = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        chat_layout.Add(chat_messages, 1, wx.ALL | wx.EXPAND, 5)
        chat_layout.Add(connected_list, 0, wx.ALL | wx.EXPAND, 5)

        input_layout = wx.BoxSizer(wx.HORIZONTAL)
        
        self.chat_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.chat_input.Bind(wx.EVT_TEXT_ENTER, self.send)
        chat_send = wx.Button(self, label="Send")
        chat_send.Bind(wx.EVT_BUTTON, self.send)
        
        input_layout.Add(self.chat_input, 1, wx.ALL, 5)
        input_layout.Add(chat_send, 0, wx.ALL | wx.RIGHT, 5)

        main_layout.Add(chat_layout, 1, wx.ALL | wx.EXPAND, 5)
        main_layout.Add(input_layout, 0, wx.ALL | wx.EXPAND | wx.BOTTOM, 5)

        self.SetSizer(main_layout)

    def send(self, event):
        text = self.chat_input.GetValue()
        if text:
            print(text)

class Test(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="ChtCnt")
        panel = ChatPanel(self)

        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        connect = file_menu.Append(wx.ID_ANY, "Connect", "Connect to server")

        menu_bar.Append(file_menu, "File")

        self.Bind(wx.EVT_MENU, self.connect, connect)
        
        self.SetMenuBar(menu_bar)
        self.Show()

    def connect(self, event):
        print("connect")
    

if __name__ == "__main__":
    app = wx.App()
    frame = Test()
    app.MainLoop()
