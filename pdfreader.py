import wx, fitz, os

class PDFViewer(wx.Frame):
    def __init__(self, parent, title):
        super(PDFViewer, self).__init__(parent, title=title, size=(800, 600))
        
        self.panel = wx.Panel(self)
        self.splitter = wx.SplitterWindow(self.panel)
        
        self.file_list = wx.ListBox(self.splitter, style=wx.LB_SINGLE)
        self.pdf_view = wx.Panel(self.splitter)

        self.splitter.SplitVertically(self.file_list, self.pdf_view)
        
        self.Bind(wx.EVT_LISTBOX, self.on_file_selected, self.file_list)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.splitter, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
        
        self.load_files()
        
    def load_files(self):
        dlg = wx.DirDialog(self, "Chose folder", style=wx.DD_DEFAULT_STYLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.folder_path = dlg.GetPath()  
            files = os.listdir(self.folder_path)
            pdf_files = [file for file in files if file.lower().endswith('.pdf')]
            
            self.file_list.Set(pdf_files)
        
        dlg.Destroy()
    
    def on_file_selected(self, event):
        selected_file = self.file_list.GetStringSelection()
        file_path = os.path.join(self.folder_path, selected_file)
        
        doc = fitz.open(file_path)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        
        image = wx.Image(pix.width, pix.height, pix.samples)
        image.SetData(pix.samples)
        
        bitmap = image.ConvertToBitmap()
        self.pdf_view.bitmap = wx.StaticBitmap(self.pdf_view, -1, bitmap)
        self.pdf_view.Layout()

app = wx.App()
frame = PDFViewer(None, "PDF Viewer")
frame.Show()
app.MainLoop()
