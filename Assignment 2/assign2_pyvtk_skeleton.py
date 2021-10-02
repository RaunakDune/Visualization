# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 10:46:25 2020

@author: created by Duong B Nguyen, modified by Guoning Chen
"""

'''
    Load vtk structured/unstructured grid or polydata data with a given file name (and directory) 
    and compute and visualize the iso-contours with an input iso-value.
    
'''
import vtk
import math

vtk.vtkObject.GlobalWarningDisplayOff() #Disable vtkOutputWindow

'''
    Global variables for vtk to re-render the screen when the user presses a keyboard
'''
vtk_poly_mapper = vtk.vtkPolyDataMapper()
lut = vtk.vtkLookupTable()
vtk_render_window = vtk.vtkRenderWindow()


'''
    Handle the keyboard press events
    When the user press 0, 1 or 2, the new corresponding color map will be applied
'''
def keypress_callback(obj, ev):
    key = obj.GetKeySym()
    #print(key, 'was pressed')
    
    if key == '0' or key == '1' or key == '2' or key == '3':
        color_scheme = int(key)
        MakeLUT(color_scheme, lut)
        vtk_poly_mapper.SetLookupTable(lut)
        vtk_render_window.Render()

'''
    The main function.
'''
def main():
    
    #Provide the introduction about the program
    print("Introduction: This program loads a vtk structured/unstructured grid or polydata data file given the file name (and directory) and show the color plot of its scalar field\n")
    
    ''' Step 1: Ask users to input the vtk file name '''
    print("Please input the full file name: ")
    input_file_name = input()
    
    ''' Step 2: Read and verify the vtk input file '''
    vtk_reader = vtk.vtkDataSetReader()
    vtk_reader.SetFileName(input_file_name)
    vtk_reader.Update()
    
    # Verify
    if vtk_reader.IsFileStructuredGrid() \
       or vtk_reader.IsFileUnstructuredGrid() \
       or vtk_reader.IsFilePolyData():
        print('Data file loaded successfully!')
    else:
        print('Cannot read the input file!')
        print('Exiting the program...')
        return 0
        
    ''' Step 3 Use geometry filter to get the geometry representation  '''
    vtk_geometry = vtk.vtkGeometryFilter()
    if vtk_reader.IsFileStructuredGrid():
        vtk_geometry.SetInputData(vtk_reader.GetStructuredGridOutput())
        vtk_geometry.Update()
    elif vtk_reader.IsFileUnstructuredGrid():
        vtk_geometry.SetInputData(vtk_reader.GetUnstructuredGridOutput())
        vtk_geometry.Update()
    
    
    ''' Step 4: Get the scalar field '''
    
    # For all data of assignment 2, the scalar field has a name "s"
    scalar_field = "s"
    
    # Verify the name of the scalar field, and then get the min, max scalar values
    try:
        if not vtk_reader.IsFilePolyData():
            min_scalar,max_scalar = vtk_geometry.GetOutput().GetPointData().GetArray(scalar_field).GetRange()
        else:
            min_scalar,max_scalar = vtk_reader.GetPolyDataOutput().GetPointData().GetArray(scalar_field).GetRange()

        print("The min and max scalar values: ", min_scalar, max_scalar)
    except :
        print('Cannot find the inputed scalar field!')
        print('Exiting the program...')
        return 0
    

    
    ''' Step 5: Use vtkPolyDataMapper (or vtkDataSetMapper) to visualize the scalar data '''
    
    # The mapper is responsible for pushing the geometry into the graphics
    # library. It may also do color mapping, if scalars or other
    # attributes are defined.
    if not vtk_reader.IsFilePolyData():
        vtk_poly_mapper.SetInputData(vtk_geometry.GetOutput()) 
        # You can also use .SetInputConnection and .GetOutputPort() here
    else:
        vtk_poly_mapper.SetInputData(vtk_reader.GetPolyDataOutput())
        
    #Create vtk color lookup table and use it for the color mapping
    
    color_scheme = 0
    MakeLUT(color_scheme, lut)
    vtk_poly_mapper.SetScalarModeToUsePointData()
    vtk_poly_mapper.SetLookupTable(lut)
    vtk_poly_mapper.SetScalarRange(min_scalar, max_scalar) #Specify range in terms of scalar minimum and maximum (smin,smax). These values are used to map scalars into lookup table
    vtk_poly_mapper.SelectColorArray(scalar_field)
   
    '''
    Note: Instead of using vtkPolyDataMapper representation, you can use vtkDataSetMapper for this task
    Here is the sample code for vtkDataSetMapper:
        
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(vtk_geometry.GetOutput())
        mapper.SetScalarModeToUsePointData()
        mapper.SetLookupTable(lut)
        mapper.SetScalarRange(min_scalar,max_scalar)
        mapper.SelectColorArray(scalar_field)
    '''
    
    ''' Step 6: Create an actor to the above mapper '''
    
    # The actor is a grouping mechanism: besides the geometry (mapper), it
    # also has a property, transformation matrix, and/or texture map.
    vtk_actor = vtk.vtkActor()
    vtk_actor.SetMapper(vtk_poly_mapper)
    
    
    ''' 
        Assignment 2 Task 2.3 and 2.4 
        Extract the iso-contours by using vtkContourFilter
        Compute the following code!!!
    '''
    
    # Ask the user to input the threshold value for iso-contour extraction
    # Uncomment the following two lines for Assignment 2
    # print("Please input the threshold value for iso-contour extraction: ")
    # scalar_threshold = input()
    
    ''' TODO: Create iso-contour based on the user input scalar_threshold here '''




    ''' TODO: Create a mapper for the extract contour geometry here '''





    # Create an actor for the contour mapper.
    vtk_contour_actor = vtk.vtkActor() 
    
    ''' TODO: set the mapper for this actor using the above contour mapper here '''
    
    # The following set the color and thickness of the contours
    colors = vtk.vtkNamedColors()
    vtk_contour_actor.GetProperty().SetColor(colors.GetColor3d("Black"))
    vtk_contour_actor.GetProperty().SetLineWidth(2)
    
    ''' Step 7: Create vtk renderer, window and show the visualization result'''
    
    # Create the graphics structure. The renderer renders into the render
    # window. The render window interactor captures mouse events and will
    # perform appropriate camera or actor manipulation depending on the
    # nature of the events.
    vtk_renderer = vtk.vtkRenderer()
    vtk_render_window.AddRenderer(vtk_renderer)
    vtk_ren_win_iterator = vtk.vtkRenderWindowInteractor()
    vtk_ren_win_iterator.AddObserver('KeyPressEvent', keypress_callback, 1.0)
    vtk_ren_win_iterator.SetRenderWindow(vtk_render_window)

    # Add the actors to the renderer, set the background and size
    vtk_renderer.AddActor(vtk_actor) #Add the actor for the color plot
    
    ''' TODO: add the actor for the contours here '''
    
    
     
    # Set the background color and initialize the vtk window
    colors = vtk.vtkNamedColors() #initialize the color variable
    vtk_renderer.SetBackground(colors.GetColor3d("White")) # you can change the background color here
    vtk_render_window.SetSize(500, 500)
    

    # This allows the interactor to initalize itself. It has to be
    # called before an event loop.
    vtk_ren_win_iterator.Initialize()

    # Start rendering   
    vtk_render_window.Render()
    vtk_render_window.SetWindowName('COSC 6344 Visualization - YOUR NAME')

    # Start the event loop so that the vtk window keeps openning
    vtk_ren_win_iterator.Start()


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
    
    nc = 256 #interpolate 256 values, increase this to get more colors

    if colorScheme == 0: # rainbow
        
        lut.SetNumberOfTableValues(nc)
        lut.Build()
        
        # The min scalar value is mapped to 0, and the max value is mapped to 1
        sMin = 0.
        sMax = 1.
        
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
        
    elif colorScheme == 2: #Heat-map
        lut.SetNumberOfTableValues(nc)
        lut.Build()
        
        ''' TODO: complete the heat-map color mapping here '''
        
        
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


if __name__ == '__main__':
    main()
