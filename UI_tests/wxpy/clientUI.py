import wx
from client import Client


class ChatPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        main_layout = wx.BoxSizer(wx.VERTICAL)
        

        ### CHAT ZONE
        chat_layout = wx.BoxSizer(wx.HORIZONTAL)
        
        self.chat_messages = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.connected_list = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        chat_layout.Add(self.chat_messages, 1, wx.ALL | wx.EXPAND, 5)
        chat_layout.Add(self.connected_list, 0, wx.ALL | wx.EXPAND, 5)

        ### INPUT ZONE
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
            self.chat_input.Clear()
            self.parent.SendMessage(text)

    def display_message(self, message):
        self.chat_messages.AppendText("{}: {}\n".format(message.username, message.content))
    
    def display_connected(self, message):
        self.connected_list.Clear()
        for user in message.content:
            self.connected_list.AppendText("{}\n".format(user))

class IPinput(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title = 'Connect', size = (300,200))
        panel = wx.Panel(self)

        main_layout = wx.BoxSizer(wx.VERTICAL)
        
        ### USERNAME
        self.input_user = wx.TextCtrl(panel)
        username_layout = wx.BoxSizer(wx.HORIZONTAL)
        username_label = wx.StaticText(panel, label = 'Username:')
        username_layout.Add(username_label, 0, wx.ALL, 5)
        username_layout.Add(self.input_user, 1, wx.ALL, 5)


        ### IP PORT
        ip_port_layout = wx.BoxSizer(wx.HORIZONTAL)
        ip_label = wx.StaticText(panel, label = 'Server IP')
        self.input_ip = wx.TextCtrl(panel)
        colon_label = wx.StaticText(panel, label = ':')
        self.input_port = wx.TextCtrl(panel, size = (125, -1))

        ip_port_layout.Add(ip_label, 0, wx.ALL, 5)
        ip_port_layout.Add(self.input_ip, 0, wx.ALL | wx.EXPAND, 5)
        ip_port_layout.Add(colon_label, 0, wx.ALL, 5)
        ip_port_layout.Add(self.input_port, 0, wx.ALL, 5)

        ### BUTTONS

        button_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(panel, wx.ID_OK, label = 'OK')
        self.cancel_button = wx.Button(panel, wx.ID_CANCEL, label = 'Cancel')

        button_layout.Add(self.ok_button, 0, wx.ALL, 5)
        button_layout.Add(self.cancel_button, 0, wx.ALL, 5)


        main_layout.Add(username_layout, 0, wx.ALL | wx.EXPAND, 5)
        main_layout.Add(ip_port_layout, 0, wx.ALL, 5)
        main_layout.Add(button_layout, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(main_layout)

    def GetValues(self):
        return (self.input_user.GetValue(), self.input_ip.GetValue(), self.input_port.GetValue())

class Test(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="ChtCnt")
        self.client = Client(self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.panel = ChatPanel(self)

        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        connect = file_menu.Append(wx.ID_ANY, "Connect", "Connect to server")

        menu_bar.Append(file_menu, "File")

        self.Bind(wx.EVT_MENU, self.connect, connect)
        
        self.SetMenuBar(menu_bar)
        self.Show()

    def connect(self, event):
        with IPinput(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                username, ip, port = dlg.GetValues()
                self.client.connect(ip, int(port), username)

    def SendMessage(self, data):
        self.client.send_message(data)
    
    def UpdateConnected(self, data):
        self.panel.display_connected(data)

    def DisplayMessage(self, message):
        self.panel.display_message(message)

    def OnClose(self, event):
        self.client.cleanup()
        self.Destroy()

if __name__ == "__main__":
    app = wx.App()
    frame = Test()
    app.MainLoop()
