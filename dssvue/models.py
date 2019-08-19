import logging
import pandas as pd
from .mplqt import *

toc_headers = ["Type","A","B","C","D","E","F"]

class PathDataModel(QtCore.QAbstractTableModel):
    def __init__(self,array_df,parent=None):
        super().__init__(parent)
        if not isinstance(array_df, pd.DataFrame):
            logging.warn('Data assigned must be pandas dataframe')
            array_df = None
        self.__container = array_df

    def rowCount(self, parent=QtCore.QModelIndex):
        if not self.empty():
            return self.__container.shape[0]
        return 0

    def columnCount(self, parent=QtCore.QModelIndex()):
        # Type,A,B,C,D,E,F
        return 7

    def rows(self):
        if not self.empty():
            return self.__container.shape[0]
        return 0

    def cols(self):
        if not self.empty():
            return self.__container.shape[1]
        return 0

    def columns(self):
        if not self.empty():
            return self.__container.columns.tolist()

    def empty(self):
        if self.__container is None:
            return True
        return False

    def flags(self, index):
        return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def getData(self):
        return self.__container

    get_data = getData

    def set_data(self,array_df):
        if not isinstance(array_df, pd.DataFrame):
            logging.warn('Data assigned must be pandas DataFrame')
            return
        logging.debug('Model Data assignment ...')
        self.layoutAboutToBeChanged.emit()
        self.__container = array_df
        self.layoutChanged.emit()
        logging.debug('Model Data assignment completed.')

    def data(self, index, role=None):
        if index.isValid():
            if self.empty():
                return False
            row = index.row()
            column = index.column()
            value = str(self.__container.iloc[row,column])

            if role is None:
                return value

            if role == QtCore.Qt.DisplayRole:
                return value

            if role == QtCore.Qt.EditRole:
                return False

            if role == QtCore.Qt.ToolTipRole:
                return False

            if role == QtCore.Qt.DecorationRole:
                return False
    
    def get_pathname(self,index):
        if index.isValid():
            row = index.row()
            data = self.__container.iloc[row,:]
            parts = data.A,data.B,data.C,data.D,data.E,data.F
            path = '/' + '/'.join(parts) + '/'
            return path

    def get_type(self,index):
        if index.isValid():
            row = index.row()
            data = self.__container.iloc[row,:]
            return data.Type

    def size(self):
        if not self.empty():
            return self.__container.shape[0]

    def headerData(self, section, orientation, role):
        if not self.empty():
            hor_headers = self.__container.columns.tolist()
            vert_headers = self.__container.index.tolist()
            if role == QtCore.Qt.DisplayRole:

                if orientation == QtCore.Qt.Horizontal:

                    if section < len(hor_headers):
                        return hor_headers[section]
                    else:
                        return "not implemented"
                elif orientation == QtCore.Qt.Vertical:
                    return vert_headers[section] #section + 1

    def reset_rows(self):
        self.layoutAboutToBeChanged.emit()
        self.__container = self.__container.sort_index()
        self.layoutChanged.emit()

    def sort(self, Ncol, order):
        """Sort table by given column number."""
        self.layoutAboutToBeChanged.emit()
        self.__container = self.__container.sort_values(self.__container.columns.tolist()[Ncol],
                                                        ascending=order == Qt.AscendingOrder)
        self.layoutChanged.emit()


class DataModel(QtCore.QAbstractTableModel):
    def __init__(self,array_df,parent=None):
        super().__init__(parent)
        if not isinstance(array_df, pd.DataFrame):
            logging.warn('Data assigned must be pandas dataframe')
            array_df = None
        self.__container = array_df

    def rowCount(self, parent=QtCore.QModelIndex):
        if not self.empty():
            return self.__container.shape[0]
        return 0

    def columnCount(self, parent=QtCore.QModelIndex()):
        if not self.empty():
            return self.__container.shape[1]
        return 0

    def rows(self):
        if not self.empty():
            return self.__container.shape[0]
        return 0

    def cols(self):
        if not self.empty():
            return self.__container.shape[1]
        return 0

    def columns(self):
        if not self.empty():
            return self.__container.columns.tolist()

    def empty(self):
        if self.__container is None:
            return True
        return False

    def flags(self, index):
        return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def getData(self):
        return self.__container

    get_data = getData

    def set_data(self,array_df):
        if not isinstance(array_df, pd.DataFrame):
            logging.warn('Data assigned must be pandas DataFrame')
            return
        logging.debug('Model Data assignment ...')
        self.layoutAboutToBeChanged.emit()
        self.__container = array_df
        self.layoutChanged.emit()
        logging.debug('Model Data assignment completed.')

    def data(self, index, role=None):
        if index.isValid():
            if self.empty():
                return False
            row = index.row()
            column = index.column()
            value = str(self.__container.iloc[row,column])

            if role is None:
                return value

            if role == QtCore.Qt.DisplayRole:
                return value

            if role == QtCore.Qt.EditRole:
                return False

            if role == QtCore.Qt.ToolTipRole:
                return False

            if role == QtCore.Qt.DecorationRole:
                return False
    
    def size(self):
        if not self.empty():
            return self.__container.shape[0]

    def headerData(self, section, orientation, role):
        if not self.empty():
            hor_headers = self.__container.columns.tolist()
            vert_headers = self.__container.index.tolist()
            if role == QtCore.Qt.DisplayRole:

                if orientation == QtCore.Qt.Horizontal:

                    if section < len(hor_headers):
                        return hor_headers[section]
                    else:
                        return "not implemented"
                elif orientation == QtCore.Qt.Vertical:
                    return vert_headers[section] #section + 1

    def reset_rows(self):
        self.layoutAboutToBeChanged.emit()
        self.__container = self.__container.sort_index()
        self.layoutChanged.emit()

    def sort(self, Ncol, order):
        """Sort table by given column number."""
        self.layoutAboutToBeChanged.emit()
        self.__container = self.__container.sort_values(self.__container.columns.tolist()[Ncol],
                                                        ascending=order == Qt.AscendingOrder)
        self.layoutChanged.emit()

class CustomTableView(QTableView):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._first_show = 1

    def resizeEvent(self,event):
        super().resizeEvent(event)
        if self._first_show:
            header = self.horizontalHeader()
            for column in range(header.count()):
                header.setSectionResizeMode(column,QHeaderView.ResizeToContents)
                width = header.sectionSize(column)
                header.setSectionResizeMode(column,QHeaderView.Interactive)
                header.resizeSection(column, width)

class PairedDataWindow(QMainWindow):
    def __init__(self, data=None, title='', parent = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.tableview = CustomTableView()
        model = DataModel(data)
        self.tableview.setModel(model)
        self.resize(500,500)
        self.setCentralWidget(self.tableview)

    def setData(self,data):
        self.tableview.model().set_data(data)

class GridImageWindow(QMainWindow):
    def __init__(self, data=None, title='', parent = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.tableview = CustomTableView()
        model = DataModel(data)
        self.tableview.setModel(model)
        self.resize(500,500)
        self.setCentralWidget(self.tableview)

    def setData(self,data):
        self.tableview.model().set_data(data)


class MplPlotWindow(QMainWindow):
    def __init__(self,x,y,title='', parent = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.mplwidget = MatplotlibWidget() 
        self.setCentralWidget(self.mplwidget)
        self.ax = self.mplwidget.getFigure().add_subplot(111)
        self.ax.plot(x,y,'.')
        self.mplwidget.draw()


def create_toc_data(data):
    if data is None or data =='':
        return pd.DataFrame(columns=toc_headers)
    else:
        return pd.DataFrame(data=data,columns=toc_headers)


