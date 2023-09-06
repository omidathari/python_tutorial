import subprocess

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit

import fc_hmi
import udp_client_class
import threading
import time
import sys
import json
import os


class uiMain(fc_hmi.Ui_MainWindow, QtWidgets.QMainWindow):
    # For some strange reason this must be outside the __init__ function
    server_rx_Signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(uiMain, self).__init__()
        self.setupUi(self)
        self.fdir = r'C:\Work\FastChargeConfig'
        self.server_ip = "127.0.0.1"
        self.server_port = 20001
        self.gui_ip = "127.0.0.1"
        self.gui_port = 20003
        self.serverIx = udp_client_class.udpClientObject(self.server_ip, self.server_port, self.gui_ip, self.gui_port,
                                                         self.__server_receiver)
        self.app = None
        self.__connect_signal_slots()
        self.update_thread = threading.Thread(target=self.__update_thread_processor)
        self.monitor_thread = threading.Thread(target=self.__monitor_thread_processor)
        self.__start_server_connection()
        self.threads_exit = False
        self.imc = 0
        # remap controls for easy access
        # DCDC tabs
        self.dcdc_tab = []
        self.op_mode = []
        self.setpoint = []
        self.limit_type = []
        self.clamp_status = []
        self.con_mode = []
        self.con_type = []
        self.cur_limit = []
        self.errors1 = []
        self.errors2 = []
        self.warnings = []
        self.measures = []

        # CRM Tabs
        self.crm_tab = []
        self.crm_batteries = []
        self.crm_status = []
        self.hpr_status = []
        self.or_status = []
        self.fan_status = []
        self.hpr_health = []
        self.or_health = []
        self.cf_health = []
        self.df_health = []

        # MRS Tabs
        self.mrs_tab = []
        self.mrs_analogs = []
        self.mrs_relays = []

        self.remap()
        self.update_thread.start()
        self.monitor_thread.start()
        self.show()

    def remap(self):
        # DCDC Section
        for x in range(1, 6):
            self.dcdc_tab.append(self.findChild(QtWidgets.QWidget, "tab_dcdc" + str(x)))
            self.op_mode.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_op_mode_" + str(x)))
            self.setpoint.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_setpoint_" + str(x)))
            self.limit_type.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_limit_type_" + str(x)))
            self.clamp_status.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_clamp_status_" + str(x)))
            self.con_mode.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_con_mode_" + str(x)))
            self.con_type.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_con_type_" + str(x)))
            self.cur_limit.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_cur_limit_" + str(x)))
            self.errors1.append(self.findChild(QtWidgets.QTextEdit, "textEdit_errors1_" + str(x)))
            self.errors2.append(self.findChild(QtWidgets.QTextEdit, "textEdit_errors2_" + str(x)))
            self.warnings.append(self.findChild(QtWidgets.QTextEdit, "textEdit_warnings_" + str(x)))
            self.measures.append(self.findChild(QtWidgets.QTextEdit, "textEdit_measures_" + str(x)))

        # CRM Section
        battery = {}
        bat_mapper = 0
        for x in range(1, 5):
            self.crm_tab.append(self.findChild(QtWidgets.QWidget, "tab_crm" + str(x)))
            self.crm_status.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_crm_status_" + str(x)))
            self.hpr_status.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_hpr_status_" + str(x)))
            self.or_status.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_or_status_" + str(x)))
            self.fan_status.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_fan_status_" + str(x)))
            self.hpr_health.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_hpr_health_" + str(x)))
            self.or_health.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_or_health_" + str(x)))
            self.cf_health.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_cf_health_" + str(x)))
            self.df_health.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_df_health_" + str(x)))

            # print(bat_mapper)
            for i in range(1, 9):
                battery["cell1_" + str(i)] = self.findChild(QtWidgets.QLineEdit,
                                                            "lineEdit_cell1_" + str(i + bat_mapper))
                battery["cell2_" + str(i)] = self.findChild(QtWidgets.QLineEdit,
                                                            "lineEdit_cell2_" + str(i + bat_mapper))
                battery["cell3_" + str(i)] = self.findChild(QtWidgets.QLineEdit,
                                                            "lineEdit_cell3_" + str(i + bat_mapper))
                battery["cell4_" + str(i)] = self.findChild(QtWidgets.QLineEdit,
                                                            "lineEdit_cell4_" + str(i + bat_mapper))
                battery["batV_" + str(i)] = self.findChild(QtWidgets.QLineEdit, "lineEdit_batv_" + str(i + bat_mapper))
                battery["batI_" + str(i)] = self.findChild(QtWidgets.QLineEdit, "lineEdit_bati_" + str(i + bat_mapper))
                battery["batT_" + str(i)] = self.findChild(QtWidgets.QLineEdit,
                                                           "lineEdit_bat_temp_" + str(i + bat_mapper))
                battery["comm_" + str(i)] = self.findChild(QtWidgets.QLineEdit,
                                                           "lineEdit_bat_comm_" + str(i + bat_mapper))
            print(bat_mapper)
            self.crm_batteries.append(battery.copy())
            battery.clear()
            bat_mapper += 8

        # MRS Section
        analogs = []
        relays = []
        for x in range(1, 6):
            self.mrs_tab.append(self.findChild(QtWidgets.QWidget, "tab_mrs" + str(x)))
            for y in range(1, 14):
                analogs.append(self.findChild(QtWidgets.QLineEdit, "lineEdit_ch" + str(y) + "_" + str(x)))
            for y in range(1, 13):
                relays.append(self.findChild(QtWidgets.QLineEdit, "relay" + str(x) + "_" + str(y)))
            self.mrs_analogs.append(analogs.copy())
            self.mrs_relays.append(relays.copy())
            analogs.clear()
            relays.clear()

    def open_file(self, filename):
        while os.path.exists(filename) == False:
            tdir, OK = QInputDialog.getText(self, 'FileDir', 'input the file dir', QLineEdit.Normal, '')
            filename = str(os.path.join(tdir, filename.split('\\')[-1]))
            if OK == False:
                return

        # if os.path.exists(filename):
        #     ...
        # else:
        #     tdir, OK = QInputDialog.getText(self, 'FileDir', 'input the file dir', QLineEdit.Normal, ' ')
        #     filename = str(os.path.join(tdir,filename.split('\\')[-1]))
        subprocess.Popen(['notepad.exe', filename])
        # print('ret',ret)
        reply = QMessageBox.critical(self, 'warning', "you're changing the file:" + filename,
                                     QMessageBox.Yes | QMessageBox.No)

        # print(reply,'ss')

    def __connect_signal_slots(self):
        # Connect all signals to slots here
        self.server_rx_Signal.connect(self.gui_rx_slot)
        self.actionDCDC_Configuration.triggered.connect(self.dcdc_config_slot)
        self.actionCRM_Configuration.triggered.connect(self.crm_config_slot)
        self.actionMRS_Configuration.triggered.connect(self.mrs_config_slot)
        self.start_stop.clicked.connect(self.button_start_stop)
        self.reset.clicked.connect(self.reset_clicked)
        self.save.clicked.connect(self.save_clicked)

    def save_clicked(self):
        print('save_clieked')
        jsonData = {"request": "reload"}
        self.serverIx.send(str.encode(json.dumps(jsonData)))

    def reset_clicked(self):
        print('reset_clicked')
        jsonData = {"request": "reset"}
        self.serverIx.send(str.encode(json.dumps(jsonData)))

    @QtCore.pyqtSlot(bool)
    def button_start_stop(self, flag):
        print("Start Stop Button Clicked")
        text = self.start_stop.text()
        if text == 'Start':
            jsonData = {"request": "start"}
            self.serverIx.send(str.encode(json.dumps(jsonData)))
            self.start_stop.setText('Stop')
        elif text == 'Stop':
            jsonData = {"request": "stop"}
            self.serverIx.send(str.encode(json.dumps(jsonData)))
            self.start_stop.setText('Start')
        else:
            print('exception text pls check')

    @QtCore.pyqtSlot(bool)
    def dcdc_config_slot(self):
        print("DCDC ")
        # self.show_msgbox("DCDC Config action.")
        filename = self.fdir + '\dcdc_configuration.ini'
        self.open_file(filename)

    def crm_config_slot(self):
        print("CRM ")
        # self.show_msgbox("CRM Config action.")
        filename = self.fdir + '\crm_configuration.ini'
        self.open_file(filename)

    def mrs_config_slot(self):
        print("MRS ")
        # self.show_msgbox("MRS Config action.")
        filename = self.fdir + '\mrs_configuration.ini'
        self.open_file(filename)

    @QtCore.pyqtSlot(str)
    def gui_rx_slot(self, test):
        try:
            self.imc += 1
            rx_dict: dict = json.loads(test)

            if ("DCDC" in rx_dict.keys()):
                kv = rx_dict["data"]
                self.handle_dcdc_json(rx_dict["DCDC"], kv)
            elif ("CRM" in rx_dict.keys()):
                kv = rx_dict["data"]
                self.handle_crm_json(rx_dict["CRM"], kv)
            elif ("MRS" in rx_dict.keys()):
                kv = rx_dict["data"]
                self.handle_mrs_json(rx_dict["MRS"], kv)
            elif ("state_machine" in rx_dict.keys()):
                kv = rx_dict["state_machine"]
                self.handle_system_json(kv)

        except BaseException as e:
            print("Exception:", e)

    def handle_dcdc_json(self, dcdc_id, dic):
        try:
            id = dcdc_id - 1
            if (dic["inuse"] == False):
                self.tabWidget_DCDC.tabBar().setTabVisible(id, False)
                return
            else:
                self.tabWidget_DCDC.tabBar().setTabVisible(id, True)

            if (dic["communication"] == False):
                self.tabWidget_DCDC.tabBar().setTabTextColor(id, QtCore.Qt.red)
            else:
                self.tabWidget_DCDC.tabBar().setTabTextColor(id, QtCore.Qt.black)

            self.op_mode[id].setText(dic["softwareMode"])
            self.setpoint[id].setText(str(dic["setpoint"]))
            self.limit_type[id].setText(str(dic["limitationType"]))
            self.clamp_status[id].setText(str(dic["clampStatus"]))
            self.con_mode[id].setText(dic["converterMode"])
            self.con_type[id].setText(dic["controlType"])
            self.cur_limit[id].setText(str(dic["currentLimit"]))
            self.errors1[id].setText(str(dic["errors1"]))
            self.errors2[id].setText(str(dic["errors2"]))
            self.warnings[id].setText(str(dic["warnings"]))
            s = ""
            for k, v in dic.items():
                if k in ['iLow', 'iHigh', 'iLow2', 'vLow', 'vHigh', 'vlow2', 'vHigh2', 'pLow', 'pHigh', 'temp1',
                         'temp2', 'temp3', 'temp4']:
                    s += str(k) + '\t: ' + str(v) + '\n'
            self.measures[id].setText(s)


        except BaseException as e:
            print(e)

    def handle_crm_json(self, crm_id, dic):
        try:
            id = crm_id - 1
            if (dic["inuse"] == False):
                self.tabWidget_CRM.tabBar().setTabVisible(id, False)
                return
            else:
                self.tabWidget_CRM.tabBar().setTabVisible(id, True)

            if (dic["communication"] == False):
                self.tabWidget_CRM.tabBar().setTabTextColor(id, QtCore.Qt.red)
            else:
                self.tabWidget_CRM.tabBar().setTabTextColor(id, QtCore.Qt.black)

            self.crm_status[id].setText(str(dic["crm_health_status"]))
            self.hpr_status[id].setText(str(dic["halfpack_relay_status"]))
            self.or_status[id].setText(str(dic["output_relay_status"]))
            self.fan_status[id].setText(str(dic["fan_status"]))
            self.hpr_health[id].setText(str(dic["halfpack_relay_health"]))
            self.or_health[id].setText(str(dic["output_relay_health"]))
            # self.cf_health[id].setText(str(dic["warnings"]))
            # self.df_health[id].setText(str(dic["warnings"]))

            # All 8 batteries
            battery = self.crm_batteries[id]
            for i in range(1, 9):
                bat_json = dic["battery_" + str(i)]
                battery["cell1_" + str(i)].setText(str(bat_json["cell_voltage_1"]))
                battery["cell2_" + str(i)].setText(str(bat_json["cell_voltage_2"]))
                battery["cell3_" + str(i)].setText(str(bat_json["cell_voltage_3"]))
                battery["cell4_" + str(i)].setText(str(bat_json["cell_voltage_4"]))
                battery["batV_" + str(i)].setText(str(bat_json["battery_voltage"]))
                battery["batI_" + str(i)].setText(str(bat_json["battery_current"]))
                battery["batT_" + str(i)].setText(str(bat_json["battery_temp"]))
                battery["comm_" + str(i)].setText(str(bat_json["comm_status"]))

        except BaseException as e:
            print("handle_crm_json Exception: " + str(e))

    def handle_mrs_json(self, mrs_id, dic):
        try:
            id = mrs_id - 1
            if (dic["inuse"] == False):
                self.tabWidget_MRS.tabBar().setTabVisible(id, False)
                return
            else:
                self.tabWidget_MRS.tabBar().setTabVisible(id, True)

            if (dic["communication"] == False):
                self.tabWidget_MRS.tabBar().setTabTextColor(id, QtCore.Qt.red)
            else:
                self.tabWidget_MRS.tabBar().setTabTextColor(id, QtCore.Qt.black)

            for i in range(1, 14):
                self.mrs_analogs[id][i - 1].setText(str(dic["AnalogChannel" + str(i)]))

            for i in range(1, 13):
                self.mrs_relays[id][i - 1].setStyleSheet(
                    "background-color:" + ("yellow" if dic['relay' + str(i)] == False else "red"))
                # self.mrs_relays[id][i - 1].setText(str(dic["relay" + str(i)]))

        except BaseException as e:
            print(e)

    def change_server_color(self, dic):
        if dic['current_state'] == 'standby':  # gray
            self.server_status.setStyleSheet(
                "background-color: gray;\nborder-style:none;\nborder:1px solid #3f3f3f; \npadding:5px;\nmin-height:20px;\nborder-radius:15px;\n")
        elif dic['current_state'] == 'start':  # green
            self.server_status.setStyleSheet(
                "background-color: green;\nborder-style:none;\nborder:1px solid #3f3f3f; \npadding:5px;\nmin-height:20px;\nborder-radius:15px;\n")
        elif dic['current_state'] == 'stop':  # red
            self.server_status.setStyleSheet(
                "background-color: red;\nborder-style:none;\nborder:1px solid #3f3f3f; \npadding:5px;\nmin-height:20px;\nborder-radius:15px;\n")

    def handle_system_json(self, dic):
        self.lineEdit_input_voltage.setText(str(dic["input_voltage"]))
        self.lineEdit_input_current.setText(str(dic["input_current"]))
        self.lineEdit_output_voltage.setText(str(dic["output_voltage"]))
        self.lineEdit_output_current.setText(str(dic["output_current"]))
        self.server_status.setText(str(dic["current_state"]))
        self.faults.setText(str(dic["faults"]) + " " + str(self.imc))
        self.change_server_color(dic)

    def __update_thread_processor(self):
        val = 0.0
        while True:
            time.sleep(1)  # 0.100 minimum
            jsonData = {"request": "update"}
            self.serverIx.send(str.encode(json.dumps(jsonData)))
            if self.threads_exit == True:
                break

    def __monitor_thread_processor(self):
        val = 0.0
        while True:
            time.sleep(2)  # 0.100 minimum
            # monitor the server and connections here
            if self.threads_exit == True:
                break

    def __server_receiver(self, data):
        self.server_rx_Signal.emit(data.decode())

    def __start_server_connection(self):
        self.serverIx.start()

    def show_msgbox(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("MessageBox!")
        msg.setInformativeText(message)
        msg.setWindowTitle(message)
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        retval = msg.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qt_app = uiMain()
    app.exec_()
    qt_app.threads_exit = True
    qt_app.serverIx.stop()
    print("Application Exit")
