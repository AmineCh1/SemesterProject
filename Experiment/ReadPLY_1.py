import vtk

    
import sys      

  

     
   

def get_parameters():
  import argparse
  description='Read a PLY file'
  epilogue= ''''''
  parser=argparse.ArgumentParser(description=description, epilog=epilogue,
  formatter_class =argparse.RawDescriptionHelpFormatter)
  parser.add_argument('filename',help='Please include a .ply file')
  args = parser.parse_args()
  return args.filename


def main():
  colors = vtk.vtkNamedColors()

  fname= get_parameters()
  reader = vtk.vtkPLYReader()
  reader.SetFileName(fname)
  reader.Update()

  mapper=vtk.vtkPolyDataMapper()
  mapper.SetInputConnection(reader.GetOutputPort())
  
  
  actor=vtk.vtkActor()
  actor.SetMapper(mapper)
  actor.GetProperty().LightingOff()

  renderer =vtk.vtkRenderer()
  renderer.AddActor(actor)

  
  
  
  render_window=vtk.vtkRenderWindow()
  render_window.SetWindowName("Simple VTK scene")
  render_window.AddRenderer(renderer)
  render_window.SetSize(600,600)
  render_window.Render()




  
  
  renderer.SetBackground(colors.GetColor3d('White'))
  render_window.OffScreenRenderingOn()
  interactor=vtk.vtkRenderWindowInteractor()
  interactor.SetRenderWindow(render_window)

  w2if = vtk.vtkWindowToImageFilter()
  w2if.SetInput(render_window)
  w2if.SetInputBufferTypeToRGBA()
  
  w2if.Update()


  writer = vtk.vtkPNGWriter()
  writer.SetInputConnection(w2if.GetOutputPort())
  writer.SetFileName("../"+fname[:-3] + "png")
  writer.Write()

  


if __name__ == "__main__":
    main()
