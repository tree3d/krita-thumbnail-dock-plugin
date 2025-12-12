from krita import Krita, DockWidget, DockWidgetFactory, DockWidgetFactoryBase
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QFileDialog, QStyle 
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QByteArray, QSettings
import os, zipfile


class ThumbnailGalleryDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thumbnail Gallery")

        # Persistent settings
        self.settings = QSettings("thumbnail_docker", "ThumbnailGallery")

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        # 📁 Select Folder button (icon + tooltip)
        self.select_button = QPushButton("Select Folder")
        icon = QIcon.fromTheme("folder-open")
        if icon.isNull():
            icon = self.style().standardIcon(QStyle.SP_DirOpenIcon)
        self.select_button.setIcon(icon)
        self.select_button.setToolTip("Select folder containing .kra files")
        self.select_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_button)

        # 🖼 Thumbnail list
        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setIconSize(QPixmap(128, 128).size())
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.layout.addWidget(self.list_widget)

        self.setWidget(self.widget)

        # Restore last folder or fallback
        self.folder_path = self.load_settings()
        self.load_kra_files(self.folder_path)

        self.list_widget.itemClicked.connect(self.thumbnail_clicked)

    # 🔐 Settings
    def load_settings(self):
        folder = self.settings.value("last_folder", "", type=str)
        if folder and os.path.isdir(folder):
            return folder
        return os.path.expanduser("~/Pictures")

    def save_settings(self):
        self.settings.setValue("last_folder", self.folder_path)

    # 📁 Folder picker
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self.widget,
            "Select Folder with .kra Files",
            self.folder_path
        )
        if folder:
            self.folder_path = folder
            self.save_settings()
            self.load_kra_files(folder)

    # 📂 Load .kra files sorted by creation date
    def load_kra_files(self, folder):
        if not os.path.isdir(folder):
            return

        self.list_widget.clear()
        kra_files = []

        for file in os.listdir(folder):
            if file.lower().endswith(".kra"):
                full_path = os.path.join(folder, file)
                try:
                    ctime = os.path.getctime(full_path)
                except Exception:
                    ctime = 0
                kra_files.append((ctime, full_path, file))

        # Newest first
        kra_files.sort(key=lambda x: x[0], reverse=True)

        for _, full_path, file in kra_files:
            item = QListWidgetItem()

            pix = self.load_kra_thumbnail(full_path)
            if pix and not pix.isNull():
                icon = QIcon(pix)
            else:
                icon = QIcon.fromTheme("krita")

            item.setIcon(icon)
            item.setText(file)
            item.setData(256, full_path)

            self.list_widget.addItem(item)

    # 🖼 Extract preview.png from .kra
    def load_kra_thumbnail(self, kra_path):
        try:
            with zipfile.ZipFile(kra_path, "r") as z:
                if "preview.png" in z.namelist():
                    data = z.read("preview.png")
                    pix = QPixmap()
                    pix.loadFromData(QByteArray(data))
                    return pix.scaled(128, 128)
        except Exception as e:
            print("Thumbnail error:", e)
        return None

    # 📂 Open in same Krita window
    def thumbnail_clicked(self, item):
        file_path = item.data(256)
        if not file_path or not os.path.exists(file_path):
            return

        doc = Krita.instance().openDocument(file_path)
        if not doc:
            return

        win = Krita.instance().activeWindow()
        if win:
            win.addView(doc)

    # Required by Krita
    def canvasChanged(self, canvas):
        pass

# keep same factory ID so the plugin stays recognized
factory = DockWidgetFactory(
    "thumbnail_gallery_docker",
    DockWidgetFactoryBase.DockRight,
    ThumbnailGalleryDocker
)

Krita.instance().addDockWidgetFactory(factory)