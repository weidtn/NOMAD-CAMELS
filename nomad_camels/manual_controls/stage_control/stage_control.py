import time
import numpy as np
from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel, QWidget, QGridLayout, QStyle
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QKeyEvent

from nomad_camels.main_classes.manual_control import Manual_Control, Manual_Control_Config
from nomad_camels.utility import variables_handling, device_handling, number_formatting

from .ui_stage_control import Ui_Form


class Stage_Control(Manual_Control, Ui_Form):
    """ """
    def __init__(self, parent=None, control_data=None):
        control_data = control_data or {}
        if 'name' in control_data:
            name = control_data['name']
        else:
            name = 'Stage Control'
        super().__init__(parent=parent, title=name)
        self.setupUi(self)
        self.setWindowTitle(f'{name} - NOMAD CAMELS')
        self.control_data = control_data

        self.pushButton_up.setIcon(self.style().standardIcon(QStyle.SP_ArrowUp))
        self.pushButton_down.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        self.pushButton_left.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.pushButton_right.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        self.pushButton_zUp.setIcon(self.style().standardIcon(QStyle.SP_ArrowUp))
        self.pushButton_zDown.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        self.pushButton_position.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.pushButton_stop.setIcon(self.style().standardIcon(QStyle.SP_BrowserStop))

        use_x, use_y, use_z = control_data['use_axis']
        self.pushButton_left.setEnabled(use_x)
        self.pushButton_right.setEnabled(use_x)
        self.pushButton_up.setEnabled(use_y)
        self.pushButton_down.setEnabled(use_y)
        self.pushButton_zUp.setEnabled(use_z)
        self.pushButton_zDown.setEnabled(use_z)

        self.pushButton_right.clicked.connect(lambda state=None, axis=0: self.step_axis(axis))
        self.pushButton_left.clicked.connect(lambda state=None, axis=0, u=False: self.step_axis(axis, u))
        self.pushButton_up.clicked.connect(lambda state=None, axis=1: self.step_axis(axis))
        self.pushButton_down.clicked.connect(lambda state=None, axis=1, u=False: self.step_axis(axis, u))
        self.pushButton_zUp.clicked.connect(lambda state=None, axis=2: self.step_axis(axis))
        self.pushButton_zDown.clicked.connect(lambda state=None, axis=2, u=False: self.step_axis(axis, u))

        self.pushButton_ref.clicked.connect(self.reference_drive)
        self.pushButton_stop.clicked.connect(self.stop_moving)

        self.pushButton_position.clicked.connect(self.input_position)
        self.pushButton_go_to.clicked.connect(self.move_to_position)

        self.lines = [self.lineEdit_read_frequ, self.lineEdit_stepX,
                      self.lineEdit_stepY, self.lineEdit_stepZ,
                      self.lineEdit_manualX, self.lineEdit_manualY,
                      self.lineEdit_manualZ, self.lineEdit_goX,
                      self.lineEdit_goY, self.lineEdit_goZ]
        self.line_names = ['read_frequ', 'stepSize_X', 'stepSize_Y',
                          'stepSize_Z', 'manual_X', 'manual_Y',
                          'manual_Z', 'go_to_X', 'go_to_Y',
                          'go_to_Z']
        self.checks = [self.checkBox_refX, self.checkBox_refY,
                       self.checkBox_refZ, self.checkBox_manualActive]
        self.check_names = ['find_ref_X', 'find_ref_Y', 'find_ref_Z',
                           'manual_active']
        if 'read_frequ' not in control_data:
            control_data['read_frequ'] = 0.5
        if 'manual_active' not in control_data:
            control_data['manual_active'] = False

        for i, line in enumerate(self.lines):
            if self.line_names[i] not in control_data:
                control_data[self.line_names[i]] = 0
            line.setText(str(control_data[self.line_names[i]]))
            line.textChanged.connect(self.line_change)
        for i, check in enumerate(self.checks):
            if self.check_names[i] not in control_data:
                control_data[self.check_names[i]] = True
            check.setChecked(control_data[self.check_names[i]])
            check.clicked.connect(self.check_change)

        ax_names = ['X', 'Y', 'Z']
        set_channels = []
        read_channels = []
        ref_functions = []
        stop_functions = []
        manual_functions = []
        for i, use in enumerate(control_data['use_axis']):
            ax = ax_names[i]
            for j, name in enumerate(self.line_names):
                if ax in name:
                    self.lines[j].setEnabled(use)
            for j, name in enumerate(self.check_names):
                if ax in name:
                    self.checks[j].setEnabled(use)
            if not use:
                set_channels.append('None')
                read_channels.append('None')
                ref_functions.append('None')
                stop_functions.append('None')
                manual_functions.append('None')
                continue
            set_channels.append(control_data['axis_channel'][i])
            if control_data['read_axis'][i]:
                read_channels.append(control_data['read_channel'][i])
            else:
                read_channels.append('None')
            ref_functions.append(control_data['axis_ref'][i])
            stop_functions.append(control_data['axis_stop'][i])
            manual_functions.append(control_data['manual_function'][i])

        channels = set(read_channels + set_channels)
        if 'None' in channels:
            channels.remove('None')
        channels = list(channels)
        self.set_channels = set_channels
        self.read_channels = read_channels
        self.ref_funcs = ref_functions
        self.stop_funcs = stop_functions
        self.manual_funcs = manual_functions
        self.read_thread = None
        self.move_thread = None
        self.start_multiple_devices(channels, True)


    def device_ready(self):
        super().device_ready()
        self.set_channels = device_handling.get_channels_from_string_list(self.set_channels)
        self.read_channels = device_handling.get_channels_from_string_list(self.read_channels)
        self.ref_funcs = device_handling.get_functions_from_string_list(self.ref_funcs)
        self.stop_funcs = device_handling.get_functions_from_string_list(self.stop_funcs)
        self.manual_funcs = device_handling.get_functions_from_string_list(self.manual_funcs)

        read_not_none = False
        for channel in self.read_channels:
            if channel is not None:
                read_not_none = True
                break
        if read_not_none:
            self.read_thread = Readback_Thread(self, self.read_channels, self.control_data['read_frequ'])
            self.read_thread.data_sig.connect(self.update_readback)
            self.read_thread.start()
        else:
            self.lineEdit_read_frequ.setEnabled(False)

        manual_X = self.control_data['manual_X']
        manual_Y = self.control_data['manual_Y']
        manual_Z = self.control_data['manual_Z']
        speeds = [manual_X, manual_Y, manual_Z]
        self.move_thread = Move_Thread(self, self.set_channels, speeds,
                                       manual_functions=self.manual_funcs,
                                       stop_functions=self.stop_funcs)
        self.move_thread.start()
        for child in self.children():
            if isinstance(child, QWidget):
                child.setFocusPolicy(Qt.ClickFocus)
        self.setFocusPolicy(Qt.ClickFocus)
        self.show()
        for i, auto in enumerate(self.control_data['auto_reference']):
            self.checks[i].setChecked(auto)
        self.reference_drive()
        for i, auto in enumerate(self.control_data['auto_reference']):
            self.checks[i].setChecked(True)


    def line_change(self):
        """ """
        for i, line in enumerate(self.lines):
            try:
                self.control_data[self.line_names[i]] = float(line.text())
            except:
                pass
        if self.read_thread:
            self.read_thread.read_time = self.control_data['read_frequ']
        manual_X = self.control_data['manual_X']
        manual_Y = self.control_data['manual_Y']
        manual_Z = self.control_data['manual_Z']
        self.move_thread.move_speeds = [manual_X, manual_Y, manual_Z]

    def check_change(self):
        """ """
        for i, check in enumerate(self.checks):
            self.control_data[self.check_names[i]] = check.isChecked()

    def update_readback(self, x, y, z):
        """

        Parameters
        ----------
        x :
            
        y :
            
        z :
            

        Returns
        -------

        """
        self.lineEdit_currentX.setText(number_formatting.format_number(x))
        self.lineEdit_currentY.setText(number_formatting.format_number(y))
        self.lineEdit_currentZ.setText(number_formatting.format_number(z))

    def close(self) -> bool:
        """ """
        if self.read_thread:
            self.read_thread.still_running = False
        if self.move_thread:
            self.move_thread.still_running = False
        return super().close()

    def closeEvent(self, a0) -> None:
        """

        Parameters
        ----------
        a0 :
            

        Returns
        -------

        """
        self.read_thread.still_running = False
        self.move_thread.still_running = False
        return super().closeEvent(a0)

    def step_axis(self, axis, up=True):
        """

        Parameters
        ----------
        axis :
            
        up :
             (Default value = True)

        Returns
        -------

        """
        ax_names = ['X', 'Y', 'Z']
        step_size = self.control_data[f'stepSize_{ax_names[axis]}']
        if not up:
            step_size *= -1
        if self.read_channels[axis] is not None:
            before = self.read_channels[axis].get()
        else:
            before = self.set_channels[axis].get()
        self.set_channels[axis].put(before + step_size)

    def reference_drive(self):
        """ """
        self.setCursor(Qt.WaitCursor)
        try:
            checks = [self.checkBox_refX, self.checkBox_refY, self.checkBox_refZ]
            for i, func in enumerate(self.ref_funcs):
                if checks[i].isChecked() and func:
                    func()
        finally:
            self.setCursor(Qt.ArrowCursor)

    def stop_moving(self):
        """ """
        for func in self.stop_funcs:
            if func:
                func()

    def input_position(self):
        """ """
        self.lineEdit_goX.setText(self.lineEdit_currentX.text())
        self.lineEdit_goY.setText(self.lineEdit_currentY.text())
        self.lineEdit_goZ.setText(self.lineEdit_currentZ.text())

    def move_to_position(self):
        """ """
        axes = ['X', 'Y', 'Z']
        for i in range(3):
            if self.set_channels[i]:
                self.set_channels[i].put(self.control_data[f'go_to_{axes[i]}'])

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        """

        Parameters
        ----------
        a0: QKeyEvent :
            

        Returns
        -------

        """
        if a0.isAutoRepeat():
            return super().keyPressEvent(a0)
        if not self.checkBox_manualActive.isChecked() or a0.modifiers() != Qt.ControlModifier:
            return super().keyPressEvent(a0)
        if a0.key() == Qt.Key_Left and (self.set_channels[0] or self.manual_funcs[0]):
            self.move_thread.up_dir[0] = False
            self.move_thread.movers[0] = True
        elif a0.key() == Qt.Key_Right and (self.set_channels[0] or self.manual_funcs[0]):
            self.move_thread.up_dir[0] = True
            self.move_thread.movers[0] = True
        elif a0.key() == Qt.Key_Up and (self.set_channels[1] or self.manual_funcs[1]):
            self.move_thread.up_dir[1] = True
            self.move_thread.movers[1] = True
        elif a0.key() == Qt.Key_Down and (self.set_channels[1] or self.manual_funcs[1]):
            self.move_thread.up_dir[1] = False
            self.move_thread.movers[1] = True
        elif a0.key() == Qt.Key_PageDown and (self.set_channels[2] or self.manual_funcs[2]):
            self.move_thread.up_dir[2] = False
            self.move_thread.movers[2] = True
        elif a0.key() == Qt.Key_PageUp and (self.set_channels[2] or self.manual_funcs[2]):
            self.move_thread.up_dir[2] = True
            self.move_thread.movers[2] = True
        else:
            super().keyPressEvent(a0)

    def keyReleaseEvent(self, a0: QKeyEvent) -> None:
        """

        Parameters
        ----------
        a0: QKeyEvent :
            

        Returns
        -------

        """
        if a0.isAutoRepeat():
            return super().keyPressEvent(a0)
        if a0.key() == Qt.Key_Left:
            self.move_thread.movers[0] = False
        elif a0.key() == Qt.Key_Right:
            self.move_thread.movers[0] = False
        elif a0.key() == Qt.Key_Up:
            self.move_thread.movers[1] = False
        elif a0.key() == Qt.Key_Down:
            self.move_thread.movers[1] = False
        elif a0.key() == Qt.Key_PageDown:
            self.move_thread.movers[2] = False
        elif a0.key() == Qt.Key_PageUp:
            self.move_thread.movers[2] = False
        else:
            super().keyReleaseEvent(a0)



class Move_Thread(QThread):
    """ """
    def __init__(self, parent=None, channels=None, move_speeds=None,
                 manual_functions=None, stop_functions=None):
        super().__init__(parent=parent)
        self.channels = channels or []
        self.manual_functions = manual_functions or []
        self.stop_functions = stop_functions or []
        self.still_running = True
        self.movers = [False, False, False]
        self.move_speeds = move_speeds or [0, 0, 0]
        self.move_starts = [np.nan, np.nan, np.nan]
        self.up_dir = [True, True, True]
        self.last_set = [np.nan, np.nan, np.nan]
        self.moving_started = [False, False, False]

    def run(self) -> None:
        """ """
        while self.still_running:
            move = False
            for i, mover in enumerate(self.movers):
                if mover:
                    move = True
                    if np.isnan(self.move_starts[i]):
                        self.move_starts[i] = time.time()
                        self.last_set[i] = self.channels[i].get()
                    self.move(i)
                else:
                    if not np.isnan(self.move_starts[i]):
                        self.move_starts[i] = np.nan
                        if self.stop_functions and self.stop_functions[i]:
                            self.stop_functions[i]()
                        self.moving_started[i] = False
            if not move:
                time.sleep(0.1)

    def move(self, ax):
        """

        Parameters
        ----------
        ax :
            

        Returns
        -------

        """
        if self.manual_functions and self.manual_functions[ax]:
            if not self.moving_started[ax]:
                self.manual_functions[ax](self.move_speeds[ax] * (1 if self.up_dir[ax] else -1))
        else:
            before = self.last_set[ax]
            now = time.time()
            step_size = self.move_speeds[ax] * (now - self.move_starts[ax])
            self.move_starts[ax] = now
            if not self.up_dir[ax]:
                step_size *= -1
            val = step_size + before
            self.channels[ax].put(val)
            self.last_set[ax] = val
        self.moving_started[ax] = True



class Readback_Thread(QThread):
    """ """
    data_sig = Signal(float, float, float)

    def __init__(self, parent=None, channels=None, read_time=np.inf):
        super().__init__(parent=parent)
        self.channels = channels or []
        self.read_time = read_time
        self.still_running = True

    def run(self):
        """ """
        accum = 0
        while self.still_running:
            self.do_reading()
            if self.read_time > 5:
                if self.read_time - accum > 5:
                    time.sleep(5)
                    accum += 5
                    continue
                else:
                    time.sleep(self.read_time - accum)
                    accum = 0
            else:
                time.sleep(self.read_time)

    def do_reading(self):
        """ """
        vals = []
        for channel in self.channels:
            if channel:
                vals.append(channel.get())
            else:
                vals.append(np.nan)
        self.data_sig.emit(*vals)



class Stage_Control_Config(Manual_Control_Config):
    """ """
    def __init__(self, parent=None, control_data=None):
        super().__init__(parent=parent, control_data=control_data,
                         title='Stage Control Config',
                         control_type='Stage_Control')
        control_data = control_data or {}
        self.axis_checkboxes = []
        self.channels_combos = []
        self.read_checkboxes = []
        self.read_combos = []
        self.ref_combos = []
        # self.ref_vals = []
        self.stop_combos = []
        # self.stop_vals = []
        self.auto_ref_checkboxes = []
        self.manual_move_combos = []
        outputs = variables_handling.get_output_channels()
        functions = variables_handling.get_non_channel_functions()
        channels = list(variables_handling.channels.keys())
        help_widge = QWidget()
        layout = QGridLayout()
        help_widge.setLayout(layout)
        for i, ax in enumerate(['x', 'y', 'z']):
            # label = QLabel(ax)
            # layout.addWidget(label, 2+i, 0)

            axis_box = QCheckBox(f'use axis {ax}')
            if 'use_axis' in control_data and control_data['use_axis']:
                axis_box.setChecked(control_data['use_axis'][i])
            self.axis_checkboxes.append(axis_box)
            layout.addWidget(axis_box, 2+i, 0)

            channel_combo = QComboBox()
            channel_combo.addItems(outputs)
            if 'axis_channel' in control_data and control_data['axis_channel'][i] in outputs:
                channel_combo.setCurrentText(control_data['axis_channel'][i])
            self.channels_combos.append(channel_combo)
            layout.addWidget(channel_combo, 2+i, 1)

            read_box = QCheckBox(f'readback axis {ax}')
            self.read_checkboxes.append(read_box)
            if 'read_axis' in control_data and control_data['read_axis']:
                read_box.setChecked(control_data['read_axis'][i])
            layout.addWidget(read_box, 2+i, 2)

            read_combo = QComboBox()
            read_combo.addItems(channels)
            if 'read_channel' in control_data and control_data['read_channel'][i] in channels:
                read_combo.setCurrentText(control_data['read_channel'][i])
            self.read_combos.append(read_combo)
            layout.addWidget(read_combo, 2+i, 3)


            label = QLabel(f'manual move function {ax}:')
            layout.addWidget(label, 2+i, 4)

            manual_combo = QComboBox()
            manual_combo.addItems(functions + ['None'])
            if 'manual_function' in control_data and control_data['manual_function'][i] in functions:
                manual_combo.setCurrentText(control_data['manual_function'][i])
            else:
                manual_combo.setCurrentText('None')
            self.manual_move_combos.append(manual_combo)
            layout.addWidget(manual_combo, 2+i, 5)


            label = QLabel(f'reference function {ax}:')
            layout.addWidget(label, 10+i, 0)

            ref_combo = QComboBox()
            ref_combo.addItems(functions + ['None'])
            if 'axis_ref' in control_data and control_data['axis_ref'][i] in functions:
                ref_combo.setCurrentText(control_data['axis_ref'][i])
            else:
                ref_combo.setCurrentText('None')
            self.ref_combos.append(ref_combo)
            layout.addWidget(ref_combo, 10+i, 1)

            # ref_val = QLineEdit()
            # if 'ref_vals' in control_data and control_data['ref_vals']:
            #     ref_val.setText(control_data['ref_vals'][i])
            # self.ref_vals.append(ref_val)
            # layout.addWidget(ref_val, 10+i, 2)

            label = QLabel(f'stop function {ax}:')
            layout.addWidget(label, 10+i, 2)

            stop_combo = QComboBox()
            stop_combo.addItems(functions + ['None'])
            if 'axis_stop' in control_data and control_data['axis_stop'][i] in functions:
                stop_combo.setCurrentText(control_data['axis_stop'][i])
            else:
                stop_combo.setCurrentText('None')
            self.stop_combos.append(stop_combo)
            layout.addWidget(stop_combo, 10+i, 3)

            auto_ref = QCheckBox('auto-reference at start')
            if 'auto_reference' in control_data:
                auto_ref.setChecked(control_data['auto_reference'][i])
            self.auto_ref_checkboxes.append(auto_ref)
            layout.addWidget(auto_ref, 10+i, 4, 1, 2)

            # stop_val = QLineEdit()
            # if 'stop_vals' in control_data and control_data['stop_vals']:
            #     stop_val.setText(control_data['stop_vals'][i])
            # self.stop_vals.append(stop_val)
            # layout.addWidget(stop_val, 10+i, 5)

            axis_box.clicked.connect(self.change_usage)
            read_box.clicked.connect(self.change_usage)
        self.layout().addWidget(help_widge, 1, 0, 1, 2)
        self.change_usage()

    def change_usage(self):
        """ """
        for i, box in enumerate(self.axis_checkboxes):
            able = box.isChecked()
            readback = self.read_checkboxes[i].isChecked()
            self.channels_combos[i].setEnabled(able)
            self.read_checkboxes[i].setEnabled(able)
            self.read_combos[i].setEnabled(able and readback)
            self.ref_combos[i].setEnabled(able)
            # self.ref_vals[i].setEnabled(able)
            self.stop_combos[i].setEnabled(able)
            self.auto_ref_checkboxes[i].setEnabled(able)
            self.manual_move_combos[i].setEnabled(able)
            # self.stop_vals[i].setEnabled(able)

    def accept(self):
        """ """
        self.control_data['use_axis'] = []
        self.control_data['axis_channel'] = []
        self.control_data['read_axis'] = []
        self.control_data['read_channel'] = []
        self.control_data['axis_ref'] = []
        # self.control_data['ref_vals'] = []
        self.control_data['axis_stop'] = []
        # self.control_data['stop_vals'] = []
        self.control_data['auto_reference'] = []
        self.control_data['manual_function'] = []
        for i in range(3):
            self.control_data['use_axis'].append(self.axis_checkboxes[i].isChecked())
            self.control_data['axis_channel'].append(self.channels_combos[i].currentText())
            self.control_data['read_axis'].append(self.read_checkboxes[i].isChecked())
            self.control_data['read_channel'].append(self.read_combos[i].currentText())
            # self.control_data['ref_vals'].append(self.ref_vals[i].text())
            self.control_data['axis_ref'].append(self.ref_combos[i].currentText())
            # self.control_data['stop_vals'].append(self.stop_vals[i].text())
            self.control_data['axis_stop'].append(self.stop_combos[i].currentText())
            self.control_data['auto_reference'].append(self.auto_ref_checkboxes[i].isChecked())
            self.control_data['manual_function'].append(self.manual_move_combos[i].currentText())

        super().accept()
