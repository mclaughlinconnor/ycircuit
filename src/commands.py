from PyQt5 import QtCore, QtWidgets, QtGui
from .components import myGraphicsItemGroup, TextBox
import copy
import logging

logger = logging.getLogger('YCircuit.commands')


class Delete(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None):
        super().__init__(parent)
        self.scene = scene
        if type(listOfItems) != list:
            self.listOfItems = [listOfItems]
        else:
            self.listOfItems = listOfItems
        self.dictOfParentItems = {}
        for item in self.listOfItems:
            item.lightenColour(False)
            # Need to remember where exactly the item was deleted in case
            # its parent is moved in the future
            item.deletePos = item.pos()
            self.dictOfParentItems[item] = item.parentItem()

    def redo(self):
        logger.info('Deleting items: %s', self.listOfItems)
        for item in self.listOfItems:
            self.scene.removeItem(item)

    def undo(self):
        logger.info('Undoing delete of items: %s', self.listOfItems)
        for item in self.listOfItems:
            self.scene.addItem(item)
            item.setParentItem(self.dictOfParentItems[item])
            if isinstance(self.dictOfParentItems[item], myGraphicsItemGroup):
                childItems = self.dictOfParentItems[item].childItems()
                childItems.append(item)
                self.dictOfParentItems[item].setItems(childItems)
            item.setPos(item.deletePos)


class AddMulti(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, scene=None, listOfItems=None, parentItem=None):
        super().__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems
        self.parentItem = parentItem

    def redo(self):
        for item in self.listOfItems:
            self.scene.addItem(item)
            item.setParentItem(self.parentItem)

    def undo(self):
        for item in self.listOfItems:
            self.scene.removeItem(item)


class Add(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, scene=None, item=None, parentItem=None, **kwargs):
        super().__init__(parent)
        self.scene = scene
        self.parentItem = parentItem
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
            # pinVisibility is actually a reference to the UI object in the
            # window that holds the value for pin visibility
            if 'pinVisibility' in kwargs:
                self.pinVisibility = kwargs['pinVisibility']
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
            self.item.setParentItem(self.parentItem)
            if isinstance(self.parentItem, myGraphicsItemGroup):
                childItems = self.parentItem.childItems()
                childItems.append(self.item)
                self.parentItem.setItems(childItems)
            logger.info('Adding item %s as a regular item', self.item)
        else:
            """Or if item is a symbol to be loaded"""
            self.item.__init__(self.parentItem, self.origin, self.item.listOfItems, mode='symbol')
            if self.parentItem is None:
                self.scene.addItem(self.item)
            # self.item.loadItems('symbol')
            # if hasattr(self, 'reflect'):
            #     if self.reflect == 1:
            #         self.item.reflect(moving=False, origin=self.origin)
            # if hasattr(self, 'rotateAngle'):
            #     self.item.rotateBy(moving=False, origin=self.origin, angle=self.rotateAngle)
            if hasattr(self, 'transform_'):
                self.item.setTransform(self.transform_)
            if hasattr(self, 'pinVisibility'):
                self.item.pinVisibility(self.pinVisibility.isChecked())
            logger.info('Adding item %s as a symbol', self.item)
        self.scene.update(self.scene.sceneRect())

    def undo(self):
        logger.info('Undoing addition of item %s', self.item)
        self.scene.removeItem(self.item)


class Draw(QtWidgets.QUndoCommand):
    """Mainly used only for wires and arcs"""

    def __init__(self, parent=None, scene=None, item=None, point=None):
        super().__init__(parent)
        self.scene = scene
        self.item = item
        self.point = point

    def redo(self):
        logger.info('Drawing the next vertex of %s at %s', self.item, self.point)
        self.item.redoDraw(self.point)

    def undo(self):
        logger.info('Undoing vertex drawn at %s for %s', self.point, self.item)
        self.item.undoDraw()


class Edit(QtWidgets.QUndoCommand):
    """Used for editing item shapes"""
    def __init__(self,
                 parent=None,
                 scene=None,
                 item=None,
                 point=None,
                 **kwargs):
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
        if self.clicked is True:
            logger.info('Editing vertex of %s to be at %s', self.item, self.point)

    def undo(self):
        self.item.undoEdit()
        if self.clicked is True:
            logger.info('Undoing edit of %s\'s vertex at %s', self.item, self.point)


class EditNet(QtWidgets.QUndoCommand):
    """Used for editing net lengths"""
    def __init__(self,
                 parent=None,
                 scene=None,
                 item=None,
                 oldLine=None,
                 newLine=None):
        super().__init__(parent)
        self.scene = scene
        self.item = item
        self.oldLine = oldLine
        self.newLine = newLine

    def redo(self):
        self.item.setLine(self.newLine)
        logger.info('Changed line for %s from %s to %s', self.item, self.oldLine, self.newLine)

    def undo(self):
        self.item.setLine(self.oldLine)
        logger.info('Changed line for %s from %s to %s', self.item, self.newLine, self.oldLine)


class Move(QtWidgets.QUndoCommand):
    def __init__(self,
                 parent=None,
                 scene=None,
                 listOfItems=None,
                 startPoint=None,
                 stopPoint=None):
        super().__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems
        self.startPoint = startPoint
        self.stopPoint = stopPoint

    def redo(self):
        logger.info(
            'Moving items %s from %s to %s',
            self.listOfItems,
            self.startPoint,
            self.stopPoint)
        for item in self.listOfItems:
            item.moveTo(self.startPoint, 'start')
            item.moveTo(self.stopPoint, 'done')

    def undo(self):
        logger.info(
            'Undoing move. Moving items %s from %s to %s',
            self.listOfItems,
            self.stopPoint,
            self.startPoint)
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
        logger.info(
            'Copying items %s to %s',
            self.listOfItems,
            self.point)
        for item in self.listOfItems:
            if item not in self.scene.items():
                self.scene.addItem(item)
            else:
                item.moveTo(self.point, 'done')

    def undo(self):
        logger.info('Undoing copy of items %s', self.listOfItems)
        for item in self.listOfItems:
            self.scene.removeItem(item)


class Rotate(QtWidgets.QUndoCommand):
    def __init__(self,
                 parent=None,
                 scene=None,
                 listOfItems=None,
                 moving=False,
                 point=None,
                 angle=None):
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
        logger.info(
            'Rotating items %s by %d around %s',
            self.listOfItems,
            self.angle,
            self.listOfPoints)
        for item in self.listOfItems:
            item.rotateBy(self.moving, self.listOfPoints[str(item)], self.angle)

    def undo(self):
        logger.info('Undoing rotation of %s', self.listOfItems)
        for item in self.listOfItems:
            item.rotateBy(self.moving, self.listOfPoints[str(item)], -self.angle)


class Mirror(QtWidgets.QUndoCommand):
    def __init__(self,
                 parent=None,
                 scene=None,
                 listOfItems=None,
                 moving=False,
                 point=None):
        super().__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems
        self.moving = moving
        self.point = point
        self.listOfPoints = {}
        for item in self.listOfItems:
            self.listOfPoints[str(item)] = item.mapFromScene(self.point)

    def redo(self):
        logger.info(
            'Mirroring items %s around %s',
            self.listOfItems,
            self.listOfPoints)
        for item in self.listOfItems:
            item.reflect(self.moving, self.listOfPoints[str(item)])

    def undo(self):
        logger.info('Undoing mirroring of %s', self.listOfItems)
        for item in self.listOfItems:
            item.reflect(self.moving, self.listOfPoints[str(item)])


class ChangeFont(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, listOfItems=None, **kwargs):
        super().__init__(parent)
        if isinstance(listOfItems, list):
            self.listOfItems = listOfItems
            for item in self.listOfItems:
                changeFont = ChangeFont(
                    self,
                    item,
                    **kwargs)
        else:
            self.item = listOfItems
            self.oldFont = self.item.font()
            if 'font' in kwargs:
                self.newFont = kwargs['font']

    def redo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.changeFont(self.newFont)
            logger.info(
                'Changing font of %s to %s %d',
                self.item,
                self.newFont.family(),
                self.newFont.pointSize())
        else:
            super().redo()

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.changeFont(self.oldFont)
            logger.info(
                'Undoing font change. Changing font of %s to %s %d',
                self.item,
                self.oldFont.family(),
                self.oldFont.pointSize())
        else:
            super().undo()


class ChangeHeight(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, listOfItems=None, **kwargs):
        super().__init__(parent)
        if isinstance(listOfItems, list):
            self.listOfItems = listOfItems
            for item in self.listOfItems:
                changeHeight = ChangeHeight(
                    self,
                    item,
                    **kwargs)
        else:
            self.item = listOfItems
            self.oldHeight = self.item.zValue()
            if 'mode' in kwargs:
                self.mode = kwargs['mode']

    def redo(self):
        if not hasattr(self, 'listOfItems'):
            oldValue = self.item.zValue()
            if self.mode == 'forward':
                self.item.setZValue(self.item.zValue() + 1)
            elif self.mode == 'back':
                self.item.setZValue(self.item.zValue() - 1)
            elif self.mode == 'reset':
                self.item.setZValue(0)
            newValue = self.item.zValue()
            logger.info('Changed height of %s from %d to %d', self.item, oldValue, newValue)
        else:
            super().redo()

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            oldValue = self.item.zValue()
            if self.mode == 'forward':
                self.item.setZValue(self.item.zValue() - 1)
            elif self.mode == 'back':
                self.item.setZValue(self.item.zValue() + 1)
            elif self.mode == 'reset':
                self.item.setZValue(self.oldHeight)
            newValue = self.item.zValue()
            logger.info('Undoing height change. Changed height of %s from %d to %d', self.item, oldValue, newValue)
        else:
            super().undo()


class Group(QtWidgets.QUndoCommand):
    def __init__(
            self,
            parent=None,
            scene=None,
            listOfItems=None,
            **kwargs):
        super().__init__(parent)
        self.scene = scene
        self.listOfItems = listOfItems

        x = min([item.scenePos().x() for item in self.listOfItems])
        y = min([item.scenePos().y() for item in self.listOfItems])
        self.origin = QtCore.QPointF(x, y)
        self.item = myGraphicsItemGroup(None, self.origin, [])

    def redo(self):
        self.scene.addItem(self.item)
        self.item.origin = self.origin
        # Set relative origins of child items
        for item in self.listOfItems:
            item.origin = item.pos() - self.item.origin
        self.item.setItems(self.listOfItems)
        logger.info('Grouping items %s together under %s', self.listOfItems, self.item)

    def undo(self):
        self.item.reparentItems()
        self.scene.removeItem(self.item)
        logger.info('Undoing group. Ungrouping %s from under %s', self.listOfItems, self.item)


class Ungroup(QtWidgets.QUndoCommand):
    def __init__(
            self,
            parent=None,
            scene=None,
            item=None,
            **kwargs):
        super().__init__(parent)
        self.scene = scene
        self.item = item
        self.listOfItems = item.listOfItems

        x = min([item.scenePos().x() for item in self.listOfItems])
        y = min([item.scenePos().y() for item in self.listOfItems])
        self.origin = QtCore.QPointF(x, y)

    def redo(self):
        self.item.reparentItems()
        self.scene.removeItem(self.item)
        logger.info('Destroying group %s containing %s', self.item, self.listOfItems)

    def undo(self):
        self.scene.addItem(self.item)
        self.item.origin = self.origin
        transform_ = self.item.transform()
        # Set relative origins of child items
        for item in self.listOfItems:
            if not hasattr(item, 'reflections'):
                item.reflections = 0
            if hasattr(self.item, 'reflections'):
                item.reflections -= self.item.reflections
                item.reflections %= 2
            else:
                self.item.reflections = 0
            if item.reflections != self.item.reflections:
                item.setTransform(item.transform().scale(-1, 1))
            itemTransform = item.transform()
            item.setTransform(transform_.inverted()[0])
            item.setTransform(itemTransform, combine=True)
            if item.reflections != self.item.reflections:
                item.setTransform(item.transform().scale(-1, 1))
            item.transformData = item.transform()
            # item.origin = transform_.map(item.pos())# - self.item.origin
            item.origin = self.item.mapFromScene(item.scenePos())
        self.item.setItems(self.listOfItems)
        for item in self.listOfItems:
            item.transformData = item.transform()
        logger.info('Undoing destruction of group %s containing items %s', self.item, self.listOfItems)


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
        if 'penJoinStyle' in kwargs:
            self.newLocalPenJoinStyle = kwargs['penJoinStyle']
            if isinstance(item, list):
                self.listOfItems = item
                for i in self.listOfItems:
                    if isinstance(i, myGraphicsItemGroup):
                        changePen = ChangePen(self, i.listOfItems, **kwargs)
                    else:
                        changePen = ChangePenJoinStyle(self, i, **kwargs)
        if 'penCapStyle' in kwargs:
            self.newLocalPenCapStyle = kwargs['penCapStyle']
            if isinstance(item, list):
                self.listOfItems = item
                for i in self.listOfItems:
                    if isinstance(i, myGraphicsItemGroup):
                        changePen = ChangePen(self, i.listOfItems, **kwargs)
                    else:
                        changePen = ChangePenCapStyle(self, i, **kwargs)


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
            logger.info('Changing pen width of %s to %d', self.item, self.newLocalPenWidth)

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(width=self.oldLocalPenWidth)
            logger.info('Undoing pen width change. Changing pen width of %s back to %d', self.item, self.oldLocalPenWidth)


class ChangePenColour(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super().__init__(parent)
        self.item = item
        self.oldLocalPenColour = self.item.localPenColour
        if 'penColour' in kwargs:
            self.newLocalPenColour = kwargs['penColour']

    def redo(self):
        if hasattr(self, 'newLatexImageBinary'):
            self.oldLatexImageBinary, self.item.latexImageBinary = self.item.latexImageBinary, self.newLatexImageBinary
            self.oldLatexImageHtml, self.item.latexImageHtml = self.item.latexImageHtml, self.newLatexImageHtml
            self.oldLatexExpression, self.item.latexExpression = self.item.latexExpression, self.newLatexExpression
            self.item.update()
            return
        if isinstance(self.item, TextBox):
            self.oldLatexImageBinary = self.item.latexImageBinary
            self.oldLatexImageHtml = self.item.latexImageHtml
            self.oldLatexExpression = self.item.latexExpression
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penColour=self.newLocalPenColour)
            logger.info(
                'Changing pen colour of %s to %s',
                self.item,
                QtGui.QColor(self.newLocalPenColour).name())

    def undo(self):
        if isinstance(self.item, TextBox):
            if self.item.latexImageBinary is not None:
                self.item.latexImageBinary, self.newLatexImageBinary = self.oldLatexImageBinary, self.item.latexImageBinary
                self.item.latexImageHtml, self.newLatexImageHtml = self.oldLatexImageHtml, self.item.latexImageHtml
                self.item.latexExpression, self.newLatexExpression = self.oldLatexExpression, self.item.latexExpression
                self.item.update()
                return
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penColour=self.oldLocalPenColour)
            logger.info(
                'Undoing pen colour change. Changing pen colour of %s back to %s',
                self.item,
                QtGui.QColor(self.oldLocalPenColour).name())


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
            logger.info(
                'Changing pen style of %s to %d',
                self.item,
                self.newLocalPenStyle)

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penStyle=self.oldLocalPenStyle)
            logger.info(
                'Undoing pen style change. Changing pen style of %s back to %d',
                self.item,
                self.oldLocalPenStyle)


class ChangePenCapStyle(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super().__init__(parent)
        self.item = item
        self.oldLocalPenCapStyle = self.item.localPenCapStyle
        if 'penCapStyle' in kwargs:
            self.newLocalPenCapStyle = kwargs['penCapStyle']

    def redo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penCapStyle=self.newLocalPenCapStyle)
            logger.info(
                'Changing pen cap style of %s to %d',
                self.item,
                self.newLocalPenCapStyle)

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penCapStyle=self.oldLocalPenCapStyle)
            logger.info(
                'Undoing pen cap style change. Changing pen cap style of %s back to %d',
                self.item,
                self.oldLocalPenCapStyle)


class ChangePenJoinStyle(QtWidgets.QUndoCommand):
    def __init__(self, parent=None, item=None, **kwargs):
        super().__init__(parent)
        self.item = item
        self.oldLocalPenJoinStyle = self.item.localPenJoinStyle
        if 'penJoinStyle' in kwargs:
            self.newLocalPenJoinStyle = kwargs['penJoinStyle']

    def redo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penJoinStyle=self.newLocalPenJoinStyle)
            logger.info(
                'Changing pen join style of %s to %d',
                self.item,
                self.newLocalPenJoinStyle)

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalPenOptions(penJoinStyle=self.oldLocalPenJoinStyle)
            logger.info(
                'Undoing pen join style change. Changing pen join style of %s back to %d',
                self.item,
                self.oldLocalPenJoinStyle)


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
            logger.info(
                'Changing brush colour of %s to %s',
                self.item,
                QtGui.QColor(self.newLocalBrushColour).name())

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalBrushOptions(brushColour=self.oldLocalBrushColour)
            logger.info(
                'Undoing brush colour change. Changing brush colour of %s back to %s',
                self.item,
                QtGui.QColor(self.oldLocalBrushColour).name())


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
            logger.info(
                'Changing brush style of %s to %d',
                self.item,
                self.newLocalBrushStyle)

    def undo(self):
        if not hasattr(self, 'listOfItems'):
            self.item.setLocalBrushOptions(brushStyle=self.oldLocalBrushStyle)
            logger.info(
                'Undoing brush style change. Changing brush style of %s back to %d',
                self.item,
                self.oldLocalBrushStyle)
