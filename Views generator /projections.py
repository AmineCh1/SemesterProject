
import numpy as np
import sys 
import math as math
import argparse
import vtk
import os
import ico 


#We use this function to parse the user's input.
def get_parameters():
    description="Generates PNG snapshots of chosen file wrt to capture mode/ nb of snapshots."
    parser=argparse.ArgumentParser(description=description,formatter_class =argparse.RawDescriptionHelpFormatter)
    parser.add_argument('reference',help='.ply file.')
    parser.add_argument('encoded',help='.ply file.')
    parser.add_argument('mode',help='Mode of PNG capture.')
    parser.add_argument('K',help='Subdivision level k in case icoK was chosen. If icoK was not chosen, specify 0, i.e cube 0 or frontal 0.')
    parser.add_argument('lighting',help='Lighting (on/off).',default='off')
    args = parser.parse_args()
    if(args.mode=='icoK' and 'K' not in vars(args)):
        parser.error("If icoK chosen, K must be specified !")
    
    return args
    
  

# This function, given a ply file, will computes the  bounding box of the ply object, and ->
# subsequently generate the coordinates of the chosen mode, and capture the projections at the generated  ->
# coordinates.
def generateSnapshots(fname):
   
    DISTANCE_FACTOR = 1.3
    PARAMS =get_parameters()

    print(PARAMS.K)
    ## VTK pipeline ...

    colors =vtk.vtkNamedColors()
    reader = vtk.vtkPLYReader()
    
    reader.SetFileName(fname)
    reader.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())


    #We compute the bounding box of the model.
    diff=[]
    #GetBounds essentially returns (xmin,xmax,ymin,ymax,zmin,zmax)
    limits = list(mapper.GetBounds())
    diff.append(limits[1]-limits[0])
    diff.append(limits[3]-limits[2])
    diff.append(limits[5]-limits[4])


    #We define the radius with respect to the bounding box.
    radius=DISTANCE_FACTOR*np.max(diff)

    #Single, frontal projection.
    if PARAMS.mode=='frontal':
        coordinates=((radius,0,0),) 

    #6-vertex projection.
    elif PARAMS.mode=='cube':
         coordinates=[
            (radius,0,0)
            ,(-radius,0,0)
            ,(0,radius,0)
            ,(0,-radius,0)
            ,(0,0,radius)
            ,(0,0,-radius)]
    #K-level icosahedron projections.
    elif PARAMS.mode=='icoK':
        generatePoints = ico.Icosahedron(radius)
        coordinates = generatePoints.subdivide(int(PARAMS.K))
    else: 
        exit()
    
    coordinates=list(coordinates)
    actor=vtk.vtkActor()

    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Tan'))
    if(PARAMS.lighting == 'off'):
        actor.GetProperty().LightingOff()
    
    renderer =vtk.vtkRenderer()
    renderer.AddActor(actor)

    cameras= [vtk.vtkCamera() for elem in coordinates]
    f=open('coordinates.txt','w')
    f.write('\n'.join(map((lambda x : str(x)),coordinates)))
    f.close()
    print(len(coordinates))
    print(cameras)

    renWin = vtk.vtkRenderWindow()
    #Generate captures.
    
    for i in range(len(coordinates)):
        cameras[i].ParallelProjectionOn()
        cameras[i].SetParallelScale(radius/2)    
        
        #Set the focal point to the center of the bounding box 
        cameras[i].SetFocalPoint(limits[0]+(diff[0])/2,limits[2]+(diff[1])/2,limits[4]+(diff[2])/2)
        cameras[i].SetClippingRange((0.001,5000))
        #Certain coordinates required a specific View-Up vector.
        if (coordinates[i][0]== 0 and coordinates[i][2]==0):
            cameras[i].SetViewUp(0.0,0.0,1.0)
        else :
            cameras[i].SetViewUp(0.0,1.0,0.0)

        cameras[i].SetPosition((coordinates[i]))
        renderer.SetActiveCamera(cameras[i])

    
        
        renWin.OffScreenRenderingOn()

        renWin.AddRenderer(renderer)
        renWin.SetSize(1920,1080)
        renWin.Render()
        
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(renWin)
        w2if.SetInputBufferTypeToRGBA()
        w2if.ReadFrontBufferOff()
        w2if.Update()
        
        writer = vtk.vtkPNGWriter()
        
        writer.SetInputConnection(w2if.GetOutputPort())
        writer.SetFileName('img'+fname[:-4]+' %d.png' %i)
        writer.Write()

    os.system("ffmpeg -f image2 -pattern_type glob -framerate 1  -i 'img"+fname[:-4]+"*.png' -s 1920x1080 "+fname[:-4]+".avi") #psnr / [:-4] removes the extension
       
def main():
    PARAMS = get_parameters()
    generateSnapshots(PARAMS.reference)
    generateSnapshots(PARAMS.encoded)

    
    os.system("ffmpeg -i "+PARAMS.encoded[:-4]+".avi -i "+PARAMS.reference[:-4]+".avi -lavfi  ssim=\"stats_file=stats_ssim.log\" -f null -")
    os.system("ffmpeg -i "+PARAMS.encoded[:-4]+".avi -i "+PARAMS.reference[:-4]+".avi -lavfi  psnr=\"stats_file=stats_psnr.log\" -f null -")


if __name__ == "__main__":

    main()

    


        




    





