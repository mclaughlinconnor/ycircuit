from PyQt4 import QtCore, QtGui
from components import myGraphicsItemGroup


class Delete(QtGui.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None):
        super(Delete, self).__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems
        for item in self.listOfItems:
            item.changeColourToGray(False)

    def redo(self):
        for item in self.listOfItems:
            self.scene.removeItem(item)

    def undo(self):
        for item in self.listOfItems:
            self.scene.addItem(item)


class AddMulti(QtGui.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None):
        super(AddMulti, self).__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems

    def redo(self):
        for item in self.listOfItems:
            self.scene.addItem(item)

    def undo(self):
        for item in self.listOfItems:
            self.scene.removeItem(item)


class Add(QtGui.QUndoCommand):
    def __init__(self, parent=None, scene=None, item=None):
        super(Add, self).__init__(parent)
        self.scene = scene
        self.item = item

    def redo(self):
        self.scene.addItem(self.item)
        self.scene.update(self.scene.sceneRect())

    def undo(self):
        self.scene.removeItem(self.item)


class Edit(QtGui.QUndoCommand):
    def __init__(self, parent=None, scene=None, item=None, point=None):
        super(Edit, self).__init__(parent)
        self.scene = scene
        self.item = item
        self.point = point

    def redo(self):
        self.item.redoEdit(self.point)

    def undo(self):
        self.item.undoEdit()


class ChangePen(QtGui.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super(ChangePen, self).__init__(parent)
        if 'width' in kwargs:
            self.newLocalPenWidth = kwargs['width']
            if isinstance(item, list):
                self.listOfItems = item
                for i in self.listOfItems:
                    if isinstance(i, myGraphicsItemGroup):
                        changePen = ChangePen(self, i.listOfItems, **kwargs)
                    else:
                        changePen = ChangePenWidth(self, i, **kwargs)
        if 'penColour' in kwargs:
            self.newLocalPenColour = kwargs['penColour']
            if isinstance(item, list):
                self.listOfItems = item
                for i in self.listOfItems:
                    if isinstance(i, myGraphicsItemGroup):
                        changePen = ChangePen(self, i.listOfItems, **kwargs)
                    else:
                        changePen = ChangePenColour(self, i, **kwargs)
        if 'penStyle' in kwargs:
            self.newLocalPenStyle = kwargs['penStyle']
            if isinstance(item, list):
                self.listOfItems = item
                for i in self.listOfItems:
                    if isinstance(i, myGraphicsItemGroup):
                        changePen = ChangePen(self, i.listOfItems, **kwargs)
                    else:
                        changePen = ChangePenStyle(self, i, **kwargs)


class ChangePenWidth(QtGui.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super(ChangePenWidth, self).__init__(parent)
        self.item = item
        self.oldLocalPenWidth = self.item.localPenWidth
        if 'width' in kwargs:
            self.newLocalPenWidth = kwargs['width']

    def redo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(width=self.newLocalPenWidth)

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(width=self.oldLocalPenWidth)


class ChangePenColour(QtGui.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super(ChangePenColour, self).__init__(parent)
        self.item = item
        self.oldLocalPenColour = self.item.localPenColour
        if 'penColour' in kwargs:
            self.newLocalPenColour = kwargs['penColour']

    def redo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penColour=self.newLocalPenColour)

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penColour=self.oldLocalPenColour)


class ChangePenStyle(QtGui.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super(ChangePenStyle, self).__init__(parent)
        self.item = item
        self.oldLocalPenStyle = self.item.localPenStyle
        if 'penStyle' in kwargs:
            self.newLocalPenStyle = kwargs['penStyle']

    def redo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penStyle=self.newLocalPenStyle)

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penStyle=self.oldLocalPenStyle)


class ChangeBrush(QtGui.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super(ChangeBrush, self).__init__(parent)
        if 'brushColour' in kwargs:
            self.newLocalBrushColour = kwargs['brushColour']
            if isinstance(item, list):
                self.listOfItems = item
                for i in self.listOfItems:
                    if isinstance(i, myGraphicsItemGroup):
                        changeBrush = ChangeBrush(self, i.listOfItems, **kwargs)
                    else:
                        changeBrush = ChangeBrushColour(self, i, **kwargs)
        if 'brushStyle' in kwargs:
            self.newLocalBrushStyle = kwargs['brushStyle']
            if isinstance(item, list):
                self.listOfItems = item
                for i in self.listOfItems:
                    if isinstance(i, myGraphicsItemGroup):
                        changeBrush = ChangeBrush(self, i.listOfItems, **kwargs)
                    else:
                        changeBrush = ChangeBrushStyle(self, i, **kwargs)


class ChangeBrushColour(QtGui.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super(ChangeBrushColour, self).__init__(parent)
        self.item = item
        self.oldLocalBrushColour = self.item.localBrushColour
        if 'brushColour' in kwargs:
            self.newLocalBrushColour = kwargs['brushColour']

    def redo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalBrushOptions(brushColour=self.newLocalBrushColour)

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalBrushOptions(brushColour=self.oldLocalBrushColour)


class ChangeBrushStyle(QtGui.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super(ChangeBrushStyle, self).__init__(parent)
        self.item = item
        self.oldLocalBrushStyle = self.item.localBrushStyle
        if 'brushStyle' in kwargs:
            self.newLocalBrushStyle = kwargs['brushStyle']

    def redo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalBrushOptions(brushStyle=self.newLocalBrushStyle)

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalBrushOptions(brushStyle=self.oldLocalBrushStyle)
