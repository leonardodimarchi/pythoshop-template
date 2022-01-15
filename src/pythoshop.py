import os
import photoshop.api as ps
from pathvalidate import sanitize_filename

class Pythoshop:
    photoshop_app = None
    psd_file = None

    def __init__(self):
        self.photoshop_app = ps.Application()
        self.photoshop_app.displayDialogs = ps.DialogModes.DisplayNoDialogs
        self.photoshop_app.Visible = False

    def closePhotoshop(self):
        while self.photoshop_app.documents.length > 0:
            self.photoshop_app.activeDocument.Close(ps.SaveOptions.DoNotSaveChanges)

        self.photoshop_app.Quit()

    def openPSDFile(self, filename):
        if not self.psd_file is None:
            raise Exception("PSD file already opened")

        if os.path.isfile(filename) == False:
            self.closePhotoshop()
            raise Exception("The specified PSD file was not found")

        self.photoshop_app.load(filename)
        self.psd_file = self.photoshop_app.activeDocument;
        return True

    def closePSDFile(self):
        if self.psd_file is None:
            raise Exception(FileNotFoundError)

        self.photoshop_app.activeDocument.Close(ps.SaveOptions.DoNotSaveChanges)
        
    def updateTitleLayer(self, layer_name, new_text):
        if self.psd_file is None:
            raise Exception(FileNotFoundError)

        layer = self.psd_file.artLayers[layer_name]
        layer_text_item = layer.textItem
        layer_text_item.contents = new_text
        return True

    def exportJPEG(self, filename, folder='', quality=10):
        if self.psd_file is None:
            raise Exception(FileNotFoundError)

        filename = sanitize_filename(filename)
        full_path = os.path.join(folder, filename)

        options = ps.JPEGSaveOptions(quality)

        # Export and close without saving
        self.psd_file.saveAs(full_path, options)

        return os.path.isfile(full_path)
