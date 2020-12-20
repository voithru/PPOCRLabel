import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class EditInList(QListWidget):
    def __init__(self):
        super(EditInList,self).__init__()
        # click to edit
        self.clicked.connect(self.item_clicked)

    def mouseDoubleClickEvent(self, event):
        # close edit
        self.closePersistentEditor(self.currentItem())

    def leaveEvent(self, event):
        # close edit  
        self.closePersistentEditor(self.currentItem())    
        
    def item_clicked(self, modelindex: QModelIndex) -> None:
        self.edited_item = self.currentItem()
        self.closePersistentEditor(self.edited_item)
        item = self.item(modelindex.row())
        self.edited_item = item
        self.openPersistentEditor(item)
        self.editItem(item)