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
    def __init__(self, parent=None, scene=None, item=None, **kwargs):
        super(Add, self).__init__(parent)
        self.scene = scene
        self.item = item
        if 'symbol' in kwargs:
            self.symbol = kwargs['symbol']
            if 'origin' in kwargs:
                self.origin = kwargs['origin']
            else:
                self.origin = QtCore.QPointF(0, 0)
        else:
            self.symbol = False

    def redo(self):
        if self.symbol is False:
            """If item is a regular item"""
            self.scene.addItem(self.item)
        else:
            """Or if item is a symbol to be loaded"""
            self.item.__init__(None, self.scene, self.origin, self.item.listOfItems)
            self.item.loadItems('symbol')
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


class Move(QtGui.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None, startPoint=None, stopPoint=None):
        super(Move, self).__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems
        self.startPoint = startPoint
        self.stopPoint = stopPoint

    def redo(self):
        for item in self.listOfItems:
            item.moveTo(self.stopPoint, 'done')

    def undo(self):
        for item in self.listOfItems:
            item.moveTo(self.startPoint, 'done')


class Copy(QtGui.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None, point=None):
        super(Copy, self).__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems
        self.point = point

    def redo(self):
        for item in self.listOfItems:
            if item not in self.scene.items():
                self.scene.addItem(item)
            else:
                item.moveTo(self.point, 'done')

    def undo(self):
        for item in self.listOfItems:
            self.scene.removeItem(item)


class Rotate(QtGui.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None, moving=False, point=None, angle=None):
        super(Rotate, self).__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems
        self.moving = moving
        self.point = point
        self.angle = angle
        self.listOfPoints = {}
        for item in self.listOfItems:
            self.listOfPoints[str(item)] = item.mapFromScene(self.point)

    def redo(self):
        for item in self.listOfItems:
            item.rotateBy(self.moving, self.listOfPoints[str(item)], self.angle)

    def undo(self):
        for item in self.listOfItems:
            item.rotateBy(self.moving, self.listOfPoints[str(item)], -self.angle)


class Mirror(QtGui.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None, moving=False, point=None):
        super(Mirror, self).__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems
        self.moving = moving
        self.point = point
        self.listOfPoints = {}
        for item in self.listOfItems:
            self.listOfPoints[str(item)] = item.mapFromScene(self.point)

    def redo(self):
        for item in self.listOfItems:
            item.reflect(self.moving, self.listOfPoints[str(item)])

    def undo(self):
        for item in self.listOfItems:
            item.reflect(self.moving, self.listOfPoints[str(item)])


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