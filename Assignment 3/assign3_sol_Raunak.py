# -*- coding: utf-8 -*-
"""
Created on Sun Oct 3 08:15:11 2021

@author: Raunak Sarbajna
"""


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
        self.setWindowTitle("COSC 6344 Visualization YOUR NAME")
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
        # self.add_vtk_object()
        
        ''' Step 3: Add the control panel to the right hand side of the central widget '''
        # Note: To add a widget, we first need to create a widget, then set the layout for it
        self.right_panel_widget = Qt.QWidget() # create a widget
        self.right_panel_layout = Qt.QVBoxLayout() # set layout - lines up the controls vertically
        self.right_panel_widget.setLayout(self.right_panel_layout) #assign the layout to the widget
        self.mainLayout.addWidget(self.right_panel_widget) # now, add it to the central frame
        
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
        self.ren.SetBackground(colors.GetColor3d("White")) # you can change the background color here

        # Start by creating a black/white lookup table.
        self.bwLut = vtk.vtkLookupTable()
        # YOU need adjust the following range to address the dynamic range issue!
        self.bwLut.SetTableRange(0, 2)
        self.bwLut.SetSaturationRange(0, 0)
        self.bwLut.SetHueRange(0, 0)
        self.bwLut.SetValueRange(0, 1)
        self.bwLut.Build()  # effective built
 

        # Start the vtk screen
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()
        self.iren.Start()

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
        groupBox = Qt.QGroupBox("3D Scalar Field Visualization") # Use a group box to group controls
        groupBox_layout = Qt.QVBoxLayout() #lines up the controls vertically
        groupBox.setLayout(groupBox_layout) 
        self.right_panel_layout.addWidget(groupBox)
  
        ''' Add a textfield ( QLineEdit) to show the file path and the browser button '''
        label = Qt.QLabel("Choose a file (e.g., vtk):")
        groupBox_layout.addWidget(label)
        hbox = Qt.QHBoxLayout()
        self.qt_file_name = Qt.QLineEdit()
        hbox.addWidget(self.qt_file_name) 
        self.qt_browser_button = Qt.QPushButton('Browser')
        self.qt_browser_button.clicked.connect(self.on_file_browser_clicked)
        self.qt_browser_button.show()
        hbox.addWidget(self.qt_browser_button)
        file_widget = Qt.QWidget()
        file_widget.setLayout(hbox)
        groupBox_layout.addWidget(file_widget)
 
        ''' Add the Open button '''
        self.qt_open_button = Qt.QPushButton('Open')
        self.qt_open_button.clicked.connect(self.open_vtk_file)
        self.qt_open_button.show()
        groupBox_layout.addWidget(self.qt_open_button)
  
        ''' Add the min, max scalar labels '''
        self.qt_min_lable = Qt.QLabel("Min Scalar: 0")
        self.qt_max_lable = Qt.QLabel("Max Scalar: 0")
        groupBox_layout.addWidget(self.qt_min_lable)
        groupBox_layout.addWidget(self.qt_max_lable)
        
        ''' Add spinbox for scalar threshold selection '''
        hbox =  Qt.QHBoxLayout()
        self.qt_isoSurf_checkbox = Qt.QCheckBox("Show iso-surface (select threshold)")
        hbox.addWidget(self.qt_isoSurf_checkbox)
        self.qt_isoSurf_checkbox.setChecked(False)
        self.qt_isoSurf_checkbox.toggled.connect(self.on_checkbox_change)
        self.qt_iso_threshold = Qt.QDoubleSpinBox()
        hbox.addWidget(self.qt_iso_threshold)

        ''' Add the Show Iso-Surface button '''
        self.qt_show_iso_button = Qt.QPushButton('Show')
        self.qt_show_iso_button.clicked.connect(self.extract_one_isosurface)
        self.qt_show_iso_button.show()
        hbox.addWidget(self.qt_show_iso_button)
        isoSurf_hwidget = Qt.QWidget()
        isoSurf_hwidget.setLayout(hbox)
        groupBox_layout.addWidget(isoSurf_hwidget)



        groupBox_layout.addWidget(Qt.QLabel("3D cut planes:"))
        ''' Add a slider bar for XY slicing plane '''
        hbox_xy =  Qt.QHBoxLayout()
        self.qt_xy_plane_checkbox = Qt.QCheckBox("Show XY Cut Plane")
        self.qt_xy_plane_checkbox.setChecked(False)
        self.qt_xy_plane_checkbox.toggled.connect(self.on_checkbox_change)
        hbox_xy.addWidget(self.qt_xy_plane_checkbox)

        

        self.qt_zslider = Qt.QSlider(QtCore.Qt.Horizontal)
        self.qt_zslider.valueChanged.connect(self.on_zslider_change)
        hbox_xy.addWidget(self.qt_zslider)
        self.label_zslider = Qt.QLabel()
        hbox_xy.addWidget(self.label_zslider)
        self.label_zslider.setText("Z index:"+str(self.qt_zslider.value()))
        z_slider_widget = Qt.QWidget()
        z_slider_widget.setLayout(hbox_xy)
        groupBox_layout.addWidget(z_slider_widget)
        
        ''' XZ Cut Plane '''

        hbox_xz =  Qt.QHBoxLayout()
        self.qt_xz_plane_checkbox = Qt.QCheckBox("Show XZ Cut Plane")
        self.qt_xz_plane_checkbox.setChecked(False)
        self.qt_xz_plane_checkbox.toggled.connect(self.on_checkbox_change)
        hbox_xz.addWidget(self.qt_xz_plane_checkbox)

        self.qt_yslider = Qt.QSlider(QtCore.Qt.Horizontal)
        self.qt_yslider.valueChanged.connect(self.on_yslider_change)
        hbox_xz.addWidget(self.qt_yslider)
        self.label_yslider = Qt.QLabel()
        hbox_xz.addWidget(self.label_yslider)
        self.label_yslider.setText("Y index:"+str(self.qt_yslider.value()))
        y_slider_widget = Qt.QWidget()
        y_slider_widget.setLayout(hbox_xz)
        groupBox_layout.addWidget(y_slider_widget)

        ''' YZ Cut Plane '''
        
        hbox_yz =  Qt.QHBoxLayout()
        self.qt_yz_plane_checkbox = Qt.QCheckBox("Show YZ Cut Plane")
        self.qt_yz_plane_checkbox.setChecked(False)
        self.qt_yz_plane_checkbox.toggled.connect(self.on_checkbox_change)
        hbox_yz.addWidget(self.qt_yz_plane_checkbox)


        self.qt_xslider = Qt.QSlider(QtCore.Qt.Horizontal)
        self.qt_xslider.valueChanged.connect(self.on_xslider_change)
        hbox_yz.addWidget(self.qt_xslider)
        self.label_xslider = Qt.QLabel()
        hbox_yz.addWidget(self.label_xslider)
        self.label_xslider.setText("X index:"+str(self.qt_xslider.value()))
        x_slider_widget = Qt.QWidget()
        x_slider_widget.setLayout(hbox_yz)
        groupBox_layout.addWidget(x_slider_widget)



        groupBox_layout.addWidget(Qt.QLabel("Raycasting:"))
        
        hbox =  Qt.QHBoxLayout()
        self.qt_dvr_checkbox = Qt.QCheckBox("Show Volume Rendering: ")
        self.qt_dvr_checkbox.setChecked(False)
        self.qt_dvr_checkbox.toggled.connect(self.on_checkbox_change)
        hbox.addWidget(self.qt_dvr_checkbox)             
        qt_volWidget = Qt.QWidget()
        qt_volWidget.setLayout(hbox)
        
        groupBox_layout.addWidget(qt_volWidget)
        
        
    def on_file_browser_clicked(self):
        dlg = Qt.QFileDialog()
        dlg.setFileMode(Qt.QFileDialog.AnyFile)
        dlg.setNameFilter("loadable files (*.vtk *.mhd)")
        
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.qt_file_name.setText(filenames[0])
    
    def open_vtk_file(self):
        '''Read and verify the vtk input file '''
        input_file_name = self.qt_file_name.text()
        
        if ".mhd" in input_file_name: #The input file is MetaImageData
            self.input_type = "mhd"
            self.reader = vtk.vtkMetaImageReader()
            self.reader.SetFileName(input_file_name)
            self.reader.Update()
        elif ".vtk" in input_file_name: # The input file is VTK
            self.input_type = "vtk"
            self.reader = vtk.vtkDataSetReader()
            self.reader.SetFileName(input_file_name)
            self.reader.Update()
                  
        # Some initialization to remove actors that are created previously
        if hasattr(self, 'isoSurf_actor'):
            self.ren.RemoveActor(self.isoSurf_actor)  

        if hasattr(self, 'outline'):
            self.ren.RemoveActor(self.outline) 
        
        if hasattr(self, 'xy_plane'):
            self.ren.RemoveActor(self.xy_plane)

        # You probably need to remove additional actors below...
        if hasattr(self, 'xz_plane'):
            self.ren.RemoveActor(self.xz_plane)
        if hasattr(self, 'yz_plane'):
            self.ren.RemoveActor(self.yz_plane)
            
        
        self.scalar_range = [self.reader.GetOutput().GetScalarRange()[0], self.reader.GetOutput().GetScalarRange()[1]]
        self.qt_min_lable.setText("Min Scalar:"+str(self.scalar_range[0]))
        self.qt_max_lable.setText("Max Scalar:"+str(self.scalar_range[1]))
        self.qt_iso_threshold.setValue((self.scalar_range[0]+self.scalar_range[1])/2)
        
        #Update the lookup table
        # YOU NEED TO UPDATE THE FOLLOWING RANGE BASED ON THE LOADED DATA!!!!
        self.bwLut.SetTableRange(self.scalar_range[0], self.scalar_range[1]/2.)
        self.bwLut.SetSaturationRange(0, 0)
        self.bwLut.SetHueRange(0, 0)
        self.bwLut.SetValueRange(0, 1)
        self.bwLut.Build()  # effective built
        
        self.dim = self.reader.GetOutput().GetDimensions()
        
                
        # set the range for the iso-surface spinner
        self.qt_iso_threshold.setRange(self.scalar_range[0],self.scalar_range[1])
       
        # set the range for the XY cut plane range 
        self.qt_zslider.setRange(0, self.dim[2]-1)
        self.qt_yslider.setRange(0, self.dim[1]-1)
        self.qt_xslider.setRange(0, self.dim[0]-1)


        # Get the data outline
        outlineData = vtk.vtkOutlineFilter()
        outlineData.SetInputConnection(self.reader.GetOutputPort())
        outlineData.Update()

        mapOutline = vtk.vtkPolyDataMapper()
        mapOutline.SetInputConnection(outlineData.GetOutputPort())

        self.outline = vtk.vtkActor()
        self.outline.SetMapper(mapOutline)
        colors = vtk.vtkNamedColors()
        self.outline.GetProperty().SetColor(colors.GetColor3d("Black"))
        self.outline.GetProperty().SetLineWidth(2.)
        
        self.ren.AddActor(self.outline)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()   
        
    ''' You need to complete the following iso surface extraction function '''   
    def extract_one_isosurface(self):
        if hasattr(self, 'isoSurf_actor'):
            self.ren.RemoveActor(self.isoSurf_actor)
            
        if self.qt_isoSurf_checkbox.isChecked() == True:            
            isoSurfExtractor = vtk.vtkMarchingCubes()
            isoSurfExtractor.SetInputConnection(self.reader.GetOutputPort())
            isoSurfExtractor.SetValue(0, self.qt_iso_threshold.value())

            isoSurfStripper = vtk.vtkStripper()
            isoSurfStripper.SetInputConnection(isoSurfExtractor.GetOutputPort())
            isoSurfStripper.Update()

            isoSurf_mapper = vtk.vtkPolyDataMapper()
            isoSurf_mapper.SetInputConnection( isoSurfStripper.GetOutputPort() )
            isoSurf_mapper.ScalarVisibilityOff()

            self.isoSurf_actor = vtk.vtkActor() 
            self.isoSurf_actor.SetMapper( isoSurf_mapper )

            colors = vtk.vtkNamedColors()

            self.isoSurf_actor.GetProperty().SetDiffuseColor(colors.GetColor3d("Orange"))
            self.isoSurf_actor.GetProperty().SetSpecular(.3)
            self.isoSurf_actor.GetProperty().SetSpecularPower(20)

            self.ren.AddActor(self.isoSurf_actor)


       
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()
     

    def on_zslider_change(self, value):
        self.label_zslider.setText("Z index:"+str(self.qt_zslider.value()))
        current_zID = int(self.qt_zslider.value())
        
        if self.qt_xy_plane_checkbox.isChecked() == True:           
            xy_plane_Colors = vtk.vtkImageMapToColors()
            xy_plane_Colors.SetInputConnection(self.reader.GetOutputPort())
            xy_plane_Colors.SetLookupTable(self.bwLut)
            xy_plane_Colors.Update()
            
            if hasattr(self, 'xy_plane'):
                self.ren.RemoveActor(self.xy_plane)
          
    
            self.xy_plane = vtk.vtkImageActor()
            self.xy_plane.GetMapper().SetInputConnection(xy_plane_Colors.GetOutputPort())
            self.xy_plane.SetDisplayExtent(0, self.dim[0], 0, self.dim[1], current_zID, current_zID) # Z
            
            self.ren.AddActor(self.xy_plane)
            
            # Re-render the screen
            self.vtkWidget.GetRenderWindow().Render() 

    def on_yslider_change(self, value):
        self.label_yslider.setText("Y index:"+str(self.qt_yslider.value()))
        current_yID = int(self.qt_yslider.value())
        
        if self.qt_xz_plane_checkbox.isChecked() == True:           
            xz_plane_Colors = vtk.vtkImageMapToColors()
            xz_plane_Colors.SetInputConnection(self.reader.GetOutputPort())
            xz_plane_Colors.SetLookupTable(self.bwLut)
            xz_plane_Colors.Update()
            
            if hasattr(self, 'xz_plane'):
                self.ren.RemoveActor(self.xz_plane)
          
    
            self.xz_plane = vtk.vtkImageActor()
            self.xz_plane.GetMapper().SetInputConnection(xz_plane_Colors.GetOutputPort())
            self.xz_plane.SetDisplayExtent(0, self.dim[0], current_yID, current_yID, 0, self.dim[2] ) # Y
            
            self.ren.AddActor(self.xz_plane)
            
            # Re-render the screen
            self.vtkWidget.GetRenderWindow().Render() 

    def on_xslider_change(self, value):
        self.label_xslider.setText("X index:"+str(self.qt_xslider.value()))
        current_xID = int(self.qt_xslider.value())
        
        if self.qt_yz_plane_checkbox.isChecked() == True:           
            yz_plane_Colors = vtk.vtkImageMapToColors()
            yz_plane_Colors.SetInputConnection(self.reader.GetOutputPort())
            yz_plane_Colors.SetLookupTable(self.bwLut)
            yz_plane_Colors.Update()
            
            if hasattr(self, 'yz_plane'):
                self.ren.RemoveActor(self.yz_plane)
          
    
            self.yz_plane = vtk.vtkImageActor()
            self.yz_plane.GetMapper().SetInputConnection(yz_plane_Colors.GetOutputPort())
            self.yz_plane.SetDisplayExtent(current_xID, current_xID, 0, self.dim[1], 0, self.dim[2] ) # X
            
            self.ren.AddActor(self.yz_plane)
            
            # Re-render the screen
            self.vtkWidget.GetRenderWindow().Render() 

           
    ''' Handle the click event for the submit button  '''
    def on_submit_clicked(self):
        self.show_popup_message(self.qt_textfield.text())
    
    ''' Handle the spinbox event '''
    def on_spinbox_change(self, value):
        self.label_spinbox.setText("Spin Box Value:"+str(value))
            

    ''' You need to complete the following for Raycasting '''
    def comp_raycasting(self):
        # Load the rendering configuration file that contains
        # control points for color and opacity transfer function
        self.load_color_transfer_values()
        
        # The volume will be displayed by ray-cast alpha compositing.
        # A ray-cast mapper is needed to do the ray-casting.
        volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()

    

        # The following added the control points to the color transfer function
        # The control points are loaded from a file
        volumeColor = vtk.vtkColorTransferFunction()
        for colorMap in self.volume_colors:
            volumeColor.AddRGBPoint(colorMap[0], colorMap[1], colorMap[2], colorMap[3])
        
    
        # The following added the control points to the opacity transfer function
        # The control points are loaded from a file
        volumeScalarOpacity = vtk.vtkPiecewiseFunction()
        for opacityMap in self.volume_opacity:
            volumeScalarOpacity.AddPoint(opacityMap[0], opacityMap[1])

    
        # Use gradient information to enhanced DVR
        # volumeGradientOpacity = vtk.vtkPiecewiseFunction()
        # volumeGradientOpacity.AddPoint(0, 0.0)
        # volumeGradientOpacity.AddPoint(90, 0.5)
        # volumeGradientOpacity.AddPoint(100, 1.0)
    
        
        # Next, you should set the volume property
        # 
    
        # Create a vtkVolume object 
        # set its mapper created above and its property.
    
        # Finally, add the volume to the renderer
        self.ren.AddViewProp(self.volume)

     
    ''' Handle the checkbox button event '''
    def on_checkbox_change(self):
          
           
        if self.qt_xy_plane_checkbox.isChecked() == False:    
            if hasattr(self, 'xy_plane'):
                self.ren.RemoveActor(self.xy_plane)
            # Re-render the screen
            self.vtkWidget.GetRenderWindow().Render()
           
        if self.qt_isoSurf_checkbox.isChecked() == False:
            if hasattr(self, 'isoSurf_actor'):
                self.ren.RemoveActor(self.isoSurf_actor)
            # Re-render the screen
            self.vtkWidget.GetRenderWindow().Render()

        if self.qt_dvr_checkbox.isChecked() == False:
            if hasattr(self, 'volume'):
                self.ren.RemoveViewProp(self.volume)
            # Re-render the screen
            self.vtkWidget.GetRenderWindow().Render()
        else:
            if hasattr(self, 'volume'):
                self.ren.RemoveViewProp(self.volume)
            self.comp_raycasting()
            # Re-render the screen
            self.vtkWidget.GetRenderWindow().Render()
            
    '''
        Load the color and opacity transfer values from the configuration file
        The default file name is "rendering_config.txt"
        Here is a sample configuration file:
            #Color
            0, 0.0, 0.0, 0.0
            500, 1.0, 0.5, 0.3
            1000, 1.0, 0.5, 0.3
            1150, 1.0, 1.0, 0.9

            #Opacity
            0, 0.00
            500, 0.15
            1000, 0.15
            1150, 0.85
    '''
    def load_color_transfer_values(self):
        fileName = "rendering_config.txt"
        self.volume_colors = []
        self.volume_opacity = []
        with open(fileName, 'r') as f:
            isLoadColor = False
            isLoadOpacity = False
            for line in f:    
                if len(line)>1:
                    if "#Color" in line:
                        isLoadColor = True
                        continue
                    if "#Opacity" in line:
                        isLoadColor = False
                        isLoadOpacity = True
                        continue
                    
                    line = line.replace("\n",'')
                    line = line.replace(" ",'')
                    line = line.split(",")
                    if isLoadColor:
                        scalar_value = float(line[0])
                        r = float(line[1])
                        g = float(line[2])
                        b = float(line[3])
                        self.volume_colors.append([scalar_value,r,g,b])
                        
                    if isLoadOpacity:
                        scalar_value = float(line[0])
                        opacity = float(line[1])
                        self.volume_opacity.append([scalar_value,opacity])
                        
        #print(self.volume_colors) 
        #print(self.volume_opacity)
        
if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())