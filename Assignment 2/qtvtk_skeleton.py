#!/usr/bin/python

'''
    Skeleton code for a GUI application created by using PyQT and PyVTK
'''


import sys
import vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import Qt

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


'''
    The Qt MainWindow class
    A vtk widget and the ui controls will be added to this main window
'''
class MainWindow(Qt.QMainWindow):

    def __init__(self, parent = None):
        Qt.QMainWindow.__init__(self, parent)
        
        ''' Step 1: Initialize the Qt window '''
        self.setWindowTitle("COSC 6344 Visualization")
        self.resize(1000,self.height())
        self.frame = Qt.QFrame() # Create a main window frame to add ui widgets
        self.mainLayout = Qt.QHBoxLayout()  # Set layout - Lines up widgets horizontally
        self.frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.frame)
        
        ''' Step 2: Add a vtk widget to the central widget '''
        # As we use QHBoxLayout, the vtk widget will be automatically moved to the left
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.mainLayout.addWidget(self.vtkWidget)
        
        #Initialize the vtk variables for the visualization tasks
        self.init_vtk_widget()
        
        # Add an object to the rendering window
        self.add_vtk_object()
        
        ''' Step 3: Add the control panel to the right hand side of the central widget '''
        # Note: To add a widget, we first need to create a widget, then set the layout for it
        self.right_panel_widget = Qt.QWidget() # create a widget
        self.right_panel_layout = Qt.QVBoxLayout() # set layout - lines up the controls vertically
        self.right_panel_widget.setLayout(self.right_panel_layout) #assign the layout to the widget
        self.mainLayout.addWidget(self.right_panel_widget) # now, add it the the central frame
        
        # The controls will be added here
        self.add_controls()
        
 

    '''
        Initialize the vtk variables for the visualization tasks
    '''    
    def init_vtk_widget(self):
        vtk.vtkObject.GlobalWarningDisplayOff() #Disable vtkOutputWindow - Comment out this line if you want to see the warning/error messages from vtk
        
        # Create the graphics structure. The renderer renders into the render
        # window. The render window interactor captures mouse events and will
        # perform appropriate camera or actor manipulation depending on the
        # nature of the events.
        self.ren = vtk.vtkRenderer() 
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        colors = vtk.vtkNamedColors()
        self.ren.SetBackground(0.8,0.8,0.8) # you can change the background color here
        
        # Start the vtk screen
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()
        self.iren.Start()
    
    ''' 
        Add a sample vtk object to the visualization window 
    '''
    def add_vtk_object(self):
        # Create a polygonal cylinder model 
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetResolution(8)
        
        # Create a vtk mapper and pass the created cylinder model to it
        cylinderMapper = vtk.vtkPolyDataMapper()
        cylinderMapper.SetInputConnection(cylinder.GetOutputPort())

        # Create a vtk actor and add it to the vtk renderer
        self.cylinderActor = vtk.vtkActor()
        self.cylinderActor.SetMapper(cylinderMapper)
        self.cylinderActor.GetProperty().SetColor(1,0,0)

        self.ren.AddActor(self.cylinderActor)

        # Re-render the object
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
    
    ''' 
        Show a popup message 
    '''
    def show_popup_message(self,msg):
        alert = Qt.QMessageBox()
        alert.setText(msg)
        alert.exec_()
    
    '''
        Add QT controls to the control panel in the righ hand size
    '''
    def add_controls(self):
    
        ''' Add a sample group box '''
        groupBox = Qt.QGroupBox("QT control panel") # Use a group box to group controls
        groupBox_layout = Qt.QVBoxLayout() #lines up the controls vertically
        groupBox.setLayout(groupBox_layout) 
        self.right_panel_layout.addWidget(groupBox)
        
        ''' This is a sample label '''
        label = Qt.QLabel("Sample Label - Add some texts below and click the submit button:")
        groupBox_layout.addWidget(label)
        
        ''' Add a text field ( QLineEdit) and a button. Place them in horizontally '''
        hbox = Qt.QHBoxLayout() # horizontal layout
        self.qt_textfield = Qt.QLineEdit() # create text field
        hbox.addWidget(self.qt_textfield) 
        
        
        self.qt_submit_button = Qt.QPushButton('Submit') #create a button
        self.qt_submit_button.clicked.connect(self.on_submit_clicked)
        self.qt_submit_button.show()
        hbox.addWidget(self.qt_submit_button)
        
        ''' Add the text field and the submit button to a widget so that we can add it to the group box '''
        sample_widget = Qt.QWidget()
        sample_widget.setLayout(hbox)
        groupBox_layout.addWidget(sample_widget)
        
        
        ''' Add a combo box to select different color '''
        groupBox_layout.addWidget(Qt.QLabel("Select a color:"))
        self.qt_color_scheme = Qt.QComboBox()
        self.qt_color_scheme.addItem("Red")
        self.qt_color_scheme.addItem("Green")
        self.qt_color_scheme.addItem("Blue")
        self.qt_color_scheme.currentIndexChanged.connect(self.change_color_scheme)
        groupBox_layout.addWidget(self.qt_color_scheme)
        
        
        ''' Add a spinbox '''
        self.label_spinbox = Qt.QLabel()
        groupBox_layout.addWidget(self.label_spinbox)
        self.qt_spinbox = Qt.QDoubleSpinBox()
        self.qt_spinbox.valueChanged.connect(self.on_spinbox_change)
        groupBox_layout.addWidget(self.qt_spinbox)
        self.label_spinbox.setText("Spin Box Value:"+str(self.qt_spinbox.value()))
        
        ''' Add a slider '''
        self.label_slider = Qt.QLabel()
        groupBox_layout.addWidget(self.label_slider)
        self.qt_slider = Qt.QSlider(QtCore.Qt.Horizontal)
        self.qt_slider.valueChanged.connect(self.on_slider_change)
        groupBox_layout.addWidget(self.qt_slider)
        self.label_slider.setText("Slider Value Value:"+str(self.qt_slider.value()))
        
        ''' Add radio buttons '''
        self.label_radio = Qt.QLabel()
        groupBox_layout.addWidget(self.label_radio)
        self.qt_radio1 = Qt.QRadioButton("Option 1")
        self.qt_radio1.setChecked(True)
        self.label_radio.setText("Selected Radio Value: "+str(self.qt_radio1.text()))
        self.qt_radio1.toggled.connect(self.on_radio_change)
        groupBox_layout.addWidget(self.qt_radio1)
        
        self.qt_radio2 = Qt.QRadioButton("Option 2")
        self.qt_radio2.toggled.connect(self.on_radio_change)
        groupBox_layout.addWidget(self.qt_radio2)
        
        ''' Add checkbox buttons'''
        self.label_checkbox = Qt.QLabel()
        groupBox_layout.addWidget(self.label_checkbox)
        self.qt_checkbox1 = Qt.QCheckBox("Checkbox 1")
        self.qt_checkbox1.setChecked(True)
        self.label_checkbox.setText("Selected Checkbox Value: "+str(self.qt_checkbox1.text()))
        self.qt_checkbox1.toggled.connect(self.on_checkbox_change)
        groupBox_layout.addWidget(self.qt_checkbox1)
        
        self.qt_checkbox2 = Qt.QCheckBox("Checkbox 2")
        self.qt_checkbox2.toggled.connect(self.on_checkbox_change)
        groupBox_layout.addWidget(self.qt_checkbox2)
    
    ''' Handle the click event for the submit button  '''
    def on_submit_clicked(self):
        self.show_popup_message(self.qt_textfield.text())
    
    ''' Handle the spinbox event '''
    def on_spinbox_change(self, value):
        self.label_spinbox.setText("Spin Box Value:"+str(value))
        
    ''' Handle the slider event '''
    def on_slider_change(self, value):
        self.label_slider.setText("Slider Value Value:"+str(self.qt_slider.value()))
    
    ''' Handle the radio button event '''
    def on_radio_change(self):
        if self.qt_radio1.isChecked() == True:
            self.label_radio.setText("Selected Radio Value: "+str(self.qt_radio1.text()))
        elif self.qt_radio2.isChecked() == True:
            self.label_radio.setText("Selected Radio Value: "+str(self.qt_radio2.text()))
     
    ''' Handle the checkbox button event '''
    def on_checkbox_change(self):
        checkbox_message = ""
        if self.qt_checkbox1.isChecked() == True:
            checkbox_message = checkbox_message + "Checkbox 1 is selected"
            
        if self.qt_checkbox2.isChecked() == True:
            checkbox_message = checkbox_message + " Checkbox 2 is selected"
        
        self.label_checkbox.setText("Selected Checkbox Value: "+checkbox_message)

        
    ''' Change color scheme '''    
    def change_color_scheme(self,selected_option):
        
        if selected_option==0: 
            self.cylinderActor.GetProperty().SetColor(1,0,0) # Red
        elif selected_option==1:
            self.cylinderActor.GetProperty().SetColor(0,1,0) # Green
        else:
            self.cylinderActor.GetProperty().SetColor(0,0,1) # Blue
            
        # Re-render the object
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

    



if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
