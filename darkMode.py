import wx

def getWidgets(parent):
    items = [parent]
    for item in parent.GetChildren():
        items.append(item)
        if hasattr(item, "GetChildren"):
            for child in item.GetChildren():
                items.append(child)
    return items


def darkMode(parent, setDark):
    widgets = getWidgets(parent)
    panel = widgets[1]
    if setDark:
        for widget in widgets:
            widget.SetBackgroundColour("Dark Grey")
            widget.SetForegroundColour("White")
    else:
        for widget in widgets:
            widget.SetBackgroundColour(wx.NullColour)
            widget.SetForegroundColour(wx.NullColour)