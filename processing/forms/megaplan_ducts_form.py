from qgis.PyQt import QtGui, QtWidgets, QtCore
from qgis.PyQt.QtWidgets import QDialogButtonBox, QWidget, QPlainTextEdit, QPushButton,QTextEdit,QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem, QLabel
from  qgis.gui import QgsFileWidget, QgsExternalResourceWidget
import json
from functools import partial
import re
import webbrowser
import sys
from qgis.utils import iface
from PIL import ImageGrab
import os
import subprocess
from qgis.core import *
from time import sleep

layer = iface.activeLayer()
project_folder = QgsExpressionContextUtils.layerScope(layer).variable('project_folder')
photos_folder = QgsExpressionContextUtils.layerScope(layer).variable('photos_folder')


TypeRole = QtCore.Qt.UserRole + 1
DATA = None
with open(project_folder + os.sep + 'data.json',"r") as f:
    DATA = json.load(f)
# -----------------------------------------------------------------------------
# DATATYPES
# -----------------------------------------------------------------------------


class DataType(object):
    """Base class for data types."""

    COLOR = QtCore.Qt.black

    def matches(self, data):
        """Logic to define whether the given data matches this type."""
        raise NotImplementedError

    def next(self, model, data, parent):
        """Implement if this data type has to add child items to itself."""
        pass

    def actions(self, index):
        """Re-implement to return custom QActions."""

        return ["Edit","Add child","Remove"]

    def paint(self, painter, option, index):
        """Optionally re-implement for use by the delegate."""
        raise NotImplementedError

    def createEditor(self, parent, option, index):
        """Optionally re-implement for use by the delegate."""
        raise NotImplementedError

    def setModelData(self, editor, model, index):
        """Optionally re-implement for use by the delegate."""
        raise NotImplementedError

    def serialize(self, model, item, data, parent):
        """Serialize this data type."""
        value_item = parent.child(item.row(), 1)
        value = value_item.data(QtCore.Qt.DisplayRole)
        if isinstance(data, dict):
            key_item = parent.child(item.row(), 0)
            key = key_item.data(QtCore.Qt.DisplayRole)
            data[key] = value
        elif isinstance(data, list):
            data.append(value)

    def key_item(self, key, model, datatype=None, editable=True):
        """Create an item for the key column for this data type."""
        key_item = QtGui.QStandardItem(key)
        key_item.setData(datatype, TypeRole)
        key_item.setData(datatype.__class__.__name__, QtCore.Qt.ToolTipRole)
        key_item.setData(
            QtGui.QBrush(datatype.COLOR), QtCore.Qt.ForegroundRole)
        key_item.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        if editable and model.editable_keys:
            key_item.setFlags(key_item.flags() | QtCore.Qt.ItemIsEditable)
        return key_item

    def value_item(self, value, model, key=None):
        """Create an item for the value column for this data type."""
        display_value = value
        item = QtGui.QStandardItem(display_value)
        item.setData(display_value, QtCore.Qt.DisplayRole)
        item.setData(value, QtCore.Qt.UserRole)
        item.setData(self, TypeRole)
        item.setData(QtGui.QBrush(self.COLOR), QtCore.Qt.ForegroundRole)
        item.setFlags(
            QtCore.Qt.ItemIsSelectable |
            QtCore.Qt.ItemIsEnabled)
        if model.editable_values:
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        return item


# -----------------------------------------------------------------------------
# Default Types
# -----------------------------------------------------------------------------


class NoneType(DataType):
    """None"""

    def matches(self, data):
        return data is None

    def value_item(self, value, model, key=None):
        item = super(NoneType, self).value_item(value, model, key)
        item.setData('None', QtCore.Qt.DisplayRole)
        return item

    def serialize(self, model, item, data, parent):
        value_item = parent.child(item.row(), 1)
        value = value_item.data(QtCore.Qt.DisplayRole)
        value = value if value != 'None' else None
        if isinstance(data, dict):
            key_item = parent.child(item.row(), 0)
            key = key_item.data(QtCore.Qt.DisplayRole)
            data[key] = value
        elif isinstance(data, list):
            data.append(value)


class StrType(DataType):
    """Strings and unicodes"""

    def matches(self, data):
        return isinstance(data, str) or isinstance(data, unicode)


class IntType(DataType):
    """Integers"""

    def matches(self, data):
        return isinstance(data, int) and not isinstance(data, bool)


class FloatType(DataType):
    """Floats"""

    def matches(self, data):
        return isinstance(data, float)


class BoolType(DataType):
    """Bools are displayed as checkable items with a check box."""

    def matches(self, data):
        return isinstance(data, bool)

    def value_item(self, value, model, key=None):
        item = super(BoolType, self).value_item(value, model, key)
        item.setCheckState(QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)
        item.setData('', QtCore.Qt.DisplayRole)
        if model.editable_values:
            item.setFlags(
                item.flags() | QtCore.Qt.ItemIsEditable |
                QtCore.Qt.ItemIsUserCheckable)
        return item

    def serialize(self, model, item, data, parent):
        value_item = parent.child(item.row(), 1)
        value = value_item.checkState() == QtCore.Qt.Checked
        if isinstance(data, dict):
            key_item = parent.child(item.row(), 0)
            key = key_item.data(QtCore.Qt.DisplayRole)
            data[key] = value
        elif isinstance(data, list):
            data.append(value)


class ListType(DataType):
    """Lists"""

    def matches(self, data):
        return isinstance(data, list)

    def next(self, model, data, parent):
        for i, value in enumerate(data):
            type_ = match_type(value)
            key_item = self.key_item(
                str(i), datatype=type_, editable=False, model=model)
            value_item = type_.value_item(value, model=model, key=str(i))
            parent.appendRow([key_item, value_item])
            type_.next(model, data=value, parent=key_item)

    def value_item(self, value, model, key):
        item = QtGui.QStandardItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        return item

    def serialize(self, model, item, data, parent):
        key_item = parent.child(item.row(), 0)
        if key_item:
            if isinstance(data, dict):
                key = key_item.data(QtCore.Qt.DisplayRole)
                data[key] = []
                data = data[key]
            elif isinstance(data, list):
                new_data = []
                data.append(new_data)
                data = new_data
        for row in range(item.rowCount()):
            child_item = item.child(row, 0)
            type_ = child_item.data(TypeRole)
            type_.serialize(
                model=self, item=child_item, data=data, parent=item)


class DictType(DataType):
    """Dictionaries"""

    def matches(self, data):
        return isinstance(data, dict)

    def next(self, model, data, parent):
        for key, value in data.items():
            type_ = match_type(value)
            key_item = self.key_item(key, datatype=type_, model=model)
            value_item = type_.value_item(value, model, key)
            parent.appendRow([key_item, value_item])
            type_.next(model, data=value, parent=key_item)

    def value_item(self, value, model, key):
        item = QtGui.QStandardItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        return item

    def serialize(self, model, item, data, parent):
        key_item = parent.child(item.row(), 0)
        if key_item:
            if isinstance(data, dict):
                key = key_item.data(QtCore.Qt.DisplayRole)
                data[key] = {}
                data = data[key]
            elif isinstance(data, list):
                new_data = {}
                data.append(new_data)
                data = new_data
        for row in range(item.rowCount()):
            child_item = item.child(row, 0)
            type_ = child_item.data(TypeRole)
            type_.serialize(model=self, item=child_item, data=data, parent=item)


# -----------------------------------------------------------------------------
# Derived Types
# -----------------------------------------------------------------------------


class RangeType(DataType):
    """A range, shown as three spinboxes next to each other.

    A range is defined as a dict with start, end and step keys.
    It supports both floats and ints.
    """

    KEYS = ['start', 'end', 'step']

    def matches(self, data):
        if isinstance(data, dict) and len(data) == 3:
            if all([True if k in self.KEYS else False for k in data.keys()]):
                return True
        return False

    def paint(self, painter, option, index):
        data = index.data(QtCore.Qt.UserRole)

        painter.save()

        painter.setPen(QtGui.QPen(index.data(QtCore.Qt.ForegroundRole).color()))
        metrics = painter.fontMetrics()
        spinbox_option = QtWidgets.QStyleOptionSpinBox()
        start_rect = QtCore.QRect(option.rect)
        start_rect.setWidth(start_rect.width() / 3.0)
        spinbox_option.rect = start_rect
        spinbox_option.frame = True
        spinbox_option.state = option.state
        spinbox_option.buttonSymbols = QtWidgets.QAbstractSpinBox.NoButtons
        for i, key in enumerate(self.KEYS):
            if i > 0:
                spinbox_option.rect.adjust(
                    spinbox_option.rect.width(), 0,
                    spinbox_option.rect.width(), 0)
            QtWidgets.QApplication.style().drawComplexControl(
                QtWidgets.QStyle.CC_SpinBox, spinbox_option, painter)
            value = str(data[key])
            value_rect = QtCore.QRectF(
                spinbox_option.rect.adjusted(6, 1, -2, -2))
            value = metrics.elidedText(
                value, QtCore.Qt.ElideRight, value_rect.width() - 20)
            painter.drawText(value_rect, value)

        painter.restore()

    def createEditor(self, parent, option, index):
        data = index.data(QtCore.Qt.UserRole)
        wid = QtWidgets.QWidget(parent)
        wid.setLayout(QtWidgets.QHBoxLayout(parent))
        wid.layout().setContentsMargins(0, 0, 0, 0)
        wid.layout().setSpacing(0)

        start = data['start']
        end = data['end']
        step = data['step']

        if isinstance(start, float):
            start_spinbox = QtWidgets.QDoubleSpinBox(wid)
        else:
            start_spinbox = QtWidgets.QSpinBox(wid)

        if isinstance(end, float):
            end_spinbox = QtWidgets.QDoubleSpinBox(wid)
        else:
            end_spinbox = QtWidgets.QSpinBox(wid)

        if isinstance(step, float):
            step_spinbox = QtWidgets.QDoubleSpinBox(wid)
        else:
            step_spinbox = QtWidgets.QSpinBox(wid)

        start_spinbox.setRange(-16777215, 16777215)
        end_spinbox.setRange(-16777215, 16777215)
        step_spinbox.setRange(-16777215, 16777215)
        start_spinbox.setValue(start)
        end_spinbox.setValue(end)
        step_spinbox.setValue(step)
        wid.layout().addWidget(start_spinbox)
        wid.layout().addWidget(end_spinbox)
        wid.layout().addWidget(step_spinbox)
        return wid

    def setModelData(self, editor, model, index):
        #if isinstance(model, QtWidgets.QAbstractProxyModel):
        #    index = model.mapToSource(index)
        #    model = model.sourceModel()
        data = index.data(QtCore.Qt.UserRole)
        data['start'] = editor.layout().itemAt(0).widget().value()
        data['end'] = editor.layout().itemAt(1).widget().value()
        data['step'] = editor.layout().itemAt(2).widget().value()
        model.itemFromIndex(index).setData(data, QtCore.Qt.UserRole)

    def value_item(self, value, model, key=None):
        """Item representing a value."""
        value_item = super(RangeType, self).value_item(None, model, key)
        value_item.setData(value, QtCore.Qt.UserRole)
        return value_item

    def serialize(self, model, item, data, parent):
        value_item = parent.child(item.row(), 1)
        value = value_item.data(QtCore.Qt.UserRole)
        if isinstance(data, dict):
            key_item = parent.child(item.row(), 0)
            key = key_item.data(QtCore.Qt.DisplayRole)
            data[key] = value
        elif isinstance(data, list):
            data.append(value)


class UrlType(DataType):
    """Provide a link to urls."""

    REGEX = re.compile(r'(?:https?):\/\/|(?:file):\/\/')

    def matches(self, data):
        if isinstance(data, str) or isinstance(data, unicode):
            if self.REGEX.match(data) is not None:
                return True
        return False

    def actions(self, index):
        explore = QtWidgets.QAction('Explore ...', None)
        explore.triggered.connect(
            partial(webbrowser.open, index.data(QtCore.Qt.DisplayRole)))
        return [explore]


class FilepathType(DataType):
    """Files and paths can be opened."""

    REGEX = re.compile(r'(\/.*)|([A-Z]:\\.*)')

    def matches(self, data):
        if isinstance(data, str) or isinstance(data, unicode):
            if self.REGEX.match(data) is not None:
                return True
        return False

    def actions(self, index):
        explore = QtWidgets.QAction('Explore ...', None)
        path = index.data(QtCore.Qt.DisplayRole)
        explore.triggered.connect(partial(webbrowser.open, path))
        return [explore]


class ChoicesType(DataType):
    """A combobox that allows for a number of choices.

    The data has to be a dict with a value and a choices key.
    {
        "value": "A",
        "choices": ["A", "B", "C"]
    }
    """

    KEYS = ['value', 'choices']

    def matches(self, data):
        if isinstance(data, dict) and len(data) == 2:
            if all([True if k in self.KEYS else False for k in data.keys()]):
                return True
        return False

    def createEditor(self, parent, option, index):
        data = index.data(QtCore.Qt.UserRole)
        cbx = QtWidgets.QComboBox(parent)
        cbx.addItems([str(d) for d in data['choices']])
        cbx.setCurrentIndex(cbx.findText(str(data['value'])))
        return cbx

    def setModelData(self, editor, model, index):
        #if isinstance(model, QtWidgets.QAbstractProxyModel):
        #    index = model.mapToSource(index)
        #    model = model.sourceModel()
        data = index.data(QtCore.Qt.UserRole)
        data['value'] = data['choices'][editor.currentIndex()]
        model.itemFromIndex(index).setData(data['value'] , QtCore.Qt.DisplayRole)
        model.itemFromIndex(index).setData(data, QtCore.Qt.UserRole)

    def value_item(self, value, model, key=None):
        """Item representing a value."""
        value_item = super(ChoicesType, self).value_item(value['value'], model, key)
        value_item.setData(value, QtCore.Qt.UserRole)
        return value_item

    def serialize(self, model, item, data, parent):
        value_item = parent.child(item.row(), 1)
        value = value_item.data(QtCore.Qt.UserRole)
        if isinstance(data, dict):
            key_item = parent.child(item.row(), 0)
            key = key_item.data(QtCore.Qt.DisplayRole)
            data[key] = value
        elif isinstance(data, list):
            data.append(value)


# Add any custom DataType to this list
#
DATA_TYPES = [
    NoneType(),
    UrlType(),
    FilepathType(),
    StrType(),
    IntType(),
    FloatType(),
    BoolType(),
    ListType(),
    RangeType(),
    ChoicesType(),
    DictType()
]


def match_type(data):
    """Try to match the given data object to a DataType"""
    for type_ in DATA_TYPES:
        if type_.matches(data):
            return type_

# -----------------------------------------------------------------------------
# DELEGATE
# -----------------------------------------------------------------------------


class JsonDelegate(QtWidgets.QStyledItemDelegate):
    """Display the data based on the definitions on the DataTypes."""

    def sizeHint(self, option, index):
        return QtCore.QSize(option.rect.width(), 20)

    def paint(self, painter, option, index):
        """Use method from the data type or fall back to the default."""
        if index.column() == 0:
            return super(JsonDelegate, self).paint(painter, option, index)
        type_ = index.data(TypeRole)
        if isinstance(type_, DataType):
            try:
                super(JsonDelegate, self).paint(painter, option, index)
                return type_.paint(painter, option, index)
            except NotImplementedError:
                pass
        return super(JsonDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        """Use method from the data type or fall back to the default."""
        if index.column() == 0:
            return super(JsonDelegate, self).createEditor(
                parent, option, index)
        try:
            return index.data(TypeRole).createEditor(parent, option, index)
        except NotImplementedError:
            return super(JsonDelegate, self).createEditor(
                parent, option, index)

    def setModelData(self, editor, model, index):
        """Use method from the data type or fall back to the default."""
        if index.column() == 0:
            return super(JsonDelegate, self).setModelData(editor, model, index)
        try:
            return index.data(TypeRole).setModelData(editor, model, index)
        except NotImplementedError:
            return super(JsonDelegate, self).setModelData(editor, model, index)



# -----------------------------------------------------------------------------
# MODEL
# -----------------------------------------------------------------------------

class InputWindow_(QtWidgets.QDialog):
    """Main Window."""
    def __init__(self):
        """Initializer."""
        super().__init__()
        self.setWindowTitle("Add property and value")
        self.resize(400, 200)



        self.layout = QtWidgets.QGridLayout(self)

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.key = QtWidgets.QLineEdit()
        self.value = QtWidgets.QTextEdit()
        self.keyLabel = QtWidgets.QLabel("Property")
        self.valueLabel = QtWidgets.QLabel("Value")

        self.layout.addWidget(self.keyLabel, 0, 0)
        self.layout.addWidget(self.key, 0, 1)
        self.layout.addWidget(self.valueLabel, 1, 0)
        self.layout.addWidget(self.value, 1, 1)
        self.layout.addWidget(self.buttonBox, 2, 1)


class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

class InputWindow(QtWidgets.QDialog):
    """Main Window."""
    def __init__(self):
        """Initializer."""
        super().__init__()
        self.setWindowTitle("Add property and value")
        self.setMinimumSize(500,500)
        self.resize(1000, 1000)




        self.layout = QtWidgets.QGridLayout(self)

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        #self.key = QgsCheckableComboBox()
        self.list_ducts = []
        for obj in DATA:
            self.list_ducts.append(obj["Bezeichnung"])
        table_data = { "Ducts/Pipes":self.list_ducts, "Number":['0' for o in self.list_ducts]}

        #self.key.clear()
        #self.key.addItems(list_ducts)

        #self.value = QtWidgets.QgsCheckableTextEdit()
        self.keyLabel = QtWidgets.QLabel("Select children items")
        #self.valueLabel = QtWidgets.QLabel("Value")
        self.table = TableView(table_data, len(self.list_ducts), 2)

        self.layout.addWidget(self.keyLabel, 0, 0)
        #self.layout.addWidget(self.key, 0, 1)
        self.layout.addWidget(self.table, 1, 0)
        #self.layout.addWidget(self.valueLabel, 1, 0)
        #self.layout.addWidget(self.value, 1, 1)
        self.layout.addWidget(self.buttonBox, 2, 0)



class JsonModel(QtGui.QStandardItemModel):
    """Represent JSON-serializable data."""
    onDataUpdate_ = QtCore.pyqtSignal()
    def __init__(
            self, parent=None,
            data=None,
            editable_keys=False,
            editable_values=False):
        super(JsonModel, self).__init__(parent=parent)
        if data is not None:
            self.init(data, editable_keys, editable_values)

    def init(self, data, editable_keys=False, editable_values=False):
        """Convert the data to items and populate the model."""
        self.clear()
        self.setHorizontalHeaderLabels(['Property', 'Value'])
        self.editable_keys = editable_keys
        self.editable_values = editable_values
        parent = self.invisibleRootItem()
        type_ = match_type(data)
        parent.setData(type_, TypeRole)
        type_.next(model=self, data=data, parent=parent)
        self.dataChanged.connect(lambda: self.onDataUpdate_.emit())





    def serialize(self):
        """Assemble the model back into a dict or list."""
        parent = self.invisibleRootItem()
        type_ = parent.data(TypeRole)
        if isinstance(type_, ListType):
            data = []
        elif isinstance(type_, DictType):
            data = {}
        type_.serialize(model=self, item=parent, data=data, parent=parent)
        return data

    def addData(self, item, direction='insert'):
        self.input = InputWindow()

        if self.input.exec_() == QtWidgets.QDialog.Accepted:
            if item.hasChildren():
                print(item.row())
                type_ = item.data(TypeRole)
                data = []
                type_.serialize(model=self, item=item, data=data, parent=item)
                if item.row() == 0:
                    data = data[0]

                print(data)


                for i in range(0,item.rowCount()):
                    item.removeRow(0)

            else:

                data = []

            ducts = []
            for row, d in enumerate(self.input.list_ducts):
                if int(self.input.table.item(row, 1).text()) != 0:
                    for i in range( int(self.input.table.item(row, 1).text())):
                        ducts.append(self.input.table.item(row, 0).text())




            for duct in ducts:
                for d in DATA:
                    if duct == d["Bezeichnung"]:
                        data.append(d)


            type_ = match_type(data)


            if item.parent() is None:
                parent = self.invisibleRootItem()
            else:
                parent = item.parent()

            if direction == 'insert':
                item.setData(type_, TypeRole)
                type_.next(model=self, data=data, parent=item)

            self.onDataUpdate_.emit()




    def removeData(self, item):
        if item.parent() is None:
            parent = self.invisibleRootItem()
        else:
            parent = item.parent()
        parent.removeRow(item.row())
        self.onDataUpdate_.emit()





class JsonSortFilterProxyModel(QtCore.QSortFilterProxyModel):
    """Show ALL occurences by keeping the parents of each occurence visible."""

    def filterAcceptsRow(self, sourceRow, sourceParent):
        """Accept the row if the parent has been accepted."""
        index = self.sourceModel().index(sourceRow, self.filterKeyColumn(), sourceParent)
        return self.accept_index(index)

    def accept_index(self, index):
        if index.isValid():
            text = str(index.data(self.filterRole()))
            if self.filterRegExp().indexIn(text) >= 0:
                return True
            for row in range(index.model().rowCount(index)):
                if self.accept_index(index.model().index(row, self.filterKeyColumn(), index)):
                    return True
        return False


# -----------------------------------------------------------------------------
# VIEW
# -----------------------------------------------------------------------------


class JsonView(QtWidgets.QTreeView):
    """Tree to display the JsonModel."""

    def __init__(self, model, parent=None):
        super(JsonView, self).__init__(parent=parent)
        self.model = model

        #self.setRootIsDecorated(True)
        #self.setHeaderHidden(False)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._menu)
        self.setItemDelegate(JsonDelegate())



    def value(self):
        return self.model.serialize()


    def _menu(self, position):
        """Show the actions of the DataType (if any)."""
        menu = QtWidgets.QMenu()
        index = self.indexAt(position)
        data = index.data(TypeRole)

        if data is None:
            return
        for action in data.actions(index):
            menu.addAction(action)
        action = menu.exec_(self.viewport().mapToGlobal(position))
        if action:
            indexes = self.selectedIndexes()
            item = self.model.itemFromIndex(index)


            if action.text() == "Edit":
                self.edit(index)

            if action.text() == "Add child":
                if item.data(0) == 'Children':
                    self.model.addData(item)


            #if action.text() == "Insert sibling up":
            #    self.model.addData(item,'up')


            #if action.text() == "Insert sibling down":
            #    self.model.addData(item,'down')


            if action.text() == "Remove":
                self.model.removeData(item)










def take_screenshot(layer, photo_path, feature):


    geom = feature.geometry()
    polyline = geom.asPolyline()

    name = str(polyline[0].asWkt())
    os.system('SnippingTool.exe')




    im = ImageGrab.grabclipboard()
    im.save(photos_folder + os.sep + name + '.png','PNG')
    sleep(2)
    photo_path.setDocumentPath(photos_folder + os.sep + name + '.png')


    #pixmap  = QtGui.QPixmap(data_dir + os.sep + str(int(self.feature['id'])) + '.png')
    #self.image.setPixmap(pixmap)






def update_field(view, model, layer, feature, edit):

    data = model.serialize()



    print(data)
    edit.setPlainText(str(json.dumps(data)))
    try:
        idx = layer.fields().indexFromName('JSON')
        layer.changeAttributeValue(feature.id(), idx,str(json.dumps(data)))
    except:
        pass





def init_form(dialog, layer, feature):

    #idx = layer.fields().indexFromName('JSON')



    dialog.showButtonBox()

    #dialog.disconnectButtonBox()


    json_container = dialog.findChild(QPlainTextEdit, "JSON")
    photo_path = dialog.findChild(QgsExternalResourceWidget, "PHOTO")
    #buttonBox = dialog.findChild(QDialogButtonBox,"buttonBox")
    #buttonBox.accepted.disconnect(dialog.accept)
    #print(buttonBox)
    json_container.setVisible(True)
    print(json_container)
    #control_image = dialog.findChild(QWidget, "pushButton_photo")
    print(feature.id())
    try:
        if feature.id() > -9000000:
            data = json.loads(feature['JSON'])
        else:

            data = {"Graben":{"Children":[]}}
    except:
        data = json.loads(feature['JSON'])

    try:
        if feature.id() > -9000000:
            photo_data =  feature['PHOTO']
        else:
            photo_data =  ''
    except:
        photo_data =  ''
    #control_image.clicked.connect(take_screenshot)

    model = JsonModel(data=data, editable_keys=False, editable_values=True)
    view = JsonView(model)
    photo_path.setDocumentPath(photo_data)



    view.setModel(model)
    view.setAnimated(True)
    view.expandAll()
    #view.show()
    #widget_wraper = MyQgsEditorWidgetWrapper(layer, idx, view, model, parent=None)
    #widget_wraper.setFormFeature(feature)
    photo = QPushButton('Take Screenshot')



    dialog.layout().addWidget(photo)
    dialog.layout().addWidget(view)
    update_field(view, model, layer, feature, json_container)
    photo.clicked.connect(lambda: take_screenshot(layer, photo_path, feature))
    model.onDataUpdate_.connect(lambda: update_field(view,model,layer, feature,json_container))
    #buttonBox.accepted.connect(lambda: validate(model,layer, feature,json_container))
