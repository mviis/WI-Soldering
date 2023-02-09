from PyQt5 import uic
from PyQt5 import QtCore 
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets,uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
import sys, base64,os,json,time
from timeapi import apptime
import admin_console
from marker_ import Canvas
import resources
from retry import retry
from mes_master import TraceProduction


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




class Popup(QtWidgets.QDialog):
    def __init__(self):
        super(Popup, self).__init__()
        file_path = resource_path('ui/popup_ui.ui')
        uic.loadUi(file_path, self)
        # uic.loadUi('ui/popup_ui.ui', self)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        file_path = resource_path('ui/main.ui')
        uic.loadUi(file_path, self)


class Alert(QtWidgets.QDialog):
    def __init__(self):
        super(Alert, self).__init__()
        file_path = resource_path('ui/alert.ui')
        uic.loadUi(file_path, self)



class Application:

    """main Application"""
    def expection_handleing(self,obj):
        #print(obj)
        pass

    def msgbx(self,title,text):
        self.window.setEnabled(False)
        self.msgBox.setText(text)
        self.msgBox.setWindowTitle(title)
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.exec_()
        
    def drawio(self):
        try:
            w = QWidget()
            self.canvas = Canvas()
            self.canvas.setMinimumWidth(1152)
            self.canvas.setMaximumWidth(1152)
            self.canvas.setMinimumHeight(620)
            self.canvas.setMaximumHeight(620)
            grid = self.window.grd_
            grid.addWidget(self.canvas,1152,620)
            self.canvas.resize(self.canvas.sizeHint()) 

            self.canvas.load_image(resource_path("resources/temp_.png"),w=1152,h=648)

        except Exception as e:
            print(e)


    def __init__(self):
        try:

            super().__init__()
            self.opp_id = 0000
            self.part_id = ""
            self.app = QtWidgets.QApplication(sys.argv)
            self.msgBox = QMessageBox()
            self.splash = QtWidgets.QSplashScreen(QPixmap(resource_path("resources/sketch.png")))
            self.splash.show()
            self.window = Ui()
            self.popup = Popup()
            self.alert = Alert()
            self.window.showFullScreen()
            self.admin = admin_console.Admin(self)
            self.initializers()
            self.timers()
            self.window.admin_tab.setTabEnabled(1, False)
            self.drawio()
            self.window.show()
            self.splash.hide()
            self.msgBox.setIcon(QMessageBox.Information)
            self.mesInterface = TraceProduction()
            try:
                if os.getenv("mviis_secret")=="r06IzLeZ+jYkxDeBjwc651mdWQa+aUynIE+bZ8acrKA=":
                    pass
                else:
                    raise Exception("Licence Error")

            except Exception as e:
                self.window.setEnabled(False)
                self.msgBox.setText("Invalid Licence")
                self.msgBox.setWindowTitle("Error!")
                self.msgBox.setStandardButtons(QMessageBox.Ok)
                self.msgBox.exec_()
                if self.msgBox.standardButton(self.msgBox.clickedButton()) == QMessageBox.Ok:
                    sys.exit()
                

            sys.exit(self.app.exec_())
        except Exception as e:
            self.expection_handleing(e)

    def create_folders(self):
        folders = ["programs","assy_log"]
        for f in folders:
            if not os.path.exists(f):
                os.mkdir(f)

  
            
    def initializers(self):
        self.window.setWindowTitle("MVIIS - Interactive Work Instructions with MES")
        self.confirm = False
        self.plogin=False
        self.temp_image = False
        self.step = -1
        self.create_folders()
        self.timers()
        self.connections()
        self.load_part_nums()
        self.prod_initializers()
        self.window.username_keyin.setFocus(True)
        self.child_sn = False
        self.set_animations_fade_in()
        self.set_animations_fade_out()
        self.set_animations_fade_in_wi()
       

    def load_part_nums(self):
        self.window.partnum_select.clear()
        self.window.partnum_select.addItem("Select an option")

        self.window.ptmgt_select_part.clear()
        self.window.ptmgt_select_part.addItem("Select an option")

        for files in os.listdir("programs"):
            if files.endswith(".json"):
                prog = files.strip(".json")
                self.window.partnum_select.addItem(prog)
                self.window.ptmgt_select_part.addItem(prog)
            

    def prod_initializers(self):
        self.parent_sn = False


    def timers(self):
        try:
            self.tx = QtCore.QTimer()
            self.tx.timeout.connect(lambda: self.appbeat())
            self.tx.start(10)
        except Exception as e:
            self.expection_handleing(e)

    def appbeat(self):
        try:
            self.window.dat_lab.setText("Date: "+str(apptime.sdate()))
            self.window.time_lab.setText("Time: "+str(apptime.stime()))
            self.window.shift_lab.setText("Shift: "+str(apptime.sshift()))
            self.window.operator_lab.setText("Operator: "+str(self.opp_id))
            if self.plogin==True and self.child_sn:
                session = apptime.unixnow()-self.session
                #self.window.sessionBar.setValue(300-int(session))
                if session > 300:
                    self.logout()
                else:
                    pass
                self.window.program_lab.setText("Program: "+str(self.part_id))
                self.window.total_assy_count_lab.setText("Current_assy: " + str(self.step+1) +" / "+ str(len(self.steps)))
                self.window.Parent_sn_lab.setText("Parent Part SN: " + str(self.parent_sn))
                self.window.child_part_lab.setText("Child Part# :" + str(self.child_sn))
                self.window.child_part_sn_lab.setText("Child Part SN:" + str(self.steps[self.step]['child_part_name']))
                self.window.Parent_part_lab.setText("Parent Part# :" + str(self.part_id))
                self.window.Board_position_lab.setText("Board Position: " + str(self.steps[self.step]['region']))
                self.window.location_ax.setText("Fixture Location: " + str(self.steps[self.step]['a_loc']))
            else:
                pass
                    
        except Exception as e:
            self.expection_handleing(e)
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_PageUp:
            self.next_wi()  
    def closeEvent(self):
        pass


    def set_animations_fade_in(self):
        self.anim_fin = QPropertyAnimation(self.popup, b"windowOpacity")
        self.anim_fin.setDuration(300)
        self.anim_fin.setStartValue(0.0)
        self.anim_fin.setEndValue(1.0)

    def set_animations_fade_out(self):
        self.anim_fout = QPropertyAnimation(self.popup, b"windowOpacity")
        self.anim_fout.setDuration(300)
        self.anim_fout.setStartValue(1.0)
        self.anim_fout.setEndValue(0.0)

    def set_animations_fade_in_wi(self):
        self.anim_fin_wi = QPropertyAnimation(self.window.label, b"Opacity")
        self.anim_fin_wi.setDuration(1000)
        self.anim_fin_wi.setStartValue(0.0)
        self.anim_fin_wi.setEndValue(1.0)
        self.anim_fin_wi.setProperty


    def connections(self):
        #self.window.sessionBar.setMinimum(0)
        #self.window.sessionBar.setMaximum(300)
        
        self.popup.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.popup.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.window.login_butt.clicked.connect(self.login)
        self.window.logout_p.clicked.connect(self.logout)
        self.window.next.clicked.connect(self.next_wi)
        # self.window.prev.clicked.connect(self.prev_wi)
        self.window.exit_butt.clicked.connect(lambda:sys.exit())
        self.popup.scanarea.returnPressed.connect(self.scan_check)
        self.window.username_keyin.returnPressed.connect(lambda:self.window.password_keyin.setFocus(True))
        self.window.password_keyin.returnPressed.connect(lambda:self.window.partnum_select.setFocus(True))
        self.window.keyPressEvent = self.keyPressEvent
        finish = QAction("Quit", self.popup)
        finish.triggered.connect(self.request_barcode)
        self.alert.OK_button.clicked.connect(lambda:self.alert.hide())

   
    
    #@retry(ReferenceError, tries=-1)   
    def next_wi(self):
        try:
            if self.step < len(self.steps) and not self.step+1==len(self.steps):
                if not self.confirm==True:
                    self.step = self.step+1
                 
                   
                self.request_barcode()
                
            elif self.confirm==True:
                self.request_barcode()
            else:
                comp = self.mesInterface.conduit_end(self.parent_sn)
                if comp[0]==True:
                    self.popup.diag_resp.setText(f"Assy & Stage Pass Success! <{self.parent_sn}>")
                else:
                    self.popup.diag_resp.setText(f"Assy & Stage Pass Failed! <{self.parent_sn}> \n {comp[1]}")
                #time.sleep(4)
                self.parent_sn= False
                self.child_sn=False
                self.step= -1
                self.request_barcode()
                
                ### MES STAGE PASSING ####
                pass
        except Exception as e:
            self.expection_handleing(e)

    def prev_wi(self):
        self.step = self.step-1
        

    def logout(self):
        self.opp_id = "XXXXXX"
        self.plogin = False
        self.child_sn=False
        self.parent_sn= False
        #self.window.opPane.setTabEnabled(0, True)
        self.window.opPane.setCurrentIndex(0)
        #self.window.opPane.setTabEnabled(1, False)
        #self.window.opPane.setTabEnabled(2, False)
        self.window.setEnabled(True)
        self.popup.hide()

    def attempt_login(self,un,pw):
        ###MESLOGIN####
        return True

    def login(self):
        self.window.login_resp.setText("")
        username = self.window.username_keyin.text()
        password = self.window.password_keyin.text()
        part_num = self.window.partnum_select.currentText()
        self.window.username_keyin.clear()
        self.window.password_keyin.clear()

        if username  !="" and password  != "":
            if username == "Admin" and password == "sanmina":
                self.window.opPane.setCurrentIndex(2)

            elif not username == "Admin" and self.attempt_login(username,password):
                if part_num  != "Select an option":
                    
                    self.plogin = self.mesInterface.conduit_login(un=username,pw=password)
                    if self.plogin == True:
                        self.session = apptime.unixnow()
                        self.opp_id = username
                        self.step = -1
                        self.window.opPane.setCurrentIndex(1)
                        self.part_id=part_num
                        self.load_program()
                        self.request_barcode()
                    else:
                        self.window.login_resp.setText("User Not Authorised")


                else:
                    self.window.login_resp.setText("Invalid Entry")

            else:
                    self.window.login_resp.setText("Invalid Entry")
        else:
            self.window.login_resp.setText("Invalid Entry")



    def load_program(self):
        try:
            file = open("programs/"+self.part_id+".json")
            self.stepData = json.load(file)
            steps = self.stepData["steps"]
            self.steps = sorted(steps, key=lambda d: d['step_no']) 
            self.part_id = self.stepData['partname']
            self.window.progressBar.setMinimum(0)
            self.window.progressBar.setMaximum(len(self.steps))
            self.window.progressBar.setValue(self.step)
            
                
        except Exception as e:
            self.expection_handleing(e)

    def create_assy_log(self,sn):
        with open(r"assy_log/"+sn+'.json',"w") as f:
            d = {"partname":self.part_id,"parent_serial":sn,"operator":str(self.opp_id),"datetime":str(apptime.sdate())+str(apptime.stime()),"steps":[]}
            json.dump(d,f,indent=4)


    def check_assy_log(self,sn
                       ):
        if os.path.isfile(r"assy_log/"+sn+'.json'):
            with open(r"assy_log/"+sn+'.json',"r") as f:
                d = json.load(f)
                steps = d["steps"]
                steps = sorted(steps, key=lambda d: d['Assy_step'])
                if len(steps)!=0:
                    self.step = int(steps[-1]["Assy_step"])
                else:
                    self.step = 0
                self.next_wi()
        else:
            self.anim_fout.start()
            self.popup.hide()
            self.window.setDisabled(False)
            self.create_assy_log(sn)
            self.next_wi()


    def update_assy_log(self):
        with open(r"assy_log/"+self.parent_sn+'.json',"r") as f:
            d = json.load(f)

        child_log = {
                    "Assy_step":self.step,
                    "child_part_name": str(self.steps[self.step]['child_part_name']),
                    "child_part_serial": str(self.child_sn),
                    "integration_time": str(apptime.sdate())+str(apptime.stime()),  
                    "operator":self.opp_id,
                    "location":str(self.steps[self.step]['a_loc'])
                    }
                    
        d["steps"].append(child_log)
        with open(r"assy_log/"+self.parent_sn+'.json',"w") as f: 
            json.dump(d,f,indent=4)

        self.anim_fout.start()
        self.popup.hide()
        self.confirm=False
        self.next_wi()
        

    def scan_check(self):
        sn = self.popup.scanarea.text()
        self.popup.scanarea.clear()
        sn = sn.upper()

        if sn.upper() == "EXIT":
            self.logout()

        if  self.parent_sn == False:
            wtloc =self.mesInterface.check_whatlog(sn=sn,pn=self.part_id,swk=self.stepData["parent_swstn"])
            #wtloc = True,""
            if wtloc[0]== True:
                # end = self.mesInterface.conduit_end(sn)
                # if end[0]==True:
                self.parent_sn = sn 
                self.check_assy_log(sn)
            #     else:
            #         self.parent_sn == False
            #         self.popup.diag_resp.setText(end[1])
            else:
                self.parent_sn == False
                self.popup.diag_resp.setText(wtloc[1])

        elif not self.parent_sn == False and self.confirm==False:
            wtloc =self.mesInterface.check_whatlog(sn=sn,pn=self.steps[self.step]["child_part_name"],swk=self.steps[self.step]["short_workstation"])

            if wtloc[0]==True:
                self.child_sn = sn
                self.anim_fout.start()
                self.popup.hide()
                self.window.setDisabled(False)
                self.image_path =  self.steps[self.step]["image_path"]
                self.show_wi_pic()
                self.session = apptime.unixnow()
                self.confirm = True
            else:
                self.popup.diag_resp.setText(wtloc[1])

        elif self.confirm==True:
                if sn==self.steps[self.step]['a_loc']:
                    x= self.mesInterface.assemble_pcba(self.parent_sn,self.child_sn,self.steps[self.step]['a_loc'])
                    if x[0] == True:
                        self.update_assy_log()
                    else:
                        self.popup.diag_resp.setText(x[1])
                else:
                    logform = str(apptime.sdate())+str(apptime.stime()) + "," + self.opp_id + "," + str(self.child_sn) + "," + self.steps[self.step]['a_loc'] +"," + sn +"\n"
                    open("location.log","a+").write(logform)
                    self.popup.diag_resp.setText("Invalid Location!")
                    
            
    def request_barcode(self):
        if not self.parent_sn:
            self.popup.setStyleSheet("QDialog {background-color:#495b53;color:white}")
            self.window.setDisabled(True)
            self.popup.diag_reqs.setText("Scan the Parent SN#" + self.part_id)
            self.popup.diag_resp.setText("")
            self.anim_fin.start()
            self.popup.show()
            
        else:
            try:
                if self.step <= len(self.steps):
                    self.window.setDisabled(True)
                    if self.confirm==False:
                        self.popup.diag_reqs.setText("Scan the Child SN#" +self.steps[self.step]["child_part_name"])
                    else:
                        self.popup.diag_reqs.setText("Scan the Location Tag#")
                    self.popup.diag_resp.setText("")
                    self.popup.setStyleSheet("QDialog {background-color:#495b53;color:white}")
                    self.anim_fin.start()
                    self.popup.show()
                else:
                    ####DO SFDC PASSS ###
                    pass
            except Exception as e:
                print(e)

       

    def show_wi_pic(self):
        try:
            cwd = os.getcwd()
            path = os.path.join(cwd,self.image_path)
            self.window.label.setPixmap(QPixmap(path))
            self.anim_fin_wi.start()
            self.window.progressBar.setValue(self.step+1)

        except Exception as e:
            print(e)
            self.window.label.setPixmap(QPixmap(resource_path("resources/temp_.png")))
                # self.window.assy_msg_disp.setText("")
    
    def select_image(self):
        try:
            fname = QFileDialog.getOpenFileName(self.window, 'Open file','c:\\',"Image files (*.jpg *.png)")
            print(fname[0])
            self.temp_image = fname[0]
            self.canvas.load_image(fname[0],w=1152,h=620)
          
        except Exception as e:
            print(e)

        

if __name__=="__main__":

    myapp= Application()