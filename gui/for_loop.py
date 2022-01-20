# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'for_loop.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_for_loop_config(object):
    def setupUi(self, for_loop_config):
        for_loop_config.setObjectName("for_loop_config")
        for_loop_config.resize(380, 476)
        self.gridLayout = QtWidgets.QGridLayout(for_loop_config)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_add_point = QtWidgets.QPushButton(for_loop_config)
        self.pushButton_add_point.setMinimumSize(QtCore.QSize(30, 23))
        self.pushButton_add_point.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_add_point.setObjectName("pushButton_add_point")
        self.gridLayout.addWidget(self.pushButton_add_point, 1, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(for_loop_config)
        self.label_9.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 1, 2, 1, 1)
        self.pushButton_del_point = QtWidgets.QPushButton(for_loop_config)
        self.pushButton_del_point.setMinimumSize(QtCore.QSize(30, 23))
        self.pushButton_del_point.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_del_point.setObjectName("pushButton_del_point")
        self.gridLayout.addWidget(self.pushButton_del_point, 1, 4, 1, 1)
        self.comboBox_loop_type = QtWidgets.QComboBox(for_loop_config)
        self.comboBox_loop_type.setMinimumSize(QtCore.QSize(135, 0))
        self.comboBox_loop_type.setObjectName("comboBox_loop_type")
        self.comboBox_loop_type.addItem("")
        self.comboBox_loop_type.addItem("")
        self.comboBox_loop_type.addItem("")
        self.comboBox_loop_type.addItem("")
        self.comboBox_loop_type.addItem("")
        self.gridLayout.addWidget(self.comboBox_loop_type, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(for_loop_config)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.path_line_button = Path_Button_Edit(for_loop_config)
        self.path_line_button.setMinimumSize(QtCore.QSize(0, 30))
        self.path_line_button.setObjectName("path_line_button")
        self.gridLayout.addWidget(self.path_line_button, 5, 0, 1, 2)
        self.sweep_widget = QtWidgets.QWidget(for_loop_config)
        self.sweep_widget.setObjectName("sweep_widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.sweep_widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_max = QtWidgets.QLabel(self.sweep_widget)
        self.label_max.setObjectName("label_max")
        self.gridLayout_2.addWidget(self.label_max, 5, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.lineEdit_max = Variable_Box(self.sweep_widget)
        self.lineEdit_max.setObjectName("lineEdit_max")
        self.gridLayout_2.addWidget(self.lineEdit_max, 6, 1, 1, 1)
        self.lineEdit_point_distance = Variable_Box(self.sweep_widget)
        self.lineEdit_point_distance.setObjectName("lineEdit_point_distance")
        self.gridLayout_2.addWidget(self.lineEdit_point_distance, 9, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.sweep_widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 1, 1, 1)
        self.lineEdit_stop = Variable_Box(self.sweep_widget)
        self.lineEdit_stop.setObjectName("lineEdit_stop")
        self.gridLayout_2.addWidget(self.lineEdit_stop, 4, 1, 1, 1)
        self.label_min = QtWidgets.QLabel(self.sweep_widget)
        self.label_min.setObjectName("label_min")
        self.gridLayout_2.addWidget(self.label_min, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.sweep_widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.sweep_widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)
        self.lineEdit_start = Variable_Box(self.sweep_widget)
        self.lineEdit_start.setObjectName("lineEdit_start")
        self.gridLayout_2.addWidget(self.lineEdit_start, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.sweep_widget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 7, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 11, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.sweep_widget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 7, 0, 1, 1)
        self.comboBox_sweep_mode = QtWidgets.QComboBox(self.sweep_widget)
        self.comboBox_sweep_mode.setObjectName("comboBox_sweep_mode")
        self.comboBox_sweep_mode.addItem("")
        self.comboBox_sweep_mode.addItem("")
        self.comboBox_sweep_mode.addItem("")
        self.comboBox_sweep_mode.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_sweep_mode, 1, 1, 1, 1)
        self.lineEdit_min = Variable_Box(self.sweep_widget)
        self.lineEdit_min.setObjectName("lineEdit_min")
        self.gridLayout_2.addWidget(self.lineEdit_min, 6, 0, 1, 1)
        self.lineEdit_n_points = Variable_Box(self.sweep_widget)
        self.lineEdit_n_points.setObjectName("lineEdit_n_points")
        self.gridLayout_2.addWidget(self.lineEdit_n_points, 9, 0, 1, 1)
        self.checkBox_include_endpoints = QtWidgets.QCheckBox(self.sweep_widget)
        self.checkBox_include_endpoints.setChecked(True)
        self.checkBox_include_endpoints.setObjectName("checkBox_include_endpoints")
        self.gridLayout_2.addWidget(self.checkBox_include_endpoints, 10, 0, 1, 2)
        self.gridLayout.addWidget(self.sweep_widget, 3, 0, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 6, 1, 1, 1)
        self.tableWidget_points = QtWidgets.QTableWidget(for_loop_config)
        self.tableWidget_points.setMaximumSize(QtCore.QSize(150, 16777215))
        self.tableWidget_points.setObjectName("tableWidget_points")
        self.tableWidget_points.setColumnCount(0)
        self.tableWidget_points.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget_points, 2, 2, 5, 3)

        self.retranslateUi(for_loop_config)
        QtCore.QMetaObject.connectSlotsByName(for_loop_config)
        for_loop_config.setTabOrder(self.comboBox_loop_type, self.pushButton_add_point)
        for_loop_config.setTabOrder(self.pushButton_add_point, self.pushButton_del_point)
        for_loop_config.setTabOrder(self.pushButton_del_point, self.comboBox_sweep_mode)
        for_loop_config.setTabOrder(self.comboBox_sweep_mode, self.lineEdit_start)
        for_loop_config.setTabOrder(self.lineEdit_start, self.lineEdit_stop)
        for_loop_config.setTabOrder(self.lineEdit_stop, self.lineEdit_min)
        for_loop_config.setTabOrder(self.lineEdit_min, self.lineEdit_max)
        for_loop_config.setTabOrder(self.lineEdit_max, self.lineEdit_n_points)
        for_loop_config.setTabOrder(self.lineEdit_n_points, self.lineEdit_point_distance)
        for_loop_config.setTabOrder(self.lineEdit_point_distance, self.checkBox_include_endpoints)
        for_loop_config.setTabOrder(self.checkBox_include_endpoints, self.tableWidget_points)

    def retranslateUi(self, for_loop_config):
        _translate = QtCore.QCoreApplication.translate
        for_loop_config.setWindowTitle(_translate("for_loop_config", "Form"))
        self.pushButton_add_point.setText(_translate("for_loop_config", "+"))
        self.label_9.setText(_translate("for_loop_config", "Points:"))
        self.pushButton_del_point.setText(_translate("for_loop_config", "-"))
        self.comboBox_loop_type.setItemText(0, _translate("for_loop_config", "start - stop"))
        self.comboBox_loop_type.setItemText(1, _translate("for_loop_config", "start - min - max - stop"))
        self.comboBox_loop_type.setItemText(2, _translate("for_loop_config", "start - max - min - stop"))
        self.comboBox_loop_type.setItemText(3, _translate("for_loop_config", "Value-List"))
        self.comboBox_loop_type.setItemText(4, _translate("for_loop_config", "Text-File"))
        self.label.setText(_translate("for_loop_config", "Loop-Type:"))
        self.label_max.setText(_translate("for_loop_config", "Max"))
        self.label_3.setText(_translate("for_loop_config", "Stop"))
        self.label_min.setText(_translate("for_loop_config", "Min"))
        self.label_6.setText(_translate("for_loop_config", "Sweep mode"))
        self.label_2.setText(_translate("for_loop_config", "Start"))
        self.label_8.setText(_translate("for_loop_config", "point-distance"))
        self.label_7.setText(_translate("for_loop_config", "# points"))
        self.comboBox_sweep_mode.setItemText(0, _translate("for_loop_config", "linear"))
        self.comboBox_sweep_mode.setItemText(1, _translate("for_loop_config", "logarithmic"))
        self.comboBox_sweep_mode.setItemText(2, _translate("for_loop_config", "exponential"))
        self.comboBox_sweep_mode.setItemText(3, _translate("for_loop_config", "1/x"))
        self.checkBox_include_endpoints.setText(_translate("for_loop_config", "Include end-points"))

from utility.path_button_edit import Path_Button_Edit
from utility.variable_tool_tip_box import Variable_Box
