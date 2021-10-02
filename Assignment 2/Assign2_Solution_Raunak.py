# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 06:24:11 2021

@author: Raunak Sarbajna
"""


import sys
import vtk
import math
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
        self.setWindowTitle("COSC 6344 Visualization – Assignment 2, Raunak Sarbajna")
        self.resize(1000,self.height())
        self.frame = Qt.QFrame() # Create a main window frame to add ui widgets
        self.mainLayout = Qt.QHBoxLayout()  # Set layout - Lines up widgets horizontally
        self.frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.frame)
        

        
        ''' Step 3: Add the control panel to the right hand side of the central widget '''
        # Note: To add a widget, we first need to create a widget, then set the layout for it
        self.right_panel_widget = Qt.QWidget() # create a widget
        self.right_panel_layout = Qt.QVBoxLayout() # set layout - lines up the controls vertically
        self.right_panel_widget.setLayout(self.right_panel_layout) #assign the layout to the widget
        self.mainLayout.addWidget(self.right_panel_widget) # now, add it the the central frame
        
        # The controls will be added here
        self.add_controls()

        ''' Step 2: Add a vtk widget to the central widget '''
        # As we use QHBoxLayout, the vtk widget will be automatically moved to the left
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.mainLayout.addWidget(self.vtkWidget)
        
        #Initialize the vtk variables for the visualization tasks
        self.init_vtk_widget()
        
        # Add an object to the rendering window
        #self.add_vtk_object()


 

    '''
        Initialize the vtk variables for the visualization tasks
    '''    
    def init_vtk_widget(self):
        vtk.vtkObject.GlobalWarningDisplayOff() #Disable vtkOutputWindow - Comment out this line if you want to see the warning/error messages from vtk
        
        # Create the graphics structure. The renderer renders into the render
        # window. The render window interactor captures mouse events and will
        # perform appropriate camera or actor manipulation depending on the
        # nature of the events.
        self.vtk_poly_mapper = vtk.vtkPolyDataMapper()
        self.lut = vtk.vtkLookupTable()
        self.ren = vtk.vtkRenderer() 
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        colors = vtk.vtkNamedColors()
        self.ren.SetBackground(colors.GetColor3d("White")) # you can change the background color here
        
        # Start the vtk screen
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()
        self.iren.Start()
    
    ''' 
        Add a sample vtk object to the visualization window 
    '''
    def add_vtk_object(self):

        ''' Step 2: Read and verify the vtk input file '''
        self.vtk_reader = vtk.vtkDataSetReader()
        self.vtk_reader.SetFileName(self.filename)
        self.vtk_reader.Update()
        
        # Verify
        if self.vtk_reader.IsFileStructuredGrid() \
        or self.vtk_reader.IsFileUnstructuredGrid() \
        or self.vtk_reader.IsFilePolyData():
            self.show_popup_message('Data file loaded successfully!')
        else:
            self.show_popup_message('Cannot read the input file!')

        ''' Step 3 Use geometry filter to get the geometry representation  '''
        vtk_geometry = vtk.vtkGeometryFilter()
        if self.vtk_reader.IsFileStructuredGrid():
            vtk_geometry.SetInputData(self.vtk_reader.GetStructuredGridOutput())
            vtk_geometry.Update()
        elif self.vtk_reader.IsFileUnstructuredGrid():
            vtk_geometry.SetInputData(self.vtk_reader.GetUnstructuredGridOutput())
            vtk_geometry.Update()
        
        
        ''' Step 4: Get the scalar field '''
        
        # For all data of assignment 2, the scalar field has a name "s"
        self.scalar_field = "s"
        
        # Verify the name of the scalar field, and then get the min, max scalar values
        try:
            if not self.vtk_reader.IsFilePolyData():
                self.min_scalar,self.max_scalar = vtk_geometry.GetOutput().GetPointData().GetArray(self.scalar_field).GetRange()
            else:
                self.min_scalar,self.max_scalar = self.vtk_reader.GetPolyDataOutput().GetPointData().GetArray(self.scalar_field).GetRange()

            # print(self.max_scalar, self.min_scalar)
            self.max_label.setText("Max Scalar Values: "+str(self.max_scalar))
            self.min_label.setText("Min Scalar Values: "+str(self.min_scalar))
        except Exception as inst:
            self.show_popup_message('Cannot find the inputed scalar field!')
            # self.show_popup_message(inst)

        ''' Step 5: Use vtkPolyDataMapper (or vtkDataSetMapper) to visualize the scalar data '''
    
        # The mapper is responsible for pushing the geometry into the graphics
        # library. It may also do color mapping, if scalars or other
        # attributes are defined.
        if not self.vtk_reader.IsFilePolyData():
            self.vtk_poly_mapper.SetInputData(vtk_geometry.GetOutput()) 
            # You can also use .SetInputConnection and .GetOutputPort() here
        else:
            self.vtk_poly_mapper.SetInputData(self.vtk_reader.GetPolyDataOutput())
            print("it's polydata")
            
        #Create vtk color lookup table and use it for the color mapping
        
        color_scheme = 0
        MakeLUT(color_scheme, self.lut)
        self.vtk_poly_mapper.SetScalarModeToUsePointData()
        self.vtk_poly_mapper.SetLookupTable(self.lut)
        self.vtk_poly_mapper.SetScalarRange(self.min_scalar, self.max_scalar) #Specify range in terms of scalar minimum and maximum (smin,smax). These values are used to map scalars into lookup table
        self.vtk_poly_mapper.SelectColorArray(self.scalar_field)

        self.vtk_actor = vtk.vtkActor()
        self.vtk_actor.SetMapper(self.vtk_poly_mapper)
        self.ren.AddActor(self.vtk_actor)

        '''
            Contour Mapping
        '''

        self.scalar_threshold = (self.min_scalar + self.max_scalar) / 2
        self.k = 8

        # self.vtk_contour = vtk.vtkContourFilter()
        # self.vtk_contour.SetInputData( self.vtk_reader.GetPolyDataOutput() )
        # # self.vtk_contour.SetValue( 0, self.scalar_threshold ) 
        # self.vtk_contour.GenerateValues(8, self.min_scalar, self.max_scalar)

        

        # # Take the isosurface data and create geometry
        # self.vtk_contour_mapper = vtk.vtkPolyDataMapper()
        # self.vtk_contour_mapper.SetInputConnection( self.vtk_contour.GetOutputPort() )
        # self.vtk_contour_mapper.SetScalarRange(self.min_scalar, self.max_scalar)
        # self.vtk_contour_mapper.ScalarVisibilityOff()

        

        # # Create an actor for the contour mapper.
        # self.vtk_contour_actor = vtk.vtkActor() 
        # self.vtk_contour_actor.SetMapper( self.vtk_contour_mapper )
        
        # # The following set the color and thickness of the contours
        # colors = vtk.vtkNamedColors()
        # self.vtk_contour_actor.GetProperty().SetColor(colors.GetColor3d("Black"))
        # self.vtk_contour_actor.GetProperty().SetLineWidth(2)

        # self.ren.AddActor(self.vtk_contour_actor)

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
        Add QT controls to the control panel in the left side
    '''
    def add_controls(self):
    
        ''' Add a sample group box '''
        groupBox = Qt.QGroupBox("Scalar Field Visualization Controller") # Use a group box to group controls
        groupBox_layout = Qt.QVBoxLayout() #lines up the controls vertically
        groupBox.setLayout(groupBox_layout) 
        self.right_panel_layout.addWidget(groupBox)
        
        ''' This is a sample label '''
        label = Qt.QLabel("Select a VTK file:")
        groupBox_layout.addWidget(label)
        self.filename = ""
        
        ''' Add a text field ( QLineEdit) and a button. Place them in horizontally '''
        hbox = Qt.QHBoxLayout() # horizontal layout
        self.fname_label = Qt.QLabel()
        hbox.addWidget(self.fname_label)
        
        
        self.qt_submit_button = Qt.QPushButton('Browse') #create a button
        self.qt_submit_button.clicked.connect(self.openFileNameDialog)
        self.qt_submit_button.show()

        
        hbox.addWidget(self.qt_submit_button)

        
        ''' Add the text field and the submit button to a widget so that we can add it to the group box '''
        sample_widget = Qt.QWidget()
        sample_widget.setLayout(hbox)
        groupBox_layout.addWidget(sample_widget)

        labelbox = Qt.QHBoxLayout() # horizontal layout
        self.max_label = Qt.QLabel()
        self.min_label = Qt.QLabel()
        labelbox.addWidget(self.max_label)
        labelbox.addWidget(self.min_label)
        label_widget = Qt.QWidget()
        label_widget.setLayout(labelbox)
        groupBox_layout.addWidget(label_widget)
        
        
        ''' Add a combo box to select different color '''
        groupBox_layout.addWidget(Qt.QLabel("Select a Colour Scheme:"))
        self.qt_color_scheme = Qt.QComboBox()
        self.qt_color_scheme.addItem("Rainbow")
        self.qt_color_scheme.addItem("BWR")
        self.qt_color_scheme.addItem("Heatmap")
        self.qt_color_scheme.currentIndexChanged.connect(self.change_color_scheme)
        groupBox_layout.addWidget(self.qt_color_scheme)

        ''' Add radio buttons '''
        self.label_radio = Qt.QLabel()
        groupBox_layout.addWidget(self.label_radio)
        self.qt_radio1 = Qt.QRadioButton("Single Iso-contour (Default threshold is middle of range)")
        self.qt_radio1.setChecked(True)
        self.label_radio.setText("Current Iso-contour status: "+str(self.qt_radio1.text()))
        self.qt_radio1.toggled.connect(self.on_radio_change)
        groupBox_layout.addWidget(self.qt_radio1)
        
        self.qt_radio2 = Qt.QRadioButton("Multiple Iso-Contour (Default number is 8)")
        self.qt_radio2.toggled.connect(self.on_radio_change)
        groupBox_layout.addWidget(self.qt_radio2)
        
        
        ''' This is a sample label '''
        label = Qt.QLabel("Update Iso-Counter threshold:")
        groupBox_layout.addWidget(label)
        
        ''' Add a text field ( QLineEdit) and a button. Place them in horizontally '''
        hbox = Qt.QHBoxLayout() # horizontal layout
        self.qt_textfield = Qt.QLineEdit() # create text field
        self.qt_textfield.setValidator(Qt.QDoubleValidator())
        self.qt_textfield.setText("0.0")
        hbox.addWidget(self.qt_textfield) 
        
        
        self.qt_submit_button = Qt.QPushButton('Update all Iso-Contour') #create a button
        self.qt_submit_button.clicked.connect(self.on_submit_clicked)
        self.qt_submit_button.show()
        hbox.addWidget(self.qt_submit_button)
        
        ''' Add the text field and the submit button to a widget so that we can add it to the group box '''
        sample_widget = Qt.QWidget()
        sample_widget.setLayout(hbox)
        groupBox_layout.addWidget(sample_widget)
        
        ''' Add a slider '''
        self.label_slider = Qt.QLabel()
        groupBox_layout.addWidget(self.label_slider)
        self.qt_slider = Qt.QSlider(QtCore.Qt.Horizontal)
        self.qt_slider.setMinimum(1)
        self.qt_slider.setMaximum(50)
        self.qt_slider.setValue(8)
        self.qt_slider.setTickPosition(Qt.QSlider.TicksBelow)
        self.qt_slider.setTickInterval(2)
        self.qt_slider.valueChanged.connect(self.on_slider_change)
        groupBox_layout.addWidget(self.qt_slider)
        self.label_slider.setText("Number of Iso-Counters:"+str(self.qt_slider.value()))
        

        
        # ''' Add checkbox buttons'''
        # self.label_checkbox = Qt.QLabel()
        # groupBox_layout.addWidget(self.label_checkbox)
        # self.qt_checkbox1 = Qt.QCheckBox("Checkbox 1")
        # self.qt_checkbox1.setChecked(True)
        # self.label_checkbox.setText("Selected Checkbox Value: "+str(self.qt_checkbox1.text()))
        # self.qt_checkbox1.toggled.connect(self.on_checkbox_change)
        # groupBox_layout.addWidget(self.qt_checkbox1)
        
        # self.qt_checkbox2 = Qt.QCheckBox("Checkbox 2")
        # self.qt_checkbox2.toggled.connect(self.on_checkbox_change)
        # groupBox_layout.addWidget(self.qt_checkbox2)
    
    ''' Handle the click event for the submit button  '''
    def on_submit_clicked(self):
        self.scalar_threshold = float(self.qt_textfield.text())
        try:
            self.ren.RemoveActor(self.vtk_contour_actor)
        except:
            print("tried to delete an actor who hasn't been created yet")
        if self.qt_radio1.isChecked() == True:
            self.single_iso()
        elif self.qt_radio2.isChecked() == True:
            self.k_iso() 
    
        
    ''' Handle the slider event '''
    def on_slider_change(self, value):
        self.k = self.qt_slider.value()
        self.label_slider.setText("Slider Value Value:"+str(self.qt_slider.value()))
    
    ''' Handle the radio button event '''
    def on_radio_change(self):
        if self.qt_radio1.isChecked() == True:
            self.label_radio.setText("Current Iso-contour status: "+str(self.qt_radio1.text()))
        elif self.qt_radio2.isChecked() == True:
            self.label_radio.setText("Current Iso-contour status: "+str(self.qt_radio2.text()))     

        
    ''' Change color scheme '''    
    def change_color_scheme(self,selected_option):
        
        MakeLUT(selected_option, self.lut)
        self.vtk_poly_mapper.SetScalarModeToUsePointData()
        self.vtk_poly_mapper.SetLookupTable(self.lut)
        self.vtk_poly_mapper.SetScalarRange(self.min_scalar, self.max_scalar) #Specify range in terms of scalar minimum and maximum (smin,smax). These values are used to map scalars into lookup table
        self.vtk_poly_mapper.SelectColorArray(self.scalar_field)
        self.vtk_actor.SetMapper(self.vtk_poly_mapper)
            
        # Re-render the object
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
    
    '''
        Add file input dialog box
    '''
    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QtWidgets.QFileDialog.getOpenFileName()", ".","VTK Files (*.vtk)", options=options)
        if fname:
            self.filename = fname
            self.fname_label.setText(fname)

        self.add_vtk_object()

    def single_iso(self):
        self.vtk_contour = vtk.vtkContourFilter()
        self.vtk_contour.SetInputData( self.vtk_reader.GetPolyDataOutput() )
        self.vtk_contour.SetValue( 0, self.scalar_threshold ) 

        # Take the isosurface data and create geometry
        self.vtk_contour_mapper = vtk.vtkPolyDataMapper()
        self.vtk_contour_mapper.SetInputConnection( self.vtk_contour.GetOutputPort() )
        self.vtk_contour_mapper.SetScalarRange(self.min_scalar, self.max_scalar)
        self.vtk_contour_mapper.ScalarVisibilityOff()

        

        # Create an actor for the contour mapper.
        self.vtk_contour_actor = vtk.vtkActor() 
        self.vtk_contour_actor.SetMapper( self.vtk_contour_mapper )
        
        # The following set the color and thickness of the contours
        colors = vtk.vtkNamedColors()
        self.vtk_contour_actor.GetProperty().SetColor(colors.GetColor3d("Black"))
        self.vtk_contour_actor.GetProperty().SetLineWidth(2)

        self.ren.AddActor(self.vtk_contour_actor)

        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()


    def k_iso(self):
        self.vtk_contour = vtk.vtkContourFilter()
        self.vtk_contour.SetInputData( self.vtk_reader.GetPolyDataOutput() )
        self.vtk_contour.GenerateValues(self.k, self.min_scalar, self.max_scalar)

        

        # Take the isosurface data and create geometry
        self.vtk_contour_mapper = vtk.vtkPolyDataMapper()
        self.vtk_contour_mapper.SetInputConnection( self.vtk_contour.GetOutputPort() )
        self.vtk_contour_mapper.SetScalarRange(self.min_scalar, self.max_scalar)
        self.vtk_contour_mapper.ScalarVisibilityOff()

        

        # Create an actor for the contour mapper.
        self.vtk_contour_actor = vtk.vtkActor() 
        self.vtk_contour_actor.SetMapper( self.vtk_contour_mapper )
        
        # The following set the color and thickness of the contours
        colors = vtk.vtkNamedColors()
        self.vtk_contour_actor.GetProperty().SetColor(colors.GetColor3d("Black"))
        self.vtk_contour_actor.GetProperty().SetLineWidth(2)

        self.ren.AddActor(self.vtk_contour_actor)

        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()

        

        
'''
    Create a color lookup table by using three different color map schemes
        @input: colorScheme = 0,1 or 2
                lut - vtkLookupTable
    References: 
        https://lorensen.github.io/VTKExamples/site/Python/VisualizationAlgorithms/DisplacementPlot/
        https://lorensen.github.io/VTKExamples/site/Python/Visualization/AssignCellColorsFromLUT/
'''
def MakeLUT(colorScheme, lut):
    # See: [Diverging Color Maps for Scientific Visualization]
    #      (http:#www.kennethmoreland.com/color-maps/)
    
    nc = 1024 #interpolate 256 values, increase this to get more colors
    # The min scalar value is mapped to 0, and the max value is mapped to 1
    sMin = 0.
    sMax = 1.

    if colorScheme == 0: # rainbow
        
        lut.SetNumberOfTableValues(nc)
        lut.Build()
        
        
        
        hsv = [0.0,1.0,1.0]
        
        for i in range(0, nc):
            s = float(i) / nc #uniformlly interpolate the scalar values
            hsv[0] = 240. - 240. *(s-sMin)/(sMax-sMin)
            rgb = hsvRgb(hsv)
            rgb.append(1.0)  # set alpha (or opacity) channel
            lut.SetTableValue(i, *rgb)

    # Assignment 2: Task 2.1 below
            
    elif colorScheme == 1: # Blue-white-red diverging 
        lut.SetNumberOfTableValues(nc)
        lut.Build()
        
        ''' TODO: complete the blue-white-red color mapping here '''
        
        hsv = [240.0,1.0,1.0]
        
        for i in range(0, int(nc/2)):
            s = float(i) / nc #uniformlly interpolate the scalar values
            hsv[1] = 1. - (s-sMin)/(sMax-sMin)
            rgb = hsvRgb(hsv)
            rgb.append(1.0)  # set alpha (or opacity) channel
            lut.SetTableValue(i, *rgb)
        
        hsv = [0.0,1.0,1.0]
        for i in range(int(nc/2), nc):
            s = float(i) / nc #uniformlly interpolate the scalar values
            hsv[1] = (s-sMin)/(sMax-sMin)
            rgb = hsvRgb(hsv)
            rgb.append(1.0)  # set alpha (or opacity) channel
            lut.SetTableValue(i, *rgb)
        
    elif colorScheme == 2: #Heat-map
        lut.SetNumberOfTableValues(nc)
        lut.Build()
        
        ''' TODO: complete the heat-map color mapping here '''

        ''' Red Channel '''   
        rgba = [0.0,0.0,0.0,1.0]

        for i in range(0, int(nc/3)):
            s = float(i) / nc #uniformlly interpolate the scalar values
            rgba[0] = 3.0 * (s-sMin)/(sMax-sMin)
            lut.SetTableValue(i, *rgba)
        
        ''' Green Channel '''   
        rgba = [1.0,0.0,0.0,1.0]

        for i in range(int(nc/3), int(nc * (2/3))):
            s = float(i) / nc #uniformlly interpolate the scalar values
            rgba[1] = 1.5 * (s-sMin)/(sMax-sMin)
            lut.SetTableValue(i, *rgba)
        
        ''' Blue Channel '''   
        rgba = [1.0,1.0,0.0,1.0]

        for i in range(int(nc * (2/3)), nc):
            s = float(i) / nc #uniformlly interpolate the scalar values
            rgba[2] = 1.0 * (s-sMin)/(sMax-sMin)
            lut.SetTableValue(i, *rgba)
        
        
        
'''
    Convert HSV to RGB color 
'''
def hsvRgb(hsv):
    rgb = [0,0,0]
    #h, s, v      - hue, sat, value
    #r, g, b      - red, green, blue
    #i, f, p, q, t   - interim values


    # guarantee valid input:
    h = hsv[0] / 60.
    while h >= 6.:
        h -= 6.
    while h < 0.:
        h += 6.

    s = hsv[1]
    if (s < 0.):
        s = 0.
    if (s > 1.):
        s = 1.

    v = hsv[2]
    if (v < 0.):
        v = 0.
    if (v > 1.):
        v = 1.


    # if sat==0, then is a gray:
    if s == 0.0:
        rgb[0] = rgb[1] = rgb[2] = v
        return rgb
    


    # get an rgb from the hue itself:

    i = math.floor(h)
    f = h - i
    p = v * (1. - s)
    q = v * (1. - s * f)
    t = v * (1. - (s * (1. - f)))

    if math.floor(i) == 0:
      r = v
      g = t
      b = p
      

    elif math.floor(i) == 1:
      r = q
      g = v
      b = p
      

    elif math.floor(i) == 2:
      r = p
      g = v
      b = t
      

    elif math.floor(i) == 3:
      r = p
      g = q 
      b = v
      

    elif math.floor(i) == 4:
      r = t
      g = p
      b = v
      

    elif math.floor(i) == 5:
      r = v
      g = p 
      b = q
      
    rgb[0] = r
    rgb[1] = g
    rgb[2] = b

    return rgb
    



if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
