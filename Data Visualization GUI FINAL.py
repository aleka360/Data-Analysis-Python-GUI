# Data analysis tool to graph variables from CSV Files
#
#CSV File needs UTF-8 codec
#
#
#
#

import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem,  QAbstractItemView, QMessageBox, QFileDialog
from PyQt5 import uic, QtCore
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import xlwt
import xlrd





qtCreatorFile = "csv table gui.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #button actions
        self.import_button.clicked.connect(self.LoadCsv)#import
        self.add_button.clicked.connect(self.AddVariable)#Add to table
        self.table_widget.cellClicked.connect(self.cell_was_clicked)#Part of above
        self.plot_button.clicked.connect(self.PlotVariables)#plot
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)#number of rows to fill in
        self.help_button.clicked.connect(self.Help_Window)#help
        self.export_button.clicked.connect(self.savefile)#export able
        self.load_button.clicked.connect(self.loadfile)#import table
        self.clear_button.clicked.connect(self.ClearTable)#clear
        
        
      
        
        
        
    def ClearTable(self):
        self.table_widget.clearContents()
        
        
        
    def savefile(self):
        filename,_ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.table_widget.model()
        for c in range(model.columnCount()):
            text = model.headerData(c, QtCore.Qt.Horizontal)
            sheet.write(0, c+1, text, style=style)
    
        for r in range(model.rowCount()):
            text = model.headerData(r, QtCore.Qt.Vertical)
            sheet.write(r+1, 0, text, style=style)
    
        for c in range(model.columnCount()):
            for r in range(model.rowCount()):
                text = model.data(model.index(r, c))
                sheet.write(r+1, c+1, text)
        wbk.save(filename)


    def loadfile(self):
        
        root = tk.Tk()
        root.withdraw()
        file_path=filedialog.askopenfilename()
        loc = (file_path) 
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0)
        
        data = [[sheet.cell_value(r,c) for c in range (sheet.ncols)] for r in range(sheet.nrows)]

        headers = data[0]
        Data = data[1:]
        self.table_widget.setHorizontalHeaderLabels(headers)
        
        
        for row, columnvalues in enumerate(Data):
            for column, value in enumerate(columnvalues): 
                item = QTableWidgetItem(value)
                self.table_widget.setItem(row, column, item)
        self.table_widget.removeColumn(0)
       
        
    def cell_was_clicked(self, row, column):
        self.table_widget.itemAt(row, column)
        global r1
        global r2
        global r3
        global r4
        global c
        c = column
        r1 = row
        r2 = row+1
        r3 = row+2
        r4 = row+3
        
    def LoadCsv(self):
        root = tk.Tk()
        root.withdraw()
        file_path=filedialog.askopenfilename()
        global data
        data = pd.read_csv(file_path)
        global df 
        df = pd.DataFrame(data)
        self.variables = list(df.columns.values)
        self.list_widget.addItems(self.variables)
        self.list_widget.setCurrentRow(0)
       
    def Help_Window(self):
        msg=QMessageBox()
        msg.setWindowTitle("How to use")
        msg.setText("This is a tool to help with data analysis and visualization. \n\nTo start, select a csv file with data you want to visualize. Make sure the file is encoded with UTF-8. \n\nNext, select the variable you want to add to a cell, select the cell on the table, and then press the Add button. \n\nIn the case you want to add the same variable to multiple cells within the same column, select how many cells you want from the left hand side drop down menu (Values range from 1-4), click the variable, then the top cell of where you want the variables to be inputed, and then click Add. \n\nOnce you have all the variables in their corresponding cells, to graph them, select the rows you want to graph. To do this, click the bottom-most cell of the set fo graphs, and drag the cursor up until all the rows you want to graph are blue, this makes sure everything works correctly. \n\n IMPORTANT: make sure you choose the correct settings before plotting the graphs. \n\nIf your x-variable has omitted data (NaN values), do not select the Time Series option. This option is for continuous variables with no gaps between values. Additionally, do not try to graph a time series plot and a non-time series plot within one action (it can only deal with one type of data at a time) \n\nOnce you press the plot button, a pop-up window with the graphs will appear. You are able to have multiple separate pop-up windows at a time, so it is not necessary to close one graph to graph another. \n\nTo export your current table setup, just click the 'Export Table' button and save the file. To then load it back in, click the 'Import Table' button and select the correct file. \n\nOnce imported, make sure you have all the CSV files the table uses before trying to graph.")
        msg.exec_()
        
    def AddVariable(self, list_widget):
        if self.fillCombo_box.currentText() == "1":
            self.table_widget.setItem(r1,c, QTableWidgetItem(str(self.list_widget.currentItem().text())))
            
        if self.fillCombo_box.currentText() == "2":
            self.table_widget.setItem(r1,c, QTableWidgetItem(str(self.list_widget.currentItem().text())))
            self.table_widget.setItem(r2,c, QTableWidgetItem(str(self.list_widget.currentItem().text())))
            
        if self.fillCombo_box.currentText() == "3":
            self.table_widget.setItem(r1,c, QTableWidgetItem(str(self.list_widget.currentItem().text())))
            self.table_widget.setItem(r2,c, QTableWidgetItem(str(self.list_widget.currentItem().text())))
            self.table_widget.setItem(r3,c, QTableWidgetItem(str(self.list_widget.currentItem().text())))
            
        if self.fillCombo_box.currentText() == "4":
            self.table_widget.setItem(r1,c, QTableWidgetItem(str(self.list_widget.currentItem().text())))
            self.table_widget.setItem(r2,c, QTableWidgetItem(str(self.list_widget.currentItem().text())))
            self.table_widget.setItem(r3,c, QTableWidgetItem(str(self.list_widget.currentItem().text())))
            self.table_widget.setItem(r4,c, QTableWidgetItem(str(self.list_widget.currentItem().text())))
    
    def getsamerowcell(self, table_widget,columnname):

        ROW = table_widget.currentItem().row()
        headercount = table_widget.columnCount()
        for x in range(0,headercount,1):
            headertext = table_widget.horizontalHeaderItem(x).text()
            if columnname == headertext:
                cell = table_widget.item(ROW, x).text()   # get cell at row, col
                return str(cell)
    
    def getsamerowcell_2(self, table_widget,columnname):

        m = int(len(table_widget.selectionModel().selectedRows())-1)
        ROW = table_widget.currentItem().row()
        headercount = table_widget.columnCount()
        for x in range(0,headercount,1):
            headertext = table_widget.horizontalHeaderItem(x).text()
            if columnname == headertext:
                cell = table_widget.item(ROW + m, x).text()   # get cell at row, col
                return str(cell)
            
    def getsamerowcell_3(self, table_widget,columnname):

        m = int(len(table_widget.selectionModel().selectedRows())-2)
        ROW = table_widget.currentItem().row()
        headercount = table_widget.columnCount()
        for x in range(0,headercount,1):
            headertext = table_widget.horizontalHeaderItem(x).text()
            if columnname == headertext:
                cell = table_widget.item(ROW + m, x).text()   # get cell at row, col
                return str(cell)
            
            
    def getsamerowcell_4(self, table_widget,columnname):

        m = int(len(table_widget.selectionModel().selectedRows())-3)
        ROW = table_widget.currentItem().row()
        headercount = table_widget.columnCount()
        for x in range(0,headercount,1):
            headertext = table_widget.horizontalHeaderItem(x).text()
            if columnname == headertext:
                cell = table_widget.item(ROW + m, x).text()   # get cell at row, col
                return str(cell)

        
        
   
        
    def PlotVariables(self, table_widget):
        if self.Cont_X.isChecked() == True:
            if self.Cont_Y.isChecked() == False:
               if self.combo_box.currentText() == "2":
                    if int(len(self.table_widget.selectionModel().selectedRows()))==1:
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                        y1a_cell = self.getsamerowcell(self.table_widget, "Var y-axis-2")
                    
                     #Retrieve Graph 1 Variables from cell names
                        x1=df[str(x1_cell)]
                        y1=df[str(y1_cell)]
                        y1a=df[str(y1a_cell)]
                    #make continuous line from broken data
                        s1mask = np.isfinite(y1)
                        s1amask = np.isfinite(y1a)
               
                        color='tab:red'
                        fig, (ax1) = plt.subplots(1, sharex='col', sharey='row')
               
                    #Plot 1 create
               
                        ax1.plot(x1[s1mask],y1[s1mask], label= str(y1_cell), color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel("Kg", color=color)
                        ax1.tick_params(axis='y')
                        
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                        
                        
                   
                        color='tab:blue'
                        ax1.plot(x1[s1mask],y1a[s1amask], label= str(y1a_cell), color=color)
                        
                        
                        ax1.legend(loc = "upper right")
                        plt
                        
                    
                        
                        plt.show()
                    
                    
                    if int(len(self.table_widget.selectionModel().selectedRows()))==2:
                       #retreive cell names
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                        y1a_cell = self.getsamerowcell(self.table_widget, "Var y-axis-2")
                   
                        x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                        y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                        y2a_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-2")
                  
                   #Retrieve Graph 1 Variables from cell names
                        x1=df[str(x1_cell)]
                        y1=df[str(y1_cell)]
                        y1a=df[str(y1a_cell)]
                   
                   #Retrieve Graph 2 Variables from cell names
                        x2=df[str(x2_cell)]
                        y2=df[str(y2_cell)]
                        y2a=df[str(y2a_cell)]
                   
                   #Connect the dots
                   
                        s1mask = np.isfinite(y1)
                        s1amask = np.isfinite(y1a)
                        
                        s2mask = np.isfinite(y2)
                        s2amask = np.isfinite(y2a)
                   
                   #Main plot create
                   
                        color='tab:red'
                        fig, (ax1,ax2) = plt.subplots(2, sharex='col', sharey='row')
                   
                   #Plot 1 create
                   
                        ax1.plot(x1[s1mask],y1[s1mask], label= str(y1_cell), color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel(str("Kg"), color=color)
                        ax1.tick_params(axis='y')
                        
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        
                        ax1.plot(x1[s1mask],y1a[s1amask],label= str(y1a_cell), color=color)
                        ax1.legend(loc = "upper right")
                        plt.show()
                   
                   #Plot 2 create
            
                        color='tab:red'
                 
                        ax2.plot(x2[s1mask],y2[s2mask], label= str(y2_cell), color=color)
                        ax2.set_xlabel(str(x2_cell))
                        ax2.set_ylabel("Kg", color=color)
                        ax2.tick_params(axis='y')
                        
                        ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax2.minorticks_on()
                        ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        ax2.plot(x2[s2mask],y2a[s2amask],label= str(y2a_cell), color=color)
                        ax2.legend(loc = "upper right")
                        plt.show()
                     
                    if int(len(self.table_widget.selectionModel().selectedRows()))==3:
                       #retreive cell names
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                        y1a_cell = self.getsamerowcell(self.table_widget, "Var y-axis-2")
                   
                        x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                        y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                        y2a_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-2")
                        
                        x3_cell = self.getsamerowcell_3(self.table_widget, "Var x-axis")
                        y3_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-1")
                        y3a_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-2")
                  
                   #Retrieve Graph 1 Variables from cell names
                        x1=df[str(x1_cell)]
                        y1=df[str(y1_cell)]
                        y1a=df[str(y1a_cell)]
                   
                   #Retrieve Graph 2 Variables from cell names
                        x2=df[str(x2_cell)]
                        y2=df[str(y2_cell)]
                        y2a=df[str(y2a_cell)]
                        
                        x3=df[str(x3_cell)]
                        y3=df[str(y3_cell)]
                        y3a=df[str(y3a_cell)]
                   
                   #Connect the dots
                   
                        s1mask = np.isfinite(y1)
                        s1amask = np.isfinite(y1a)
                        
                        s2mask = np.isfinite(y2)
                        s2amask = np.isfinite(y2a)
                        
                        s3mask = np.isfinite(y3)
                        s3amask = np.isfinite(y3a)
                   
                   #Main plot create
                   
                        color='tab:red'
                        fig, (ax1,ax2,ax3) = plt.subplots(3, sharex='col', sharey='row')
                   
                   #Plot 1 create
                   
                        ax1.plot(x1[s1mask],y1[s1mask], label= str(y1_cell), color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel("Kg", color=color)
                        ax1.tick_params(axis='y')
                        
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        ax1.plot(x1[s1mask],y1a[s1amask],label= str(y1a_cell), color=color)
                        ax1.legend(loc = "upper right")
                        plt.show()
                        
                        
                   
                   #Plot 2 create
            
                        color='tab:red'
                 
                        ax2.plot(x2[s1mask],y2[s2mask],label= str(y2_cell), color = color)
                        ax2.set_xlabel(str(x2_cell))
                        ax2.set_ylabel("Kg", color=color)
                        ax2.tick_params(axis='y')
                        
                        ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax2.minorticks_on()
                        ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                        ax2a=ax2.twinx() #create second set of y axis for second graph
                   
                        color='tab:blue'
                   
                        ax2.plot(x2[s2mask],y2a[s2amask], label= str(y2a_cell), color=color)
                        ax2a.set_ylabel(str(y2a_cell), color=color)
                        ax2.legend(loc = "upper right")
                        plt.show()
                    
                  #Plot 3 create
            
                        color='tab:red'
                 
                        ax3.plot(x3[s1mask],y3[s3mask], label= str(y3_cell), color=color)
                        ax3.set_xlabel(str(x3_cell))
                        ax3.set_ylabel("Kg", color=color)
                        ax3.tick_params(axis='y')
                        
                        ax3.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax3.minorticks_on()
                        ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        ax3.plot(x3[s3mask],y3a[s2amask], label= str(y3a_cell), color=color)
                        ax3.legend(loc = "upper right")
                        plt.show()
                        
                        
                    if int(len(self.table_widget.selectionModel().selectedRows()))==4:
                       #retreive cell names
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                        y1a_cell = self.getsamerowcell(self.table_widget, "Var y-axis-2")
                   
                        x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                        y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                        y2a_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-2")
                        
                        x3_cell = self.getsamerowcell_3(self.table_widget, "Var x-axis")
                        y3_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-1")
                        y3a_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-2")
                        
                        x4_cell = self.getsamerowcell_4(self.table_widget, "Var x-axis")
                        y4_cell = self.getsamerowcell_4(self.table_widget, "Var y-axis-1")
                        y4a_cell = self.getsamerowcell_4(self.table_widget, "Var y-axis-2")
                  
                   #Retrieve Graph 1 Variables from cell names
                        x1=df[str(x1_cell)]
                        y1=df[str(y1_cell)]
                        y1a=df[str(y1a_cell)]
                   
                   #Retrieve Graph 2 Variables from cell names
                        x2=df[str(x2_cell)]
                        y2=df[str(y2_cell)]
                        y2a=df[str(y2a_cell)]
                        
                   #Retrieve Graph 3 Variables from cell names
                        x3=df[str(x3_cell)]
                        y3=df[str(y3_cell)]
                        y3a=df[str(y3a_cell)]
                        
                   #Retrieve Graph 4 Variables from cell names
                        x4=df[str(x4_cell)]
                        y4=df[str(y4_cell)]
                        y4a=df[str(y4a_cell)]
                   
                   #Connect the dots
                   
                        s1mask = np.isfinite(y1)
                        s1amask = np.isfinite(y1a)
                        
                        s2mask = np.isfinite(y2)
                        s2amask = np.isfinite(y2a)
                        
                        s3mask = np.isfinite(y3)
                        s3amask = np.isfinite(y3a)
                        
                        s4mask = np.isfinite(y4)
                        s4amask = np.isfinite(y4a)
                   
                   #Main plot create
                   
                        color='tab:red'
                        fig, (ax1,ax2,ax3,ax4) = plt.subplots(4, sharex='col', sharey='row')
                   
                   #Plot 1 create
                   
                        ax1.plot(x1[s1mask],y1[s1mask], label= str(y1_cell), color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel("Kg", color=color)
                        ax1.tick_params(axis='y')
                   
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                        
                        
                   
                        color='tab:blue'
                   
                        ax1.plot(x1[s1mask],y1a[s1amask],label= str(y1a_cell), color=color)
                        ax1.legend(loc = "upper right")
                        plt.show()
                   
                   #Plot 2 create
            
                        color='tab:red'
                 
                        ax2.plot(x2[s1mask],y2[s2mask],label= str(y2_cell), color=color)
                        ax2.set_xlabel(str(x2_cell))
                        ax2.set_ylabel("Kg", color=color)
                        ax2.tick_params(axis='y')
                        
                        ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax2.minorticks_on()
                        ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                                  
                        color='tab:blue'
                   
                        ax2.plot(x2[s2mask],y2a[s2amask],label= str(y2a_cell), color=color)
                        ax2.legend(loc = "upper right")
                        plt.show()
                    
                    
                  #Plot 3 create
            
                        color='tab:red'
                 
                        ax3.plot(x3[s1mask],y3[s3mask], label= str(y3_cell), color=color)
                        ax3.set_xlabel(str(x3_cell))
                        ax3.set_ylabel("Kg", color=color)
                        ax3.tick_params(axis='y')
                        
                        ax3.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax3.minorticks_on()
                        ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        ax3.plot(x3[s3mask],y3a[s3amask], label= str(y3a_cell), color=color)
                        ax3.legend(loc = "upper right")
                        plt.show()
                        
                        
                    #Plot 4 create
            
                        color='tab:red'
                 
                        ax4.plot(x4[s1mask],y4[s4mask],label= str(y4_cell), color=color)
                        ax4.set_xlabel(str(x4_cell))
                        ax4.set_ylabel("Kg", color=color)
                        ax4.tick_params(axis='y')
                        
                        ax4.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax4.minorticks_on()
                        ax4.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        ax4.plot(x4[s4mask],y4a[s4amask], label= str(y4a_cell), color=color)
                        ax4.legend(loc = "upper right")
                        plt.show()
                        
                        
               if self.combo_box.currentText() == "1":
                if int(len(self.table_widget.selectionModel().selectedRows()))==1:
                    x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                    y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                    
                
                 #Retrieve Graph 1 Variables from cell names
                    
                    x1=np.array(df[str(x1_cell)])
                    y1=np.array(df[str(y1_cell)])
                    
             
                    
                
                    s1mask = np.isfinite(y1)
                    
           
                    color='tab:red'
                    fig, (ax1) = plt.subplots(1, sharex='col', sharey='row')
           
                #Plot 1 create
           
                    ax1.plot(x1[s1mask],y1[s1mask], color=color)
                    ax1.set_xlim([np.nanmin(x1), np.nanmax(x1)])
                    ax1.set_ylim([np.nanmin(y1), np.nanmax(y1)])
                    ax1.set_xlabel(str(x1_cell))
                    ax1.set_ylabel(str(y1_cell), color=color)
                    ax1.tick_params(axis='y')
                    
                    plt.grid(b=True, which='major', color='#666666', linestyle='--')
                    plt.minorticks_on()
                    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                    plt.show()
                    
                
                
                if int(len(self.table_widget.selectionModel().selectedRows()))==2:
                   #retreive cell names
                    x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                    y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                    
               
                    x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                    y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                   
              
               #Retrieve Graph 1 Variables from cell names
                    x1=np.array(df[str(x1_cell)])
                    y1=np.array(df[str(y1_cell)])
                    
               
               #Retrieve Graph 2 Variables from cell names
                    x2=np.array(df[str(x2_cell)])
                    y2=np.array(df[str(y2_cell)])
                    
               
               #Connect the dots
               
                    s1mask = np.isfinite(y1)
                    
                    
                    s2mask = np.isfinite(y2)
                    
               
               #Main plot create
               
                    color='tab:red'
                    fig, (ax1,ax2) = plt.subplots(2, sharex='col', sharey='row')
               
               #Plot 1 create
               
                    ax1.plot(x1[s1mask],y1[s1mask], color=color)
                    ax1.set_xlabel(str(x1_cell))
                    ax1.set_ylabel(str(y1_cell), color=color)
                    ax1.tick_params(axis='y')
                    
                    ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax1.minorticks_on()
                    ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                  
               
    
               
               #Plot 2 create
        
                    color='tab:red'
             
                    ax2.plot(x2[s1mask],y2[s2mask], color=color)
                    ax2.set_xlabel(str(x2_cell))
                    ax2.set_ylabel(str(y2_cell), color=color)
                    ax2.tick_params(axis='y')
                    
                    ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax2.minorticks_on()
                    ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    
                    plt.show()
                 
                if int(len(self.table_widget.selectionModel().selectedRows()))==3:
                   #retreive cell names
                    x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                    y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                   
               
                    x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                    y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                   
                    
                    x3_cell = self.getsamerowcell_3(self.table_widget, "Var x-axis")
                    y3_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-1")
                   
              
               #Retrieve Graph 1 Variables from cell names
                    x1=np.array(df[str(x1_cell)])
                    y1=np.array(df[str(y1_cell)])
                    
               
               #Retrieve Graph 2 Variables from cell names
                    x2=np.array(df[str(x2_cell)])
                    y2=np.array(df[str(y2_cell)])
                   
                    
                    x3=np.array(df[str(x3_cell)])
                    y3=np.array(df[str(y3_cell)])
                   
               
               #Connect the dots
               
                    s1mask = np.isfinite(y1)
                    
                    
                    s2mask = np.isfinite(y2)
                   
                    
                    s3mask = np.isfinite(y3)
                   
               
               #Main plot create
               
                    color='tab:red'
                    fig, (ax1,ax2,ax3) = plt.subplots(3, sharex='col', sharey='row')
               
               #Plot 1 create
               
                    ax1.plot(x1[s1mask],y1[s1mask], color=color)
                    ax1.set_xlabel(str(x1_cell))
                    ax1.set_ylabel(str(y1_cell), color=color)
                    ax1.tick_params(axis='y')
                    
                    ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax1.minorticks_on()
                    ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                   
               
               #Plot 2 create
        
                    color='tab:red'
             
                    ax2.plot(x2[s1mask],y2[s2mask], color=color)
                    ax2.set_xlabel(str(x2_cell))
                    ax2.set_ylabel(str(y2_cell), color=color)
                    ax2.tick_params(axis='y')
                    
                    ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax2.minorticks_on()
                    ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                
              #Plot 2 create
        
                    color='tab:red'
             
                    ax3.plot(x3[s1mask],y3[s3mask], color=color)
                    ax3.set_xlabel(str(x3_cell))
                    ax3.set_ylabel(str(y3_cell), color=color)
                    ax3.tick_params(axis='y')
                    
                    ax3.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax3.minorticks_on()
                    ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    plt.show()
                    
                    
                if int(len(self.table_widget.selectionModel().selectedRows()))==4:
                   #retreive cell names
                    x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                    y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                   
               
                    x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                    y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                    
                    
                    x3_cell = self.getsamerowcell_3(self.table_widget, "Var x-axis")
                    y3_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-1")
                    
                    
                    x4_cell = self.getsamerowcell_4(self.table_widget, "Var x-axis")
                    y4_cell = self.getsamerowcell_4(self.table_widget, "Var y-axis-1")
              
               #Retrieve Graph 1 Variables from cell names
                    x1=np.array(df[str(x1_cell)])
                    y1=np.array(df[str(y1_cell)])
                    
               
               #Retrieve Graph 2 Variables from cell names
                    x2=np.array(df[str(x2_cell)])
                    y2=np.array(df[str(y2_cell)])
                   
                    
                    x3=np.array(df[str(x3_cell)])
                    y3=np.array(df[str(y3_cell)])
                    
               #Retrieve Graph 4 Variables from cell names
                    x4=np.array(df[str(x4_cell)])
                    y4=np.array(df[str(y4_cell)])
               
               #Connect the dots
               
                    s1mask = np.isfinite(y1)
                    
                    s2mask = np.isfinite(y2)
                    
                    s3mask = np.isfinite(y3)
                    
                    s4mask = np.isfinite(y4)
               
               #Main plot create
               
                    color='tab:red'
                    fig, (ax1,ax2,ax3,ax4) = plt.subplots(4, sharex='col', sharey='row')
               
               #Plot 1 create
               
                    ax1.plot(x1[s1mask],y1[s1mask], color=color)
                    ax1.set_xlabel(str(x1_cell))
                    ax1.set_ylabel(str(y1_cell), color=color)
                    ax1.tick_params(axis='y')
                    
                    ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax1.minorticks_on()
                    ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    
               
               #Plot 2 create
        
                    color='tab:red'
             
                    ax2.plot(x2[s1mask],y2[s2mask], color=color)
                    ax2.set_xlabel(str(x2_cell))
                    ax2.set_ylabel(str(y2_cell), color=color)
                    ax2.tick_params(axis='y')
                    
                    ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax2.minorticks_on()
                    ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    
                
                
              #Plot 3 create
        
                    color='tab:red'
             
                    ax3.plot(x3[s1mask],y3[s3mask], color=color)
                    ax3.set_xlabel(str(x3_cell))
                    ax3.set_ylabel(str(y3_cell), color=color)
                    ax3.tick_params(axis='y')
                    
                    ax3.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax3.minorticks_on()
                    ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
            
                    
                    
                #Plot 4 create
        
                    color='tab:red'
             
                    ax4.plot(x4[s1mask],y4[s4mask], color=color)
                    ax4.set_xlabel(str(x4_cell))
                    ax4.set_ylabel(str(y4_cell), color=color)
                    ax4.tick_params(axis='y')
                    
                    ax4.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax4.minorticks_on()
                    ax4.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                     #create second set of y axis for fourth graph
               
                
                    plt.show()
            if self.Cont_Y.isChecked() == True:
                if self.combo_box.currentText() == "2":
                    if int(len(self.table_widget.selectionModel().selectedRows()))==1:
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                        y1a_cell = self.getsamerowcell(self.table_widget, "Var y-axis-2")
                    
                     #Retrieve Graph 1 Variables from cell names
                        x1=df[str(x1_cell)]
                        y1=df[str(y1_cell)]
                        y1a=df[str(y1a_cell)]
                    #make continuous line from broken data
                        
               
                        color='tab:red'
                        fig, (ax1) = plt.subplots(1, sharex='col', sharey='row')
               
                    #Plot 1 create
               
                        ax1.plot(x1,y1, label= str(y1_cell), color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel("Kg", color=color)
                        ax1.tick_params(axis='y')
                        
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                        
                        
                   
                        color='tab:blue'
                        ax1.plot(x1,y1a, label= str(y1a_cell), color=color)
                        
                        
                        ax1.legend(loc = "upper right")
                        plt
                        
                    
                        
                        plt.show()
                    
                    
                    if int(len(self.table_widget.selectionModel().selectedRows()))==2:
                       #retreive cell names
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                        y1a_cell = self.getsamerowcell(self.table_widget, "Var y-axis-2")
                   
                        x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                        y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                        y2a_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-2")
                  
                   #Retrieve Graph 1 Variables from cell names
                        x1=df[str(x1_cell)]
                        y1=df[str(y1_cell)]
                        y1a=df[str(y1a_cell)]
                   
                   #Retrieve Graph 2 Variables from cell names
                        x2=df[str(x2_cell)]
                        y2=df[str(y2_cell)]
                        y2a=df[str(y2a_cell)]
                   
                   #Connect the dots
                   
                        
                   
                   #Main plot create
                   
                        color='tab:red'
                        fig, (ax1,ax2) = plt.subplots(2, sharex='col', sharey='row')
                   
                   #Plot 1 create
                   
                        ax1.plot(x1,y1, label= str(y1_cell), color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel(str("Kg"), color=color)
                        ax1.tick_params(axis='y')
                        
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        
                        ax1.plot(x1,y1a,label= str(y1a_cell), color=color)
                        ax1.legend(loc = "upper right")
                        plt.show()
                   
                   #Plot 2 create
            
                        color='tab:red'
                 
                        ax2.plot(x2,y2, label= str(y2_cell), color=color)
                        ax2.set_xlabel(str(x2_cell))
                        ax2.set_ylabel("Kg", color=color)
                        ax2.tick_params(axis='y')
                        
                        ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax2.minorticks_on()
                        ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        ax2.plot(x2,y2a,label= str(y2a_cell), color=color)
                        ax2.legend(loc = "upper right")
                        plt.show()
                     
                    if int(len(self.table_widget.selectionModel().selectedRows()))==3:
                       #retreive cell names
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                        y1a_cell = self.getsamerowcell(self.table_widget, "Var y-axis-2")
                   
                        x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                        y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                        y2a_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-2")
                        
                        x3_cell = self.getsamerowcell_3(self.table_widget, "Var x-axis")
                        y3_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-1")
                        y3a_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-2")
                  
                   #Retrieve Graph 1 Variables from cell names
                        x1=df[str(x1_cell)]
                        y1=df[str(y1_cell)]
                        y1a=df[str(y1a_cell)]
                   
                   #Retrieve Graph 2 Variables from cell names
                        x2=df[str(x2_cell)]
                        y2=df[str(y2_cell)]
                        y2a=df[str(y2a_cell)]
                        
                        x3=df[str(x3_cell)]
                        y3=df[str(y3_cell)]
                        y3a=df[str(y3a_cell)]
                   
                   #Connect the dots
                   
                        
                   
                   #Main plot create
                   
                        color='tab:red'
                        fig, (ax1,ax2,ax3) = plt.subplots(3, sharex='col', sharey='row')
                   
                   #Plot 1 create
                   
                        ax1.plot(x1,y1, label= str(y1_cell), color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel("Kg", color=color)
                        ax1.tick_params(axis='y')
                        
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        ax1.plot(x1,y1a,label= str(y1a_cell), color=color)
                        ax1.legend(loc = "upper right")
                        plt.show()
                        
                        
                   
                   #Plot 2 create
            
                        color='tab:red'
                 
                        ax2.plot(x2,y2,label= str(y2_cell), color = color)
                        ax2.set_xlabel(str(x2_cell))
                        ax2.set_ylabel("Kg", color=color)
                        ax2.tick_params(axis='y')
                        
                        ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax2.minorticks_on()
                        ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                        ax2a=ax2.twinx() #create second set of y axis for second graph
                   
                        color='tab:blue'
                   
                        ax2.plot(x2,y2a, label= str(y2a_cell), color=color)
                        ax2a.set_ylabel(str(y2a_cell), color=color)
                        ax2.legend(loc = "upper right")
                        plt.show()
                    
                  #Plot 3 create
            
                        color='tab:red'
                 
                        ax3.plot(x3,y3, label= str(y3_cell), color=color)
                        ax3.set_xlabel(str(x3_cell))
                        ax3.set_ylabel("Kg", color=color)
                        ax3.tick_params(axis='y')
                        
                        ax3.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax3.minorticks_on()
                        ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        ax3.plot(x3,y3a, label= str(y3a_cell), color=color)
                        ax3.legend(loc = "upper right")
                        plt.show()
                        
                        
                    if int(len(self.table_widget.selectionModel().selectedRows()))==4:
                       #retreive cell names
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                        y1a_cell = self.getsamerowcell(self.table_widget, "Var y-axis-2")
                   
                        x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                        y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                        y2a_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-2")
                        
                        x3_cell = self.getsamerowcell_3(self.table_widget, "Var x-axis")
                        y3_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-1")
                        y3a_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-2")
                        
                        x4_cell = self.getsamerowcell_4(self.table_widget, "Var x-axis")
                        y4_cell = self.getsamerowcell_4(self.table_widget, "Var y-axis-1")
                        y4a_cell = self.getsamerowcell_4(self.table_widget, "Var y-axis-2")
                  
                   #Retrieve Graph 1 Variables from cell names
                        x1=df[str(x1_cell)]
                        y1=df[str(y1_cell)]
                        y1a=df[str(y1a_cell)]
                   
                   #Retrieve Graph 2 Variables from cell names
                        x2=df[str(x2_cell)]
                        y2=df[str(y2_cell)]
                        y2a=df[str(y2a_cell)]
                        
                   #Retrieve Graph 3 Variables from cell names
                        x3=df[str(x3_cell)]
                        y3=df[str(y3_cell)]
                        y3a=df[str(y3a_cell)]
                        
                   #Retrieve Graph 4 Variables from cell names
                        x4=df[str(x4_cell)]
                        y4=df[str(y4_cell)]
                        y4a=df[str(y4a_cell)]
                   
                   #Connect the dots
                   
                       
                   
                   #Main plot create
                   
                        color='tab:red'
                        fig, (ax1,ax2,ax3,ax4) = plt.subplots(4, sharex='col', sharey='row')
                   
                   #Plot 1 create
                   
                        ax1.plot(x1,y1, label= str(y1_cell), color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel("Kg", color=color)
                        ax1.tick_params(axis='y')
                   
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                        
                        
                   
                        color='tab:blue'
                   
                        ax1.plot(x1,y1a,label= str(y1a_cell), color=color)
                        ax1.legend(loc = "upper right")
                        plt.show()
                   
                   #Plot 2 create
            
                        color='tab:red'
                 
                        ax2.plot(x2,y2,label= str(y2_cell), color=color)
                        ax2.set_xlabel(str(x2_cell))
                        ax2.set_ylabel("Kg", color=color)
                        ax2.tick_params(axis='y')
                        
                        ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax2.minorticks_on()
                        ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                                  
                        color='tab:blue'
                   
                        ax2.plot(x2,y2a,label= str(y2a_cell), color=color)
                        ax2.legend(loc = "upper right")
                        plt.show()
                    
                    
                  #Plot 3 create
            
                        color='tab:red'
                 
                        ax3.plot(x3,y3, label= str(y3_cell), color=color)
                        ax3.set_xlabel(str(x3_cell))
                        ax3.set_ylabel("Kg", color=color)
                        ax3.tick_params(axis='y')
                        
                        ax3.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax3.minorticks_on()
                        ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        ax3.plot(x3,y3a, label= str(y3a_cell), color=color)
                        ax3.legend(loc = "upper right")
                        plt.show()
                        
                        
                    #Plot 4 create
            
                        color='tab:red'
                 
                        ax4.plot(x4,y4,label= str(y4_cell), color=color)
                        ax4.set_xlabel(str(x4_cell))
                        ax4.set_ylabel("Kg", color=color)
                        ax4.tick_params(axis='y')
                        
                        ax4.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax4.minorticks_on()
                        ax4.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                   
                        color='tab:blue'
                   
                        ax4.plot(x4,y4a, label= str(y4a_cell), color=color)
                        ax4.legend(loc = "upper right")
                        plt.show()
                        
                        
                if self.combo_box.currentText() == "1":
                    if int(len(self.table_widget.selectionModel().selectedRows()))==1:
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                        
                    
                     #Retrieve Graph 1 Variables from cell names
                        
                        x1=np.array(df[str(x1_cell)])
                        y1=np.array(df[str(y1_cell)])
                        
                 
                        
                    
                        
                        
               
                        color='tab:red'
                        fig, (ax1) = plt.subplots(1, sharex='col', sharey='row')
               
                    #Plot 1 create
               
                        ax1.plot(x1,y1, color=color)
                        ax1.set_xlim([np.nanmin(x1), np.nanmax(x1)])
                        ax1.set_ylim([np.nanmin(y1), np.nanmax(y1)])
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel(str(y1_cell), color=color)
                        ax1.tick_params(axis='y')
                        
                        plt.grid(b=True, which='major', color='#666666', linestyle='--')
                        plt.minorticks_on()
                        plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                        plt.show()
                        
                    
                    
                    if int(len(self.table_widget.selectionModel().selectedRows()))==2:
                       #retreive cell names
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                        
                   
                        x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                        y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                       
                  
                   #Retrieve Graph 1 Variables from cell names
                        x1=np.array(df[str(x1_cell)])
                        y1=np.array(df[str(y1_cell)])
                        
                   
                   #Retrieve Graph 2 Variables from cell names
                        x2=np.array(df[str(x2_cell)])
                        y2=np.array(df[str(y2_cell)])
                        
                   
                   #Connect the dots
                   
                        
                        
                   
                   #Main plot create
                   
                        color='tab:red'
                        fig, (ax1,ax2) = plt.subplots(2, sharex='col', sharey='row')
                   
                   #Plot 1 create
                   
                        ax1.plot(x1,y1, color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel(str(y1_cell), color=color)
                        ax1.tick_params(axis='y')
                        
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                      
                   
        
                   
                   #Plot 2 create
            
                        color='tab:red'
                 
                        ax2.plot(x2,y2, color=color)
                        ax2.set_xlabel(str(x2_cell))
                        ax2.set_ylabel(str(y2_cell), color=color)
                        ax2.tick_params(axis='y')
                        
                        ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax2.minorticks_on()
                        ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                        
                        plt.show()
                     
                    if int(len(self.table_widget.selectionModel().selectedRows()))==3:
                       #retreive cell names
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                       
                   
                        x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                        y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                       
                        
                        x3_cell = self.getsamerowcell_3(self.table_widget, "Var x-axis")
                        y3_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-1")
                       
                  
                   #Retrieve Graph 1 Variables from cell names
                        x1=np.array(df[str(x1_cell)])
                        y1=np.array(df[str(y1_cell)])
                        
                   
                   #Retrieve Graph 2 Variables from cell names
                        x2=np.array(df[str(x2_cell)])
                        y2=np.array(df[str(y2_cell)])
                       
                        
                        x3=np.array(df[str(x3_cell)])
                        y3=np.array(df[str(y3_cell)])
                       
                   
                   #Connect the dots
                   
                        
                       
                   
                   #Main plot create
                   
                        color='tab:red'
                        fig, (ax1,ax2,ax3) = plt.subplots(3, sharex='col', sharey='row')
                   
                   #Plot 1 create
                   
                        ax1.plot(x1,y1, color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel(str(y1_cell), color=color)
                        ax1.tick_params(axis='y')
                        
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                       
                   
                   #Plot 2 create
            
                        color='tab:red'
                 
                        ax2.plot(x2,y2, color=color)
                        ax2.set_xlabel(str(x2_cell))
                        ax2.set_ylabel(str(y2_cell), color=color)
                        ax2.tick_params(axis='y')
                        
                        ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax2.minorticks_on()
                        ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                    
                  #Plot 3 create
            
                        color='tab:red'
                 
                        ax3.plot(x3,y3, color=color)
                        ax3.set_xlabel(str(x3_cell))
                        ax3.set_ylabel(str(y3_cell), color=color)
                        ax3.tick_params(axis='y')
                        
                        ax3.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax3.minorticks_on()
                        ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                        plt.show()
                        
                        
                    if int(len(self.table_widget.selectionModel().selectedRows()))==4:
                       #retreive cell names
                        x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                        y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                       
                   
                        x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                        y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                        
                        
                        x3_cell = self.getsamerowcell_3(self.table_widget, "Var x-axis")
                        y3_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-1")
                        
                        
                        x4_cell = self.getsamerowcell_4(self.table_widget, "Var x-axis")
                        y4_cell = self.getsamerowcell_4(self.table_widget, "Var y-axis-1")
                  
                   #Retrieve Graph 1 Variables from cell names
                        x1=np.array(df[str(x1_cell)])
                        y1=np.array(df[str(y1_cell)])
                        
                   
                   #Retrieve Graph 2 Variables from cell names
                        x2=np.array(df[str(x2_cell)])
                        y2=np.array(df[str(y2_cell)])
                       
                        
                        x3=np.array(df[str(x3_cell)])
                        y3=np.array(df[str(y3_cell)])
                        
                   #Retrieve Graph 4 Variables from cell names
                        x4=np.array(df[str(x4_cell)])
                        y4=np.array(df[str(y4_cell)])
                   
                   #Connect the dots
                   
                        
                   
                   #Main plot create
                   
                        color='tab:red'
                        fig, (ax1,ax2,ax3,ax4) = plt.subplots(4, sharex='col', sharey='row')
                   
                   #Plot 1 create
                   
                        ax1.plot(x1,y1, color=color)
                        ax1.set_xlabel(str(x1_cell))
                        ax1.set_ylabel(str(y1_cell), color=color)
                        ax1.tick_params(axis='y')
                        
                        ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax1.minorticks_on()
                        ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                        
                   
                   #Plot 2 create
            
                        color='tab:red'
                 
                        ax2.plot(x2,y2, color=color)
                        ax2.set_xlabel(str(x2_cell))
                        ax2.set_ylabel(str(y2_cell), color=color)
                        ax2.tick_params(axis='y')
                        
                        ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax2.minorticks_on()
                        ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                        
                    
                    
                  #Plot 3 create
            
                        color='tab:red'
                 
                        ax3.plot(x3,y3, color=color)
                        ax3.set_xlabel(str(x3_cell))
                        ax3.set_ylabel(str(y3_cell), color=color)
                        ax3.tick_params(axis='y')
                        
                        ax3.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax3.minorticks_on()
                        ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                
                        
                        
                    #Plot 4 create
            
                        color='tab:red'
                 
                        ax4.plot(x4,y4, color=color)
                        ax4.set_xlabel(str(x4_cell))
                        ax4.set_ylabel(str(y4_cell), color=color)
                        ax4.tick_params(axis='y')
                        
                        ax4.grid(b=True, which='major', color='#666666', linestyle='--')
                        ax4.minorticks_on()
                        ax4.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                   
                         #create second set of y axis for fourth graph
                   
                    
                        plt.show()
        if self.Cont_X.isChecked() == False:

                
                
            if self.combo_box.currentText() == "1":
                if int(len(self.table_widget.selectionModel().selectedRows()))==1:
                    x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                    y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                    
                
                 #Retrieve Graph 1 Variables from cell names
                    
                    xtemp1=np.array(df[str(x1_cell)])
                    ytemp1=np.array(df[str(y1_cell)])
                    
                    x1=xtemp1[~np.isnan(xtemp1)]
                    y1=ytemp1[~np.isnan(ytemp1)]
                    
                
                    s1mask = np.isfinite(y1)
                    
           
                    color='tab:red'
                    fig, (ax1) = plt.subplots(1, sharey='row')
           
                #Plot 1 create
           
                    ax1.plot(x1[s1mask],y1[s1mask], color=color)
                    ax1.set_xlim([min(x1), max(x1)])
                    ax1.set_ylim([min(y1), max(y1)])
                    ax1.set_xlabel(str(x1_cell))
                    ax1.set_ylabel(str(y1_cell), color=color)
                    ax1.tick_params(axis='y')
                    
                    plt.grid(b=True, which='major', color='#666666', linestyle='--')
                    plt.minorticks_on()
                    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                    plt.show()
                    
                
                
                if int(len(self.table_widget.selectionModel().selectedRows()))==2:
                   #retreive cell names
                    x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                    y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                    
               
                    x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                    y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                   
              
               #Retrieve Graph 1 Variables from cell names
                    xtemp1=np.array(df[str(x1_cell)])
                    ytemp1=np.array(df[str(y1_cell)])
                    
               
               #Retrieve Graph 2 Variables from cell names
                    xtemp2=np.array(df[str(x2_cell)])
                    ytemp2=np.array(df[str(y2_cell)])
                    
               #remove nan from arrays
                    x1=xtemp1[~np.isnan(xtemp1)]
                    y1=ytemp1[~np.isnan(ytemp1)]
                    
                    
                    x2=xtemp2[~np.isnan(xtemp2)]
                    y2=ytemp2[~np.isnan(ytemp2)]
                    
               
               #Connect the dots
               
                    s1mask = np.isfinite(y1)
                    
                    
                    s2mask = np.isfinite(y2)
                    
               
               #Main plot create
               
                    color='tab:red'
                    fig, (ax1,ax2) = plt.subplots(2, sharey='row')
               
               #Plot 1 create
               
                    ax1.plot(x1[s1mask],y1[s1mask], color=color)
                    ax1.set_xlim([min(x1), max(x1)])
                    ax1.set_ylim([min(y1), max(y1)])
                    ax1.set_xlabel(str(x1_cell))
                    ax1.set_ylabel(str(y1_cell), color=color)
                    ax1.tick_params(axis='y')
                    
                    ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax1.minorticks_on()
                    ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
                    
                    plt.show()
    
               
               #Plot 2 create
        
                    color='tab:red'
             
                    ax2.plot(x2[s1mask],y2[s2mask], color=color)
                    ax2.set_xlim([min(x2), max(x2)])
                    ax2.set_ylim([min(y2), max(y2)])
                    ax2.set_xlabel(str(x2_cell))
                    ax2.set_ylabel(str(y2_cell), color=color)
                    ax2.tick_params(axis='y')
                    
                    ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax2.minorticks_on()
                    ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    
                    plt.show()
                 
                if int(len(self.table_widget.selectionModel().selectedRows()))==3:
                   #retreive cell names
                    x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                    y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                   
               
                    x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                    y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                   
                    
                    x3_cell = self.getsamerowcell_3(self.table_widget, "Var x-axis")
                    y3_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-1")
                   
              
               #Retrieve Graph 1 Variables from cell names
                    xtemp1=np.array(df[str(x1_cell)])
                    ytemp1=np.array(df[str(y1_cell)])
                    
               
               #Retrieve Graph 2 Variables from cell names
                    xtemp2=np.array(df[str(x2_cell)])
                    ytemp2=np.array(df[str(y2_cell)])
                   
                    
                    xtemp3=np.array(df[str(x3_cell)])
                    ytemp3=np.array(df[str(y3_cell)])
              
                #remove nan values    
                    
                    x1=xtemp1[~np.isnan(xtemp1)]
                    y1=ytemp1[~np.isnan(ytemp1)]
                    
                    
                    x2=xtemp2[~np.isnan(xtemp2)]
                    y2=ytemp2[~np.isnan(ytemp2)]
                   
                    
                    x3=xtemp3[~np.isnan(xtemp3)]
                    y3=ytemp3[~np.isnan(ytemp3)]
               
               #Connect the dots
               
                    s1mask = np.isfinite(y1)
                    
                    
                    s2mask = np.isfinite(y2)
                   
                    
                    s3mask = np.isfinite(y3)
                   
               
               #Main plot create
               
                    color='tab:red'
                    fig, (ax1,ax2,ax3) = plt.subplots(3, sharey='row')
               
               #Plot 1 create
               
                    ax1.plot(x1[s1mask],y1[s1mask], color=color)
                    ax1.set_xlim([min(x1), max(x1)])
                    ax1.set_ylim([min(y1), max(y1)])
                    ax1.set_xlabel(str(x1_cell))
                    ax1.set_ylabel(str(y1_cell), color=color)
                    ax1.tick_params(axis='y')
                    
                    ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax1.minorticks_on()
                    ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    plt.show()
               
               #Plot 2 create
        
                    color='tab:red'
             
                    ax2.plot(x2[s1mask],y2[s2mask], color=color)
                    ax2.set_xlim([min(x2), max(x2)])
                    ax2.set_ylim([min(y2), max(y2)])
                    ax2.set_xlabel(str(x2_cell))
                    ax2.set_ylabel(str(y2_cell), color=color)
                    ax2.tick_params(axis='y')
                    
                    ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax2.minorticks_on()
                    ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    plt.show()
              #Plot 2 create
        
                    color='tab:red'
             
                    ax3.plot(x3[s1mask],y3[s3mask], color=color)
                    ax3.set_xlim([min(x3), max(x3)])
                    ax3.set_ylim([min(y3), max(y3)])
                    ax3.set_xlabel(str(x3_cell))
                    ax3.set_ylabel(str(y3_cell), color=color)
                    ax3.tick_params(axis='y')
                    
                    ax3.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax3.minorticks_on()
                    ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    plt.show()
                    
                    
                if int(len(self.table_widget.selectionModel().selectedRows()))==4:
                   #retreive cell names
                    x1_cell = self.getsamerowcell(self.table_widget, "Var x-axis")
                    y1_cell = self.getsamerowcell(self.table_widget, "Var y-axis-1")
                   
               
                    x2_cell = self.getsamerowcell_2(self.table_widget, "Var x-axis")
                    y2_cell = self.getsamerowcell_2(self.table_widget, "Var y-axis-1")
                    
                    
                    x3_cell = self.getsamerowcell_3(self.table_widget, "Var x-axis")
                    y3_cell = self.getsamerowcell_3(self.table_widget, "Var y-axis-1")
                    
                    
                    x4_cell = self.getsamerowcell_4(self.table_widget, "Var x-axis")
                    y4_cell = self.getsamerowcell_4(self.table_widget, "Var y-axis-1")
              
               #Retrieve Graph 1 Variables from cell names
                    x1=np.array(df[str(x1_cell)])
                    y1=np.array(df[str(y1_cell)])
                    
               
               #Retrieve Graph 1 Variables from cell names
                    xtemp1=np.array(df[str(x1_cell)])
                    ytemp1=np.array(df[str(y1_cell)])
                    
               
               #Retrieve Graph 2 Variables from cell names
                    xtemp2=np.array(df[str(x2_cell)])
                    ytemp2=np.array(df[str(y2_cell)])
                   
                    
                    xtemp3=np.array(df[str(x3_cell)])
                    ytemp3=np.array(df[str(y3_cell)])
                    
                    xtemp4=np.array(df[str(x4_cell)])
                    ytemp4=np.array(df[str(y4_cell)])
              
                #remove nan values    
                    
                    x1=xtemp1[~np.isnan(xtemp1)]
                    y1=ytemp1[~np.isnan(ytemp1)]
                    
                    
                    x2=xtemp2[~np.isnan(xtemp2)]
                    y2=ytemp2[~np.isnan(ytemp2)]
                   
                    
                    x3=xtemp3[~np.isnan(xtemp3)]
                    y3=ytemp3[~np.isnan(ytemp3)]
                    
                    
                    x4=xtemp4[~np.isnan(xtemp4)]
                    y4=ytemp4[~np.isnan(ytemp4)]
               
               
               #Connect the dots
               
                    s1mask = np.isfinite(y1)
                    
                    s2mask = np.isfinite(y2)
                    
                    s3mask = np.isfinite(y3)
                    
                    s4mask = np.isfinite(y4)
               
               #Main plot create
               
                    color='tab:red'
                    fig, (ax1,ax2,ax3,ax4) = plt.subplots(4, sharey='row')
               
               #Plot 1 create
               
                    ax1.plot(x1[s1mask],y1[s1mask], color=color)
                    ax1.set_xlim([min(x1), max(x1)])
                    ax1.set_ylim([min(y1), max(y1)])
                    ax1.set_xlabel(str(x1_cell))
                    ax1.set_ylabel(str(y1_cell), color=color)
                    ax1.tick_params(axis='y')
                    
                    ax1.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax1.minorticks_on()
                    ax1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    plt.show()
               
               #Plot 2 create
        
                    color='tab:red'
             
                    ax2.plot(x2[s1mask],y2[s2mask], color=color)
                    ax2.set_xlim([min(x2), max(x2)])
                    ax2.set_ylim([min(y2), max(y2)])
                    ax2.set_xlabel(str(x2_cell))
                    ax2.set_ylabel(str(y2_cell), color=color)
                    ax2.tick_params(axis='y')
                    
                    ax2.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax2.minorticks_on()
                    ax2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    plt.show()
                
                
              #Plot 3 create
        
                    color='tab:red'
             
                    ax3.plot(x3[s1mask],y3[s3mask], color=color)
                    ax3.set_xlim([min(x3), max(x3)])
                    ax3.set_ylim([min(y3), max(y3)])
                    ax3.set_xlabel(str(x3_cell))
                    ax3.set_ylabel(str(y3_cell), color=color)
                    ax3.tick_params(axis='y')
                    
                    ax3.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax3.minorticks_on()
                    ax3.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    plt.show()
                    
                    
                #Plot 4 create
        
                    color='tab:red'
             
                    ax4.plot(x4[s1mask],y4[s4mask], color=color)
                    ax4.set_xlim([min(x4), max(x4)])
                    ax4.set_ylim([min(y4), max(y4)])
                    ax4.set_xlabel(str(x4_cell))
                    ax4.set_ylabel(str(y4_cell), color=color)
                    ax4.tick_params(axis='y')
                    
                    ax4.grid(b=True, which='major', color='#666666', linestyle='--')
                    ax4.minorticks_on()
                    ax4.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
               
                    plt.show()
        

        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
