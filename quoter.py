import ystockquote

#!/usr/bin/env python

import wx
import wx.grid

class wxHelloFrame(wx.Frame):
    """This is the frame for our application, it is derived from
    the wx.Frame element."""

    def __init__(self, *args, **kwargs):
        """Initialize, and let the user set any Frame settings"""
        wx.Frame.__init__(self, *args, **kwargs)
        self.quotes = []
        self.create_controls()

    def create_controls(self):
        """Called when the controls on Window are to be created"""
        # Horizontal sizer
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create the static text widget and set the text
        self.text = wx.StaticText(self, label="Enter quote")
        #Add to horizontal sizer
        #add the static text to the sizer, tell it not to resize
        self.h_sizer.Add(self.text)

        #Add 5 pixels between the static text and the edit
        #Create the Edit Field (or TextCtrl)
        self.edit = wx.TextCtrl(self, size=wx.Size(250, -1), style=wx.TE_PROCESS_ENTER)
        self.h_sizer.AddSpacer((5,0))
        self.h_sizer.Add(self.edit)
        self.edit.Bind(wx.EVT_KEY_DOWN, self.on_key_pressed)

        #Create the button
        self.button = wx.Button(self, label="Add")
        #bind the button click to our press function
        self.button.Bind(wx.EVT_BUTTON, self.on_button_pressed)

        self.h_sizer.AddSpacer((5,0))
        self.h_sizer.Add(self.button)

        self.grid = wx.grid.Grid(self);
        self.grid.CreateGrid(10, 16)
        self.grid.IsEditable = False
        self.grid.DisableCellEditControl()

        self.v_sizer.Add(self.h_sizer)
        self.v_sizer.Add(self.grid, 1, wx.EXPAND | wx.ALIGN_TOP)

        self.SetSizer(self.v_sizer)
        #self.SetAutoLayout(1)
        self.v_sizer.Fit(self)

    def on_key_pressed(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            self.get_quote()
        evt.Skip()

    def on_button_pressed(self, event):
        """Called when the button is clicked."""
        self.get_quote()


    def get_quote(self):

        quote_name = self.edit.GetValue()
        answer = ystockquote.get(quote_name)

        if answer["stock_exchange"] == '"N/A"':
            wx.MessageBox('Quote name seems incorrect', 'Info',
                wx.OK | wx.ICON_INFORMATION)
            self.edit.SetSelection(-1, -1)
            self.edit.SetFocus()
            return

        column = 1
        self.grid.SetColLabelValue(0, "Name")
        self.grid.SetCellValue(len(self.quotes), 0, quote_name)
        for key, value in answer.items():

            if not self.quotes:
                self.grid.SetColSize(column, len(str(key))*9)
                self.grid.SetColLabelValue(column, str(key))

            self.grid.SetCellValue(len(self.quotes), column, str(value))
            column = column + 1

        self.quotes.append(quote_name)

class wxHelloApp(wx.App):
    """The wx.App for the wxHello application"""

    def OnInit(self):
        """Override OnInit to create our Frame"""
        frame = wxHelloFrame(None, title="Quoter")
        frame.Show()
        self.SetTopWindow(frame)

        return True

if __name__ == "__main__":
    app = wxHelloApp()
    app.MainLoop()


