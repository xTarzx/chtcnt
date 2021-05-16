import wx
from wx.lib import intctrl
from client import Client
from stuff import Message, IDCODES
import iconfile
import darkMode

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
        self.chat_input.SetMaxLength(350)
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

    def clear_all(self):
        self.chat_messages.Clear()
        self.connected_list.Clear()

class IPinputValidator(wx.Validator):
    def Clone(self):
        return IPinputValidator()
    
    def Validate(self, win):
        username = win.input_user.GetValue()
        ip = win.input_ip.GetValue()
        port = win.input_port.GetValue()

        if len(username) == 0 or len(ip) == 0:
            wx.MessageBox("All fields must be filled in!", "Error")
            return False
        if port < 1:
            wx.MessageBox("Tf you tryna get in?", "Error")
            return False
        return True
    
    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

class IPinput(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title = 'Connect', size = (300,200))
        self.parent = parent

        main_layout = wx.BoxSizer(wx.VERTICAL)
        
        ### USERNAME
        self.input_user = wx.TextCtrl(self)
        username_layout = wx.BoxSizer(wx.HORIZONTAL)
        username_label = wx.StaticText(self, label = 'Username:')
        username_layout.Add(username_label, 0, wx.ALL, 5)
        username_layout.Add(self.input_user, 1, wx.ALL, 5)

        self.input_user.SetValidator(IPinputValidator())

        ### IP PORT
        ip_port_layout = wx.BoxSizer(wx.HORIZONTAL)
        ip_label = wx.StaticText(self, label = 'Server IP')
        self.input_ip = wx.TextCtrl(self)
        colon_label = wx.StaticText(self, label = ':')
        self.input_port = intctrl.IntCtrl(self, style=wx.TE_CENTER , size = (125, -1))
        self.input_port.SetBounds(0, 65535)
        self.input_port.SetMaxLength(5)

        self.input_ip.SetValidator(IPinputValidator())


        ip_port_layout.Add(ip_label, 0, wx.ALL, 5)
        ip_port_layout.Add(self.input_ip, 0, wx.ALL | wx.EXPAND, 5)
        ip_port_layout.Add(colon_label, 0, wx.ALL, 5)
        ip_port_layout.Add(self.input_port, 0, wx.ALL, 5)

        ### BUTTONS

        button_layout = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_button = wx.Button(self, wx.ID_OK, label = 'OK')
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, label = 'Cancel')

        button_layout.Add(self.ok_button, 0, wx.ALL, 5)
        button_layout.Add(self.cancel_button, 0, wx.ALL, 5)


        main_layout.Add(username_layout, 0, wx.ALL | wx.EXPAND, 5)
        main_layout.Add(ip_port_layout, 0, wx.ALL, 5)
        main_layout.Add(button_layout, 0, wx.ALL | wx.CENTER, 5)

        self.setColours()
        self.SetSizer(main_layout)

    def setColours(self):
        widgets = darkMode.getWidgets(self)
        for widget in widgets:
            widget.SetBackgroundColour(self.parent.GetBackgroundColour())
            widget.SetForegroundColour(self.parent.GetForegroundColour())

    def GetValues(self):
        return (self.input_user.GetValue(), self.input_ip.GetValue(), self.input_port.GetValue())

class Main(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="ChtCnt")
        self.SetIcon(iconfile.icon.getIcon())
        self.client = Client(self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.panel = ChatPanel(self)

        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        self.menu_connect = file_menu.Append(wx.ID_ANY, "Connect", "Connect to server")
        self.menu_disconnect = file_menu.Append(wx.ID_ANY, "Disconnect", "Disconnect from server")
        self.dark_mode = file_menu.AppendCheckItem(wx.ID_ANY, "Dark Mode", "Toggle Dark Mode")

        self.menu_disconnect.Enable(False)

        menu_bar.Append(file_menu, "File")

        self.Bind(wx.EVT_MENU, self.connect, self.menu_connect)
        self.Bind(wx.EVT_MENU, self.disconnect, self.menu_disconnect)
        self.Bind(wx.EVT_MENU, self.OnToggleDarkMode, self.dark_mode)

        self.SetMenuBar(menu_bar)
        self.Show()

    def connect(self, event):
        connected = False
        with IPinput(self) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                username, self.ip, port = dlg.GetValues()
                connected = self.client.connect(self.ip, int(port), username)
        if connected:
            self.panel.clear_all()
            self.menu_connect.Enable(False)
            self.menu_disconnect.Enable(True)

    def disconnect(self, event):
        self.client.cleanup()
        self.OnDisconnect()

    def OnDisconnect(self):
        self.menu_connect.Enable(True)
        self.menu_disconnect.Enable(False)
        self.DisplayMessage(Message(IDCODES.SYSTEM, f"Disconnected from {self.ip}", "System"))

    def SendMessage(self, data):
        self.client.send_message(data)
    
    def UpdateConnected(self, data):
        self.panel.display_connected(data)

    def DisplayMessage(self, message):
        self.panel.display_message(message)

    def OnClose(self, event):
        self.client.cleanup()
        self.Destroy()

    def OnToggleDarkMode(self, event):
        if self.dark_mode.IsChecked():
            darkMode.darkMode(self, True)
            self.Refresh()
        else:
            darkMode.darkMode(self, False)
            self.Refresh()

if __name__ == "__main__":
    app = wx.App()
    frame = Main()
    app.MainLoop()
