from PyQt5 import QtWidgets
from PyQt5 import uic
import os,json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import base64,os
from pathlib import Path
import shutil

class Admin:
    def __init__(self,window):
        try:
            self.app = window
            self.window = window.window
            self.alert = self.app.alert
            self.connections()
            self.initializers()
        except Exception as e:
            print(e)


    def initializers(self):
        self.msgBox = QMessageBox()
        if not os.path.isfile("configuration.json"):
            configuration = {"curl":"","murl":"","data_source":"","station":""} 
            with open("configuration.json","w") as file:
                json.dump(configuration,file)
        else:
            file = open("configuration.json")
            conf  = json.load(file)
            self.window.mes_url.setText(conf["murl"])
            self.window.con_url.setText(conf["curl"])
            self.window.data_source.setText(conf["data_source"])
            self.window.stn_address.setText(conf["station"])
        self.select_step_counter = -1
        

    def get_steps_count(self):
        self.window.spinBox_create_steps.setMinimum(1)
        self.window.spinBox_create_steps.setMaximum(len(self.steps))
        self.window.spinBox_select_steps.setMinimum(1)
        self.window.spinBox_select_steps.setMaximum(len(self.steps))
        

    def admin_load_program(self):
        try:
            file = open("programs/"+self.selected_part+".json")
            self.stepData = json.load(file)
            steps = self.stepData["steps"]
            self.steps = sorted(steps, key=lambda d: d['step_no']) 
            self.part_id = self.stepData['partname']
            self.window.parent_shwk.setText(self.stepData['parent_swstn'])
            self.get_steps_count()

        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

    
    def insert_step(self):
        self.admin_load_program()
        current_step = self.window.spinBox_create_steps.value()

        for each in range(current_step,len(self.steps)):
            
            try:
                self.steps[each]['step_no'] = each+2
                self.steps[each]['image_path'] = f"programs/{self.selected_part}/imgs/{each+2}.png"
            except:
                pass
        self.steps.append({"step_no":current_step+1,"child_part_name":"","short_workstation":"","region":"TOP","image_path":"","a_loc":""})
        self.stepData["steps"] = self.steps
        with open("programs/"+self.selected_part+".json","w") as file:
            json.dump(self.stepData,file)
     
        for i in reversed(range(current_step,len(self.steps))):
            try:
                src = "programs/"+self.selected_part+"/imgs/"+str(i+1)+".png"
                dsc = "programs/"+self.selected_part+"/imgs/"+str(i+2)+".png"
                os.rename(src,dsc)
            except Exception as e:
              
                pass

        self.admin_load_program()
        self.select_step()

    def delete_step(self):
        self.admin_load_program()
        current_step = self.window.spinBox_create_steps.value()
        if not current_step <= 1 :
            for each in self.steps:
                if each["step_no"]==current_step:
                    self.steps.remove(each)
            
            for each in range(current_step-1,len(self.steps)):
                self.steps[each]['step_no'] = each  + 1
                self.steps[each]['image_path'] = f"programs/{self.selected_part}/imgs/{each  + 1}.png"
            self.stepData["steps"] = self.steps
            with open("programs/"+self.selected_part+".json","w") as file:
                json.dump(self.stepData,file)
            try:
                os.remove("programs/"+self.selected_part+"/imgs/"+str(current_step)+".png")
            except:
                    pass

            for i in range(current_step,len(self.steps)+1):
                try:
                   
                    src = "programs/"+self.selected_part+"/imgs/"+str(i+1)+".png"
                    dsc = "programs/"+self.selected_part+"/imgs/"+str(i)+".png"
                    os.rename(src,dsc)
                except Exception as e:
                    pass
            self.admin_load_program()
            self.select_step()
        else:
            self.alert.diag_label.setText("Primary Step cannot be Deleted")
            self.alert.show()

    def select_step(self):
        self.admin_load_program()
        current_step = self.window.spinBox_select_steps.value() - 1
        self.window.child_pn.setText(str(self.steps[current_step]["child_part_name"]))
        self.window.comboBox_region.setCurrentText(str(self.steps[current_step]["region"]))
        self.window.sworkstn.setText(str(self.steps[current_step]["short_workstation"]))
        self.window.location_code.setText(str(self.steps[current_step]["a_loc"]))
        i = f"programs/{self.window.ptmgt_select_part.currentText()}/imgs/{current_step+1}.png"
        try:
            self.app.canvas.load_image(i,w=1152,h=648)
        except:
            if  self.app.temp_image == False:
                self.app.canvas.load_image("resources/temp_.png",w=1152,h=648)
            else:
                self.app.canvas.load_image(self.app.temp_image,w=1152,h=648)
        
    def connections(self):
        try:
            # self.alert.OK_button.clicked.connect(lambda:self.alert.hide())
            self.window.insert_steps.clicked.connect(self.insert_step)
            self.window.delete_step.clicked.connect(self.delete_step)
            
            self.window.exit_teaching.clicked.connect(self.close_teaching)
            self.window.spinBox_select_steps.valueChanged.connect(self.select_step)
            self.window.spinBox_create_steps.valueChanged.connect(self.button_value_change)

            self.window.ptmgt_select_part_butt.clicked.connect(self.select_part)
            self.window.ptmgt_create_part.clicked.connect(self.create_part)
            self.window.ptmgt_delete_part.clicked.connect(self.delete_part)

            self.window.select_image.clicked.connect(self.app.select_image)

            self.window.red.clicked.connect(lambda:self.app.canvas.setColors(Qt.red))
            self.window.green.clicked.connect(lambda:self.app.canvas.setColors(Qt.green))
            self.window.undo.clicked.connect(lambda:self.app.canvas.undo())
            self.window.admin_logout.clicked.connect(self.app.logout)
            self.window.SaveStep.clicked.connect(self.save_step)
            self.window.update_parent_shwk.clicked.connect(self.update_parent_shwk)
            self.window.update_configurations.clicked.connect(self.update_configurations)

        

        except Exception as e:
            print(e)

    def update_configurations(self):
        murl = self.window.mes_url.text()
        curl = self.window.con_url.text()
        ndc = self.window.data_source.text()
        stn = self.window.stn_address.text()
        configuration = {"curl":curl,"murl":murl,"data_source":ndc,"station":stn}
        with open("configuration.json","w") as file:
            json.dump(configuration,file)


    def update_parent_shwk(self):
        text  = self.window.parent_shwk.text()
        self.stepData["parent_swstn"]= text
        with open("programs/"+self.selected_part+".json","w") as file:
            json.dump(self.stepData,file)

    def button_value_change(self):
        x = str(self.window.spinBox_create_steps.value())
        self.window.insert_steps.setText(f"Instert step after<{x}>")
        self.window.delete_step.setText(f"Delete step<{x}>")

    def close_teaching(self):
        self.window.admin_tab.setTabEnabled(0,True)
        self.window.admin_tab.setTabEnabled(1,False)
        self.window.admin_tab.setCurrentIndex(0)

    def select_part(self):
        try:
            part = self.window.ptmgt_select_part.currentText()
            if not "select" in part:

                if os.path.isfile("programs/"+part+".json"):
                    self.window.admin_tab.setTabEnabled(1,True)
                    self.window.admin_tab.setTabEnabled(0,False)
                    self.window.program_name.setText(part)
                    
                    self.selected_part = part
                    self.admin_load_program()
                    self.select_step()
                else:
                    self.alert.diag_label.setText("No Programs Found or Create the Program")
                    self.alert.show()
            else:
                self.alert.diag_label.setText("Select a program")
                self.alert.show()
        except Exception as e:
            print(e)



    def create_part(self):
        
        part = self.window.ptmgt_select_part.currentText()
        part = part.upper()
        if not "Select" in part:
            i = f"programs/{self.window.ptmgt_select_part.currentText()}/imgs/"
            if not os.path.exists(i):
                os.makedirs(i)
            if not os.path.isfile("programs/"+part+".json"):
                open(r"programs/"+part+".json",'w').write('{"partname":"'+part+'","parent_swstn":"","steps":[{"step_no":1,"child_part_name":"","short_workstation":"","region":"","image_path":"","a_loc":""}]}')
                self.alert.diag_label.setText(f"New Program created <{part}>")

                self.alert.show()
                
            else:
                self.alert.diag_label.setText(f"Program <{part}> is already exists")
                self.alert.show()
        else:
            self.alert.diag_label.setText("Create a new program")
            self.alert.show()
        self.app.load_part_nums()

    def delete_part(self):
        part = self.window.ptmgt_select_part.currentText()
        if not "Select" in part :
            if os.path.isfile("programs/"+part+".json"):
                self.alert.diag_label.setText(f"The Program <{part}> deleted successfully.")
                os.remove(r"programs/"+part+".json")
                shutil.rmtree(r"programs/"+part)
                self.alert.show()

            else:
                self.alert.diag_label.setText(f"No such program <{part}> found to be deleted.")
                self.alert.show()
        else:
            self.alert.diag_label.setText("Create a new program")
            self.alert.show()
        self.app.load_part_nums()
        


    def save_step(self):
        current_step = int(self.window.spinBox_select_steps.value()-1)
        c = self.window.child_pn.text()
        r = self.window.comboBox_region.currentText()
        w = self.window.sworkstn.text()
        a = self.window.location_code.text()
        i = f"programs/{self.window.ptmgt_select_part.currentText()}/imgs/{current_step+1}.png"
        self.app.canvas.save_image(str(i),"PNG",100)
        self.steps[current_step]["child_part_name"]=c
        self.steps[current_step]["short_workstation"]=w
        self.steps[current_step]["region"]=r
        self.steps[current_step]["a_loc"]=a
        self.steps[current_step]["image_path"]=str(i)
        with open("programs/"+self.selected_part+".json","w") as file:
            json.dump(self.stepData,file)



   