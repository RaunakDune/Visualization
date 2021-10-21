# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 08:49:30 2021

@author: Raunak Sarbajna
"""


import sys
import math
import random
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
        self.setWindowTitle("COSC 6344 Visualization - Raunak Sarbajna")
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
        #vtk.vtkObject.GlobalWarningDisplayOff() #Disable vtkOutputWindow - Comment out this line if you want to see the warning/error messages from vtk
        
        # Create the graphics structure. The renderer renders into the render
        # window. The render window interactor captures mouse events and will
        # perform appropriate camera or actor manipulation depending on the
        # nature of the events.
        self.ren = vtk.vtkRenderer() 
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        # The following set the interactor for 2D image style (i.e., no rotation)
        style = vtk.vtkInteractorStyleImage()
        self.iren.SetInteractorStyle(style)
        colors = vtk.vtkNamedColors()
        self.ren.SetBackground(colors.GetColor3d("White")) # you can change the background color here

        # Start the vtk screen
        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()
        self.iren.Start()

    '''
        Add QT controls to the control panel in the righ hand size
    '''
    def add_controls(self):
    
        ''' Add a sample group box '''
        groupBox = Qt.QGroupBox("2D Vector Field Visualization") # Use a group box to group controls
        self.groupBox_layout = Qt.QVBoxLayout() #lines up the controls vertically
        groupBox.setLayout(self.groupBox_layout) 
        self.right_panel_layout.addWidget(groupBox)
  
        ''' Add a textfield ( QLineEdit) to show the file path and the browser button '''
        label = Qt.QLabel("Choose a file (e.g., vtk):")
        self.groupBox_layout.addWidget(label)
        hbox = Qt.QHBoxLayout()
        self.qt_file_name = Qt.QLineEdit()
        hbox.addWidget(self.qt_file_name) 
        self.qt_browser_button = Qt.QPushButton('Browser')
        self.qt_browser_button.clicked.connect(self.on_file_browser_clicked)
        self.qt_browser_button.show()
        hbox.addWidget(self.qt_browser_button)
        file_widget = Qt.QWidget()
        file_widget.setLayout(hbox)
        self.groupBox_layout.addWidget(file_widget)
 
        ''' Add the Open button '''
        self.qt_open_button = Qt.QPushButton('Open')
        self.qt_open_button.clicked.connect(self.open_vtk_file)
        self.qt_open_button.show()
        self.groupBox_layout.addWidget(self.qt_open_button)
      
        ''' Add the widgets for arrow plot '''
        hbox_arrowplot = Qt.QHBoxLayout()
        self.qt_arrow_checkbox = Qt.QCheckBox("Arrow Plot ")
        self.qt_arrow_checkbox.setChecked(False)
        self.qt_arrow_checkbox.toggled.connect(self.on_arrow_checkbox_change)  
        hbox_arrowplot.addWidget(self.qt_arrow_checkbox)

        arrowscaleLabel = Qt.QLabel("    Choose arrow scale:")
        hbox_arrowplot.addWidget(arrowscaleLabel)
        self.arrow_scale = Qt.QDoubleSpinBox()
         # set the initial values of some parameters
        self.arrow_scale.setValue(0.03)
        self.arrow_scale.setRange(0, 1)
        self.arrow_scale.setSingleStep (0.01)
        hbox_arrowplot.addWidget(self.arrow_scale)

        maxPointsLabel = Qt.QLabel("Choose Maximum Number of Arrows:")
        hbox_arrowplot.addWidget(maxPointsLabel)
        self.max_points = Qt.QDoubleSpinBox()
         # set the initial values of some parameters
        self.max_points.setValue(500)
        self.max_points.setRange(200, 10000)
        self.max_points.setSingleStep (100)
        hbox_arrowplot.addWidget(self.max_points)

        arrow_widget = Qt.QWidget()
        arrow_widget.setLayout(hbox_arrowplot)
        self.groupBox_layout.addWidget(arrow_widget)


        vbox_streamline = Qt.QVBoxLayout()
        hbox_streamline = Qt.QHBoxLayout()
        self.qt_streamline_checkbox = Qt.QCheckBox("Streamline ")
        self.qt_streamline_checkbox.setChecked(False)
        self.qt_streamline_checkbox.toggled.connect(self.on_streamline_checkbox_change)
        hbox_streamline.addWidget(self.qt_streamline_checkbox) 
        seedLabel = Qt.QLabel("    Set number of seeds:")
        hbox_streamline.addWidget(seedLabel)
        self.number_seeds = Qt.QDoubleSpinBox()
         # set the initial values of some parameters
        self.number_seeds.setValue(10)
        self.number_seeds.setRange(1, 2000)
        self.number_seeds.setSingleStep (1)
        hbox_streamline.addWidget(self.number_seeds)
        streamline_hwidget = Qt.QWidget()
        streamline_hwidget.setLayout(hbox_streamline)
        #self.groupBox_layout.addWidget(streamline_widget)
        vbox_streamline.addWidget(streamline_hwidget)
     
        vbox_seed_strategy = Qt.QVBoxLayout()
        # Add radio buttons for the selection of the seed generation strategy
        self.uniform_seed_radio = Qt.QRadioButton("Uniform Seeding")
        self.uniform_seed_radio.setChecked(True)
        self.uniform_seed_radio.toggled.connect(self.on_seeding_strategy)
        vbox_seed_strategy.addWidget(self.uniform_seed_radio)

        self.random_seed_radio = Qt.QRadioButton("Random Seeding")
        self.random_seed_radio.setChecked(False)
        self.random_seed_radio.toggled.connect(self.on_seeding_strategy)
        vbox_seed_strategy.addWidget(self.random_seed_radio)
        self.seeding_strategy = 0 # Uniform seeding is the default strategy 

        seedingstrategy = Qt.QWidget()
        seedingstrategy.setLayout(vbox_seed_strategy)
        vbox_streamline.addWidget(seedingstrategy)

        streamline_widgets = Qt.QWidget()
        streamline_widgets.setLayout(vbox_streamline)
        self.groupBox_layout.addWidget(streamline_widgets)
        

        ''' Add widgets for LIC '''

        maxIntLen = Qt.QLabel("Choose Maximum Integration Length:")
        self.groupBox_layout.addWidget(maxIntLen)
        self.max_len = Qt.QSpinBox()
         # set the initial values of some parameters
        self.max_len.setValue(40)
        self.max_len.setRange(0, 100)
        self.max_len.setSingleStep (5)
        self.groupBox_layout.addWidget(self.max_len)

        self.LIC_checkbox = Qt.QCheckBox("LIC On")
        self.LIC_checkbox.setChecked(False)
        self.LIC_checkbox.toggled.connect(self.on_LIC_checkbox)
        self.groupBox_layout.addWidget(self.LIC_checkbox)


        
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
            
        if hasattr(self, 'outline'):
            self.ren.RemoveActor(self.outline)
        
        # You need to modify the following actors' names based on how you define them!!!!!
        if hasattr(self, 'arrow_actor'):
            self.ren.RemoveActor(self.arrow_actor)
        
        if hasattr(self, 'streamline_actor'):
            self.ren.RemoveActor(self.streamline_actor)
            
        if hasattr(self, 'lic_actor'):
            self.ren.RemoveActor(self.lic_actor) 

        self.seeding_strategy = 0 # Uniform seeding is the default strategy

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
        
        

    
    ''' Use the vtkGlyph2D filter to show an arrow plot on a 2D surface'''
    def on_arrow_checkbox_change(self):
        if self.qt_arrow_checkbox.isChecked() == True:
            
            # Make sure we use the velocity field
            self.reader.GetOutput().GetPointData().SetActiveVectors("velocity")

            '''Complete the arrow plot visualization here '''

            glyphSource = vtk.vtkGlyphSource2D()
            glyphSource.SetGlyphTypeToArrow()
            glyphSource.FilledOff()

            densityFilter = vtk.vtkMaskPoints()
            densityFilter.SetInputData(self.reader.GetOutput())
            densityFilter.RandomModeOn() # enable the random sampling mechanism
            densityFilter.SetRandomModeType(3) #specify the sampling mode
            # densityFilter.SetMaximumNumberOfPoints(500)
            densityFilter.SetMaximumNumberOfPoints(int(self.max_points.value()))
            # print(int(self.max_points.value()))
            densityFilter.Update()

            glyph2D = vtk.vtkGlyph2D()
            glyph2D.SetSourceConnection(glyphSource.GetOutputPort())
            glyph2D.SetInputData(densityFilter.GetOutput())
            glyph2D.OrientOn()
            glyph2D.SetScaleModeToScaleByVector()
            # glyph2D.SetScaleFactor(0.03) # adjust the length of the arrows accordingly
            # print(self.arrow_scale.value())
            glyph2D.SetScaleFactor(self.arrow_scale.value()) # adjust the length of the arrows accordingly
            glyph2D.Update()

            arrows_mapper = vtk.vtkPolyDataMapper()
            arrows_mapper.SetInputConnection(glyph2D.GetOutputPort())
            arrows_mapper.Update()
            self.arrow_actor = vtk.vtkActor()
            self.arrow_actor.SetMapper(arrows_mapper)
            self.arrow_actor.GetProperty().SetColor(1,0,0) # set the color you want

            self.ren.AddActor(self.arrow_actor)
            
        # Turn on the following if you want to disable the arrow plots
        # But again you need to modify the "arrow_actor" name based on what you use!!!
        else:
            self.ren.RemoveActor(self.arrow_actor)
            
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()
        
    '''even handle for the radio buttons of seeding strategies
    '''
    def on_seeding_strategy(self):
        if self.uniform_seed_radio.isChecked() == True:
            self.random_seed_radio.setChecked(False)
            self.seeding_strategy = 0
        elif self.random_seed_radio.isChecked() ==  True:
            self.uniform_seed_radio.setChecked(False)
            self.seeding_strategy = 1

   
    '''         
        Complete the following function for genenerate uniform seeds 
        for streamline placement

    '''
    def uniform_generate_seeds(self):
        num_seeds = int (self.number_seeds.value())
        seedPoints = vtk.vtkPoints()

        # Generate the uniformly positioned seeds below!!

        bound = self.reader.GetPolyDataOutput().GetBounds()
        for i in range(num_seeds):
            for j in range(num_seeds):
                x_i = random.randint(0,32768) / 32768.0
                y_j = random.randint(0,32768) / 32768.0
                x = bound[0] + x_i * (bound[1] - bound[0])
                y = bound[2] + y_j * (bound[3] - bound[2])
                seedPoints.InsertNextPoint(x, y, 0)

        # Need to put the seed points in a vtkPolyData object
        seedPolyData  = vtk.vtkPolyData()
        seedPolyData.SetPoints(seedPoints)
        return seedPolyData

    '''  
        Complete the following function for genenerate random seeds 
        for streamline placement
    '''
    def random_generate_seeds(self):
        numb_seeds = int (self.number_seeds.value())
        seedPoints = vtk.vtkPoints()       

        # Generate the random seeds below!!

        bound = self.reader.GetPolyDataOutput().GetBounds()
        for i in range(numb_seeds):
            for j in range(numb_seeds):
                x_i = i * (1.0/(numb_seeds - 1))
                y_j = j * (1.0/(numb_seeds - 1))
                x = bound[0] + x_i * (bound[1] - bound[0])
                y = bound[2] + y_j * (bound[3] - bound[2])
                seedPoints.InsertNextPoint(x, y, 0)

        # Need to put the seed points in a vtkPolyData object
        seedPolyData  = vtk.vtkPolyData()
        seedPolyData.SetPoints(seedPoints)
        return seedPolyData

        
    ''' 
        Complete the following function to generate a set of streamlines
        from the above generated uniform or random seeds
    '''
    def on_streamline_checkbox_change(self):
        if self.qt_streamline_checkbox.isChecked() == True:
            # Step 1: Create seeding points 
            if self.seeding_strategy == 1: 
                seedPolyData = self.random_generate_seeds() # You also can try generate_seeding_line()
            elif self.seeding_strategy == 0:
                seedPolyData = self.uniform_generate_seeds()
            
            # Step 2: Create a vtkStreamTracer object, set input data and seeding points

            stream_tracer = vtk.vtkStreamTracer()
            stream_tracer.SetInputData(self.reader.GetPolyDataOutput()) # set vector field
            stream_tracer.SetSourceData(seedPolyData) # pass in the seeds

            # Step 3: Set the parameters. 
            # Check the reference https://vtk.org/doc/nightly/html/classvtkStreamTracer.html
            # to have the full list of parameters

            stream_tracer.SetIntegratorTypeToRungeKutta45()
            stream_tracer.SetIntegrationDirectionToBoth()
            stream_tracer.Update()


            # Step 4: Visualization

            stream_mapper = vtk.vtkPolyDataMapper()
            stream_mapper.SetInputConnection(stream_tracer.GetOutputPort())
            stream_mapper.ScalarVisibilityOff()
            stream_mapper.Update()

            self.streamline_actor = vtk.vtkActor()
            self.streamline_actor.GetProperty().SetColor(0,0,1)
            self.streamline_actor.SetMapper(stream_mapper)
            self.streamline_actor.GetProperty().SetOpacity(0.4)

            self.ren.AddActor(self.streamline_actor)
                    
        
        # Turn on the following if you want to disable the streamline visualization
        # But again you need to modify the "streamline_actor" name based on what you use!!!
        else:
            self.ren.RemoveActor(self.streamline_actor)
        
           
        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()       
    

    ''' Create a white noise texture for LIC computation '''
    def create_noise_texture(self):

        for i in range( 0, self.IMG_RES):
            for j in range( 0, self.IMG_RES):   
                noise_value = int(255*(random.randint(0,32768) / 32768.0))
                self.noise_tex[i][j] = [noise_value,noise_value,noise_value]
                
 
    ''' This function generates a uniform grid for the input data '''
    def generate_uniform_grid(self):
        self.vectorFieldPolyData = self.reader.GetPolyDataOutput()
        self.bounds = self.vectorFieldPolyData.GetBounds()
        
        #Create a uniform grid of points to interpolate over
        gridPoints = vtk.vtkPoints()
        
        self.space_x = (self.bounds[1]-self.bounds[0])/(self.IMG_RES-1)
        self.space_y = (self.bounds[3]-self.bounds[2])/(self.IMG_RES-1)
        self.space_z = 0
        for i in range( 0, self.IMG_RES):   
            for j in range( 0, self.IMG_RES):           
                x = self.bounds[0] + i * self.space_x
                y = self.bounds[2] + j * self.space_y
                gridPoints.InsertNextPoint ( x, y, 0)
        
        self.LICPolyData = vtk.vtkPolyData() # We will reuse this object for the final visualization of the LIC texture
        self.LICPolyData.SetPoints(gridPoints)
 
    

    ''' COMPLETE THE FOLLOWING LIC COMPUTATION    
        For each pixel:
            1. Compute a streamline from the center of this pixel using vtlStreamTracer. 
               Set the maximum length of the streamline and the step size properly
            2. From the above obtained streamline, get its integration points and find
               their corresponding pixel indices in the white noise texture
            3. Accumulate the color values from the pixels obtained in the previous step
        @return: the LIC texture in a vtkImageData object
    '''
   
    def Compute_LIC(self, integration_length):
        
        # Create the vtkImageData to store the lic texture for rendering
        licImage = vtk.vtkImageData()

        vectorFieldPolyData = self.reader.GetPolyDataOutput()
        self.bounds = vectorFieldPolyData.GetBounds()
        self.space_x = (self.bounds[1]-self.bounds[0])/(self.IMG_RES-1)
        self.space_y = (self.bounds[3]-self.bounds[2])/(self.IMG_RES-1)
        self.space_z = 0
       
        # Initialize the vtkImageData object
        licImage.SetDimensions([self.IMG_RES,self.IMG_RES,1])
        licImage.SetSpacing(self.space_x,self.space_y,self.space_z)
        licImage.SetOrigin(self.bounds[0], self.bounds[2], self.bounds[4])
        licImage.AllocateScalars(vtk.VTK_UNSIGNED_CHAR,3)
        
        integration_len = (self.bounds[1]-self.bounds[0])/self.max_len.value()

        # LIC calculation   (PLEAE COMPLETE)

        # seedPoints = vtk.vtkPoints() 
        bound = self.reader.GetPolyDataOutput().GetBounds()
        # print(bound)
        # return licImage
        for i in range(0, self.IMG_RES):
            for j in range(0, self.IMG_RES):
                x_j = (j + 0.5) / self.IMG_RES # remember j is the column index that corresponds to x direction!
                y_i = (i + 0.5) / self.IMG_RES # i is the row index corresponding to the y direction!
                x = bound[0] + x_j * (bound[1] - bound[0])
                y = bound[2] + y_i * (bound[3] - bound[2])
                # seedPoints.InsertNextPoint(x, y, bound[4])
                # print(self.IMG_RES)
                # print(self.space_x)

                # Need to put the seed points in a vtkPolyData object
                # seedPolyData  = vtk.vtkPolyData()
                # seedPolyData.SetPoints(seedPoints)

                stream_tracer = vtk.vtkStreamTracer()
                stream_tracer.SetInputData(self.reader.GetPolyDataOutput()) # set vector field
                # stream_tracer.SetSourceData(seedPolyData) # pass in the seeds
                stream_tracer.SetStartPosition(x, y, bound[4]) 
                stream_tracer.SetMaximumPropagation(integration_len)
                stream_tracer.SetInitialIntegrationStep(self.space_x )
                stream_tracer.SetIntegrationDirectionToBoth()

                stream_tracer.Update()

                streamline = stream_tracer.GetOutput()
                integrationPts = streamline.GetPoints()
                nPts = integrationPts.GetNumberOfPoints()
                # print(integrationPts.GetBounds())
                # return licImage
                curSum = 0
                for val in range (nPts):
                    fin_x = integrationPts.GetPoint(val)[0]
                    fin_y = integrationPts.GetPoint(val)[1]
                    # print(fin_x, fin_y)
                    fin_j = (self.IMG_RES * ( (fin_x - bound[0]) / (bound[1] - bound[0]) )) - 0.5
                    fin_i = (self.IMG_RES * ( (fin_y - bound[2]) / (bound[3] - bound[2]) )) - 0.5
                    # fin_j = (self.IMG_RES * fin_x) - 0.5
                    # fin_i = (self.IMG_RES * fin_y) - 0.5
                    # print(fin_i, fin_j)
                    curSum += self.noise_tex[int(fin_i)][int(fin_j)][0]

                # return licImage
                if nPts == 0:
                    self.LIC_tex[i][j][0] = self.LIC_tex[i][j][1] = self.LIC_tex[i][j][2] = 0
                else:
                    self.LIC_tex[i][j][0] = self.LIC_tex[i][j][1] = self.LIC_tex[i][j][2] = curSum/nPts
                # return licImage
 

       # Convert the LIC texture to a vtkImageData      
        k = 0
        for j in range( 0, self.IMG_RES):
            for i in range( 0, self.IMG_RES):        
            
                r = self.LIC_tex[i][j][0]
                g = self.LIC_tex[i][j][1]
                b = self.LIC_tex[i][j][2]
                                               
                # Update the color value for the licImage
                licImage.SetScalarComponentFromDouble(j,i,k,0, r) # Note: we need to flip j,i to get the correct result
                licImage.SetScalarComponentFromDouble(j,i,k,1, g)
                licImage.SetScalarComponentFromDouble(j,i,k,2, b)
        
        return licImage
    


    def generate_LIC(self):
        
        # Step 1: Set up three texture arrays
        self.IMG_RES = 256 #Specify the texture resolution
        
        # Initialize the arrays for LIC computation 
        self.noise_tex = [[ 0 for col in range(self.IMG_RES)] for row in range(self.IMG_RES)]
        self.vec_img = [[ [0,0,0] for col in range(self.IMG_RES)] for row in range(self.IMG_RES)] 
        self.LIC_tex = [[ [0,0,0] for col in range(self.IMG_RES)] for row in range(self.IMG_RES)] 

        # Initialize an attribute image for color blending with the LIC texture
        self.attribute_vals = [[ 0 for col in range(self.IMG_RES)] for row in range(self.IMG_RES)] 
        self.attribute_img = [[ [0,0,0] for col in range(self.IMG_RES)] for row in range(self.IMG_RES)] 

        # Step 2: Create a white noise texture
        self.create_noise_texture()

        # Step 3: Compute the LIC texture
        # self.bounds = vectorFieldPolyData.GetBounds()
        bound = self.reader.GetPolyDataOutput().GetBounds()  

        length = (bound[1]-bound[0])/self.max_len.value() # Make this a user-specified parameter on the interface
        licImage = self.Compute_LIC(length)


        # Step 4: Visualize
        
        img_mapper = vtk.vtkDataSetMapper()
        img_mapper.SetInputData(licImage)
        img_mapper.Update()
        
        lic_actor = vtk.vtkActor()
        lic_actor.SetMapper(img_mapper)
        
        return lic_actor
    
    def on_LIC_checkbox(self):
        if hasattr(self, 'lic_actor'):
            self.ren.RemoveActor(self.lic_actor)   
        
        if self.LIC_checkbox.isChecked() == True:
            self.lic_actor = self.generate_LIC()
            self.ren.AddActor(self.lic_actor)

        # Re-render the screen
        self.vtkWidget.GetRenderWindow().Render()
     

        
if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
