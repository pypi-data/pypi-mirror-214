import csv
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import pandas as pd
import numpy as np
from PyQt5 import QtCore
import seaborn as sns


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.columns_details=None
        
        self.data=None
        
        self.dataviz= None
        self.table=None
        self.vBox=QVBoxLayout()
        self.file_selector=QPushButton('Pick a csv file')
        self.file_selector.clicked.connect(self.fileSelection)
        self.tabs=QTabWidget()
        self.tab1=QWidget()
        self.tab1.layout=QVBoxLayout(self)
        self.tab1.layout.addWidget(self.file_selector)
        self.tab1.setLayout(self.tab1.layout)
        self.tabs.addTab(self.tab1,"File Selection")
        self.vBox.addWidget(self.tabs)
        self.widget=QWidget()
        self.widget.setLayout(self.vBox)
        self.setCentralWidget(self.widget)

    def contextMenuEvent(self,e):
        right_click_menu=QMenu(self)
        clean_all= right_click_menu.addAction("Save To Csv")
        clean_all.triggered.connect(self.saveToCsv)
        right_click_menu.addSeparator()
        right_click_menu.exec(e.globalPos())


    def saveToCsv(self):
        path=QFileDialog.getSaveFileName()[0]
        try :
            self.pivot_table.empty==False
            self.pivot_table.to_csv(path_or_buf=path)
        except:
            self.data.to_csv(path_or_buf=path)

    def deleteColumns(self):
        
        self.selected_column=self.column_list.currentText()
        self.data=self.data.drop(columns=self.selected_column)
        self.tabs.removeTab(1)
        self.tab2=DataWindow(self.data)
        self.tabs.addTab(self.tab2,"Data Visualization")

    def renameColumns(self):
        self.selected_column=self.column_list.currentText()
    
    def changeName(self):
        self.selected_column=self.column_list.currentText()
        self.new_name=self.change_name.text()
        self.data=self.data.rename(columns={self.selected_column:self.new_name})
    def displayPivotTable(self):
        self.pivot_table=self.data.pivot_table(index=self.column_list_row.currentText(),columns=self.column_list_col.currentText(),values=self.column_list_val.currentText(),aggfunc='sum')
        self.pivot_table=self.pivot_table.reset_index()
        self.dataviz=DataWindow(self.pivot_table)
        self.tab5.layout.addWidget(self.dataviz)
        


    def fileSelection(self): 
        #choix du fichier csv à explorer   
        path = QFileDialog.getOpenFileName()[0]
        if (path and ".csv" in path ): #vérification du choix d'un fichier csv, excel et json pour plus tard
            csv_delimiter=csv.Sniffer().sniff(open(path).readline(),[",",";"])  #utilisation de sniffer pour déterminer le dialect du csv dont particulièrement le délimiteur (entre ,et ;)          
            self.data=pd.read_csv(path,delimiter=csv_delimiter.delimiter)
            columns_header=self.data.columns
            columns_type=self.data.dtypes #détermination des types des données pour limiter les agrégations autorisées sur chaque colonne de la table, pas de somme de dates ou de textes
            columns_details={'columns':columns_header,
                     'type':columns_type}
            self.columns_details=pd.DataFrame(columns_details)
            self.values=pd.concat([self.columns_details.loc[self.columns_details['type'] =="float64",:],self.columns_details.loc[self.columns_details['type'] =="int64",:]])
            self.values=self.values['columns']
            self.tab2 = DataWindow(self.data) #affichage d'un onglet permettant de visualiser le contenu du csv
            self.tabs.addTab(self.tab2,"Data visualization")
            self.tab3=QWidget()
            self.tab3.layout=QVBoxLayout(self)
            self.msg1=QLabel("Delete columns")
            self.msg2=QLabel("Select a column.")
            self.column_list=QComboBox()
            self.column_list.addItems(self.data.columns)
            self.selected_column=self.column_list.currentText()
            self.column_list.currentTextChanged.connect(self.deleteColumns)
            self.tab3.layout.addWidget(self.msg1)
            self.tab3.layout.addWidget(self.msg2)
            self.tab3.layout.addWidget(self.column_list)
            self.tab3.setLayout(self.tab3.layout)
            self.tabs.addTab(self.tab3,"Delete columns")
            self.tab4=QWidget()
            self.tab4.layout=QVBoxLayout(self)
            self.tab4.layout.addWidget(QLabel("Choose the column name to change"))
            self.column_list_changer=QComboBox()
            self.column_list_changer.addItems(self.data.columns)
            self.tab4.layout.addWidget(self.column_list_changer)
            self.tab4.layout.addWidget(QLabel("To be renamed?"))
            self.change_name=QLineEdit()
            self.tab4.layout.addWidget(self.change_name)
            self.submit_name=QPushButton()
            self.submit_name.setText("Confirm name change")
            self.submit_name.clicked.connect(self.changeName)
            self.tab4.layout.addWidget(self.submit_name)
            self.tab4.setLayout(self.tab4.layout)
            self.tabs.addTab(self.tab4,"Rename columns")

            self.tab5=QWidget()
            self.tab5.layout=QVBoxLayout(self)
            self.tab5.layout.addWidget(QLabel("Choose a column to use for rows headers"))
            self.column_list_row=QComboBox()
            self.column_list_row.addItems(self.data.columns)
            self.tab5.layout.addWidget(self.column_list_row)
            self.column_list_col=QComboBox()
            self.column_list_col.addItems(self.data.columns)
            self.tab5.layout.addWidget(QLabel("Choose a column to use for columns headers"))
            self.tab5.layout.addWidget(self.column_list_col)
            self.tab5.layout.addWidget(QLabel("Choose values to aggregate"))
            self.column_list_val=QComboBox()
            self.column_list_val.addItems(self.values)
            self.tab5.layout.addWidget(self.column_list_val)
            self.display_button=QPushButton()
            self.display_button.setText("Click to validate and generate table")
            self.display_button.clicked.connect(self.displayPivotTable)
            self.tab5.layout.addWidget(self.display_button)
            self.tab5.setLayout(self.tab5.layout)
            self.tabs.addTab(self.tab5,"Pivot Table")


            



            
            """
            print(len(columns_details))
            for item in range(len(columns_details)):
                self.rows_vBox.addWidget(Selector('row',columns_details.iat[item,0]))
                self.columns_vBox.addWidget(Selector('column',columns_details.iat[item,0]))
            self.rows_.setLayout(self.rows_vBox)            
            self.columns_.setLayout(self.columns_vBox)
            self.hBox.addWidget(self.rows_)
            self.hBox.addWidget(self.columns_)
            self.selectors.setLayout(self.hBox)
            self.vBox.addWidget(self.selectors)
            """
        else:
            self.vBox.addWidget(QLabel(text="Pick a csv please, this is still an early version"))
            

        """
            snippet de code à adapter pour merge verticalement deux tables
            clé=["Country","Product Type"]
            data_1=data.pivot_table(index=clé,columns="Month",values="Mean selling price",aggfunc=sum)
            data_1=data_1.reset_index()
            data_1['cle']=""
            for i in range(0,len(clé)):
                data_1['cle']+=data_1[clé[i]]
            data_2=data.pivot_table(index=clé,values="Gross sales",aggfunc=sum)
            data_2=data_2.reset_index()
            data_2['cle']=""
            for i in range(0,len(clé)):
                data_2['cle']+=data_2[clé[i]]
                data_2=data_2.drop(columns=clé[i])
            data_1=data_1.merge(data_2,how='outer',on='cle')
            data_1=data_1.drop(columns="cle")
            print(data_1)
        """

class DataWindow(QWidget):
    def __init__(self, data):
        super().__init__()
        layout=QVBoxLayout()
        self.table=QTableWidget()
        columns_labels=data.columns
        nb_row=data.shape[0]
        nb_col=data.shape[1]
        self.table.setRowCount(nb_row)
        self.table.setColumnCount(nb_col)
        self.table.setHorizontalHeaderLabels(columns_labels)

        for row in range(nb_row):
            for col in range(nb_col):
                item=QTableWidgetItem(str(data.iat[row,col]))
                self.table.setItem(row,col,item)
        layout.addWidget(self.table)
        self.setLayout(layout)


"""
App = QApplication(sys.argv)        
w = MainWindow()
w.resize(200,100)
w.setWindowTitle('Analyse data with Python')
w.setWindowFlags(Qt.WindowStaysOnTopHint)
w.show()

sys.exit(App.exec())
"""