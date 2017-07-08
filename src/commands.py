from PyQt5 import QtCore, QtWidgets
from .components import myGraphicsItemGroup
import copy


class Delete(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None):
        super().__init__(parent)
        self.scene = scene
        if type(listOfItems) != list:
            self.listOfItems = [listOfItems]
        else:
            self.listOfItems = listOfItems
        for item in self.listOfItems:
            item.changeColourToGray(False)

    def redo(self):
        for item in self.listOfItems:
            self.scene.removeItem(item)

    def undo(self):
        for item in self.listOfItems:
            self.scene.addItem(item)


class AddMulti(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None):
        super().__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems

    def redo(self):
        for item in self.listOfItems:
            self.scene.addItem(item)

    def undo(self):
        for item in self.listOfItems:
            self.scene.removeItem(item)


class Add(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, scene=None, item=None, **kwargs):
        super().__init__(parent)
        self.scene = scene
        if 'symbol' in kwargs:
            self.symbol = kwargs['symbol']
            if 'origin' in kwargs:
                self.origin = kwargs['origin']
            else:
                self.origin = QtCore.QPointF(0, 0)
            if 'rotateAngle' in kwargs:
                self.rotateAngle = kwargs['rotateAngle']
            else:
                self.rotateAngle = 0
            if 'reflect' in kwargs:
                self.reflect = kwargs['reflect']
            else:
                self.reflect = 0
            if 'transform' in kwargs:
                self.transform_ = kwargs['transform']
        else:
            self.symbol = False
        if self.symbol is True:
            self.item = copy.deepcopy(item)
        else:
            self.item = item

    def redo(self):
        if self.symbol is False:
            """If item is a regular item"""
            self.scene.addItem(self.item)
        else:
            """Or if item is a symbol to be loaded"""
            self.item.__init__(None, self.origin, self.item.listOfItems, mode='symbol')
            self.scene.addItem(self.item)
            # self.item.loadItems('symbol')
            # if hasattr(self, 'reflect'):
            #     if self.reflect == 1:
            #         self.item.reflect(moving=False, origin=self.origin)
            # if hasattr(self, 'rotateAngle'):
            #     self.item.rotateBy(moving=False, origin=self.origin, angle=self.rotateAngle)
            if hasattr(self, 'transform_'):
                self.item.setTransform(self.transform_)
        self.scene.update(self.scene.sceneRect())

    def undo(self):
        self.scene.removeItem(self.item)


class Draw(QtWidgets.QUndoCommand):
    """Mainly used only for wires and arcs"""
    def __init__(self, parent=None, scene=None, item=None, point=None):
        super().__init__(parent)
        self.scene = scene
        self.item = item
        self.point = point

    def redo(self):
        self.item.redoDraw(self.point)

    def undo(self):
        self.item.undoDraw()


class Edit(QtWidgets.QUndoCommand):
    """Used for editing item shapes"""
    def __init__(self, parent=None, scene=None, item=None, point=None, **kwargs):
        super().__init__(parent)
        self.scene = scene
        self.item = item
        self.point = point
        if 'clicked' in kwargs:
            self.clicked = True
        else:
            self.clicked = False

    def redo(self):
        self.item.redoEdit(self.point, clicked=self.clicked)

    def undo(self):
        self.item.undoEdit()


class EditNet(QtWidgets.QUndoCommand):
    """Used for editing net lengths"""
    def __init__(self, parent=None, scene=None, item=None, oldLine=None, newLine=None):
       super().__init__(parent)
       self.scene = scene
       self.item = item
       self.oldLine = oldLine
       self.newLine = newLine

    def redo(self):
        self.item.setLine(self.newLine)

    def undo(self):
        self.item.setLine(self.oldLine)


class Move(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None, startPoint=None, stopPoint=None):
        super().__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems
        self.startPoint = startPoint
        self.stopPoint = stopPoint

    def redo(self):
        for item in self.listOfItems:
            item.moveTo(self.startPoint, 'start')
            item.moveTo(self.stopPoint, 'done')

    def undo(self):
        for item in self.listOfItems:
            item.moveTo(self.stopPoint, 'start')
            item.moveTo(self.startPoint, 'done')


class Copy(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None, point=None):
        super().__init__(parent)
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


class Rotate(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None, moving=False, point=None, angle=None):
        super().__init__(parent)
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


class Mirror(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None, moving=False, point=None):
        super().__init__(parent)
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


class ChangePen(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super().__init__(parent)
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


class ChangePenWidth(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super().__init__(parent)
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


class ChangePenColour(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super().__init__(parent)
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


class ChangePenStyle(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super().__init__(parent)
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


class ChangeBrush(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super().__init__(parent)
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


class ChangeBrushColour(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super().__init__(parent)
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


class ChangeBrushStyle(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super().__init__(parent)
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
