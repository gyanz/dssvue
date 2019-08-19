import logging
import sys
import os
from datetime import datetime
import numpy as np
import pandas as pd
from .mplqt import *
from .models import CustomTableView,PathDataModel,create_toc_data,PairedDataWindow,MplPlotWindow
from pydsstools.heclib.dss.HecDss import Open
from pydsstools.core import DssPathName

ui_dir = os.path.join(os.path.dirname(__file__),'ui')

class DSSVue(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__),'ui','main.ui'),self)
        self.setWindowTitle('dssvue')
        self.add_gui_elements()
        self.init_toc()
        self.set_variables()
        self.add_actions()

    def add_gui_elements(self):
        pass

    def set_variables(self):    
        self.dss_fid = None

    def add_actions(self):
        self.reset_row_action = self.createAction('Reset Rows',self.reset_rows,None,
                    '','',None)
        self.excel_action = self.createAction('Open in Excel',self.show_excel,None,
                    'excel.ico','',None)
        self.table_action = self.createAction('Show table',self.show_table,None,
                    'table.ico','',None)
        self.plot_action = self.createAction('Show Plot',self.show_plot,None,
                    'plot.ico','',None)
        self.toolbar = self.addToolBar('Ribbon')
        self.toolbar.addAction(self.reset_row_action)
        self.toolbar.addAction(self.excel_action)
        self.toolbar.addAction(self.table_action)
        self.toolbar.addAction(self.plot_action)

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                    tip=None, checkable=None, signal="triggered"):
        action = QAction(text, self)
        if icon is not None:
            pass
            action.setIcon(QIcon(QtGui.QPixmap(os.path.join(ui_dir,icon))))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            getattr(action,signal).connect(slot)
        if checkable is not None:
            action.setCheckable(True)
        return action

    def show_excel(self):
        try:
            file_prefix = os.path.join(tempfile.gettempdir(),'RiskRAS')
            file_suffix = str(uuid1()) + '.xlsx'
            filename = file_prefix + file_suffix
            df = self.tableview.model().getData()
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')
            df.to_excel(writer,sheet_name='Sheet1')
            writer.save()
            #os.startfile(filename)
            open_file(filename)
        except:
            logging.warn('Error opening data in excel.')

    def selected(self):
        index = self.toc_tv.currentIndex()
        pathname = self.toc_tv.model().get_pathname(index)
        typ = self.toc_tv.model().get_type(index)
        print(pathname)
        print(typ)
        return typ,pathname

    def show_table(self):
        typ, pathname = self.selected()
        if typ == 'TS':
            ts = self.dss_fid.read_ts(pathname)
            if not ts.empty:
                times = np.array(ts.pytimes)
                times = times[~ts.nodata]
                times = times.tolist()
                values = ts.values[~ts.nodata].tolist()     
                data = [xy for xy in zip(times,values)] 
                data = np.array(data,dtype=[('Date',object),('Value',float)])
                print(data)
                win = QtGui.QMainWindow(self)
                win.setWindowTitle('Time Series')
                t = pg.TableWidget()
                win.setCentralWidget(t)
                t.setData(data)
                win.resize(500,500)
                win.show()

        elif typ == 'PD':
            df = self.dss_fid.read_pd(pathname)
            print('%r'%df.head())
            idx = df.index.tolist()
            df.insert(0,df.index.name,idx)
            df.index = range(1,df.shape[0] + 1)
            
            win = PairedDataWindow(df,parent=self)
            win.show()

        elif typ == 'GRID':
            pass

        else:
            pass

    def show_plot(self):
        typ, pathname = self.selected()
        if typ == 'TS':
            ts = self.dss_fid.read_ts(pathname)
            if not ts.empty:
                times = np.array(ts.pytimes)
                times = times[~ts.nodata].tolist()
                values = ts.values[~ts.nodata].tolist()     
                win = MplPlotWindow(times,values,pathname,self)
                win.show()

        elif typ == 'PD':
            pass

        elif typ == 'GRID':
            dataset = self.dss_fid.read_grid(pathname)
            data = dataset.read(masked=True) 
            pg.image(data,title=pathname)

        else:
            pass
        

    def reset_rows(self):
        self.toc_tv.model().reset_rows()

    def init_toc(self):
        df = create_toc_data(None)
        self.toc_tv = CustomTableView() 
        self.toc_tv.setSortingEnabled(True)
        model = PathDataModel(df)
        self.toc_tv.setModel(model)
        self.setCentralWidget(self.toc_tv)

    def open_dss(self,dss_file):
        if not self.dss_fid is None:
            self.dss_fid.close()
        self.dss_fid = Open(dss_file)
        self._load_pathnames()

    def _load_pathnames(self,condense=True):
        if isinstance(self.dss_fid,Open):
            path_list = []
            path_dict = self.dss_fid.getPathnameDict()
            print(path_dict)
            for typ,paths in path_dict.items():
                for path in paths:
                    pathobj = DssPathName(path)
                    parts = [typ] + pathobj.getParts()
                    path_list.append(parts)
            df = create_toc_data(path_list) 
            if condense:
                df = self._condense_pathnames(df)
            self.toc_tv.model().set_data(df)

    def _condense_pathnames(self,df):
        ts_df = df[df.Type == 'TS']
        ts_parts = []
        for _,ts in ts_df.groupby(by=["A","B","C","E","F"]):
            d_parts = [datetime.strptime(x,'%d%b%Y') for x in ts.D.tolist()]
            _min = min(d_parts).strftime('%d%b%Y')
            _max = max(d_parts).strftime('%d%b%Y')
            d_part = '%s - %s'%(_min,_max)
            parts = ['TS',
                     ts.A.iloc[0],
                     ts.B.iloc[0],
                     ts.C.iloc[0],
                     d_part,
                     ts.E.iloc[0],
                     ts.F.iloc[0]]
            ts_parts.append(parts)
                      
        ts_df = create_toc_data(ts_parts)        
        rest_df = df[df.Type != 'TS'] 
        df = pd.concat([ts_df,rest_df],ignore_index=True)
        return df

    def get_selected(self):
        pass


def show(dss_file):
    APP = mkQApp()
    window = DSSVue()
    window.open_dss(dss_file)
    window.show() 
    APP.exec_()
        



if __name__ == "__main__":
    app = mkQApp()
    #window = DSSVue() #
    logging.debug('START EVENT LOOP')
    #exit_status = app.exec_()
    show()
    logging.debug('END OF EVENT LOOP, EXIT STATUS = %s',exit_status)
    sys.exit(exit_status)
