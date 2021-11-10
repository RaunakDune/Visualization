import vtk
import numpy as np


def createData():
    source = vtk.vtkSphereSource()
    source.SetPhiResolution(30)
    source.SetThetaResolution(30)
    source.Update()
    poly = source.GetOutput()

    # Compute some velocity field. This data you already got.
    # I'm creating here some data myself.
    nPoints = poly.GetNumberOfPoints()
    points = [poly.GetPoint(i) for i in range(nPoints)]
    points = np.asarray(points)
    x,y,z = points.T
    vel = np.c_[x*np.cos(y*np.pi), y*np.sin(2*x*np.pi), np.cos(2*z*np.pi)]
    mag = np.linalg.norm(vel, axis=1)
    return poly, vel, mag

'''
    The main function.
'''

def main():
    # Create input.
    #    poly: vtk.vtkPolyData()
    #    vel:  np.ndarray with shape (nPoints, 3)
    #    mag:  np.ndarray with shape (nPoints,)
    poly, vel, mag = createData()

    # Create data arrays.
    velocity = vtk.vtkDoubleArray()
    velocity.SetName("velocity")
    velocity.SetNumberOfComponents(3)
    nPoints = poly.GetNumberOfPoints()
    velocity.SetNumberOfTuples(nPoints)
    for i in range(nPoints):
        velocity.SetTuple(i, list(vel[i]))
    magnitude = vtk.vtkDoubleArray()
    # Similar as SetNumberOfValues(1) + SetNumberOfTuples(nPoints):
    magnitude.SetNumberOfValues(nPoints)
    magnitude.SetName("magnitude")
    for i in range(nPoints):
        magnitude.SetValue(i, mag[i])

    # Add to point data array.
    poly.GetPointData().AddArray(velocity)
    poly.GetPointData().AddArray(magnitude)
    poly.GetPointData().SetActiveScalars("magnitude")
    poly.GetPointData().SetActiveVectors("velocity")

    arrow = vtk.vtkArrowSource()
    arrow.Update()

    # Create glyph.
    glyph = vtk.vtkGlyph3D()
    glyph.SetInputData(poly)
    glyph.SetSourceConnection(arrow.GetOutputPort())
    glyph.SetScaleFactor(0.1)
    # glyph.OrientOn()
    glyph.SetVectorModeToUseVector()
    glyph.SetColorModeToColorByScalar()
    glyph.Update()


    arrows_mapper = vtk.vtkPolyDataMapper()
    arrows_mapper.SetInputConnection(glyph.GetOutputPort())
    arrows_mapper.Update()

    arrow_actor = vtk.vtkActor()
    arrow_actor.SetMapper(arrows_mapper)
    #arrow_actor.GetProperty().SetColor(0,0,1) # set the color you want but you need to 
                                               # call ScalarVisibilityOff() in your mapper


    render = vtk.vtkRenderer()
    render.AddActor(arrow_actor)

    window = vtk.vtkRenderWindow()
    window.AddRenderer(render)
    window.SetSize(600, 600)

    window_interactor = vtk.vtkRenderWindowInteractor()
    window_interactor.SetRenderWindow(window)   
    window_interactor.Initialize()

    window.Render()
    window.SetWindowName('3D Arrow Plot')
    window_interactor.Start()        

if __name__ == '__main__':
    main()