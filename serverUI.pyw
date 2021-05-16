import wx
from datetime import datetime
from wx.core import MenuBar
from wx.lib import intctrl
from server import Server
import iconfile, darkMode

class ServerPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        main_layout = wx.BoxSizer(wx.VERTICAL)


        ### Server Control
        control_layout = wx.BoxSizer(wx.HORIZONTAL)
        
        input_port_label = wx.StaticText(self, label="Port:")

        self.input_port = intctrl.IntCtrl(self, style=wx.TE_CENTER, size = (50, -1))
        self.input_port.SetBounds(0, 65535)
        self.input_port.SetMaxLength(5)

        self.control_button = wx.Button(self, label="Start")
        self.control_button.Bind(wx.EVT_BUTTON, self.server_control)

        control_layout.Add(input_port_label, 0, wx.ALL, 5)
        control_layout.Add(self.input_port, 0, wx.ALL, 5)
        control_layout.Add(self.control_button, 0, wx.ALL, 5)


        server_log_label = wx.StaticText(self, label="Logs:")
        self.server_log = wx.TextCtrl(self, style=wx.TE_MULTILINE)


        main_layout.Add(control_layout, 0, wx.ALL | wx.CENTER, 5)
        main_layout.Add(server_log_label, 0, wx.ALL, 5)
        main_layout.Add(self.server_log, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(main_layout)
    
    def display_log(self, message):
        self.server_log.AppendText(f"{message}\n")

    def server_control(self, event):
        if self.control_button.GetLabelText() == "Start":
            self.parent.ServerStart(self.input_port.GetValue())
        elif self.control_button.GetLabelText() == "Stop":
            self.parent.ServerStop()
class Main(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="ChtCnt Server")
        self.SetIcon(iconfile.icon.getIcon())
        self.server = Server(self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.panel = ServerPanel(self)

        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        self.dark_mode = file_menu.AppendCheckItem(wx.ID_ANY, "Dark Mode", "Toggle Dark Mode")

        menu_bar.Append(file_menu, "File")

        self.Bind(wx.EVT_MENU, self.OnToggleDarkMode, self.dark_mode)

        self.SetMenuBar(menu_bar)
        self.Show()

    def DisplayLog(self, message):
        self.panel.display_log("{} - {}".format(datetime.now().strftime("%H:%M:%S"), message))

    def ServerStart(self, port):
        self.DisplayLog("Server Start")
        self.server.start_server(port)
        self.panel.control_button.SetLabel("Stop")
    
    def ServerStop(self):
        self.DisplayLog("Server Stop")
        self.server.stop_server()
        self.panel.control_button.SetLabel("Start")
    
    def OnClose(self, event):
        self.server.stop_server()
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