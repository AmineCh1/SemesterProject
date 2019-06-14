#We define two structures that make the program overall a bit more readable : Points and faces 
class Point: 
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z 
    def toTup(self):
        return (self.x,self.y,self.z)
    # Since the faces of an icosahedron are triangular, each face consists of 3 points.
class Face:
    def __init__(self,p_1,p_2,p_3):
        self.p_1=p_1
        self.p_2=p_2
        self.p_3=p_3

class Icosahedron:
    phi=0.5*(1+5**0.5)
    # We essentially want to build a set of coordinates.
    #We first initialize the faces and points of a standard 12-vertex icosahedron.
    def __init__(self,radius):
        self.points=[Point(-radius,  self.phi*radius,  0),
        Point( radius,  self.phi*radius,  0),
        Point(-radius, -self.phi*radius,  0),
        Point( radius, -self.phi*radius,  0),

        Point( 0, -radius,  self.phi*radius),
        Point( 0,  radius,  self.phi*radius),
        Point( 0, -radius, -self.phi*radius),
        Point( 0,  radius, -self.phi*radius),

        Point( self.phi*radius,  0, -radius),
        Point( self.phi*radius,  0,  radius),
        Point(-self.phi*radius,  0, -radius),
        Point(-self.phi*radius,  0,  radius)]
    
        self.faces = [Face(self.points[0], self.points[11], self.points[5]),
        Face(self.points[0], self.points[5], self.points[1]),
        Face(self.points[0], self.points[1], self.points[7]),
        Face(self.points[0], self.points[7], self.points[10]),
        Face(self.points[0], self.points[10], self.points[11]),

        
        Face(self.points[1], self.points[5], self.points[9]),
        Face(self.points[5], self.points[11], self.points[4]),
        Face(self.points[11], self.points[10], self.points[2]),
        Face(self.points[10], self.points[7], self.points[6]),
        Face(self.points[7], self.points[1], self.points[8]),

        
        Face(self.points[3], self.points[9], self.points[4]),
        Face(self.points[3], self.points[4], self.points[2]),
        Face(self.points[3], self.points[2], self.points[6]),
        Face(self.points[3], self.points[6], self.points[8]),
        Face(self.points[3], self.points[8], self.points[9]),

        
        Face(self.points[4], self.points[9], self.points[5]),
        Face(self.points[2], self.points[4], self.points[11]),
        Face(self.points[6], self.points[2], self.points[10]),
        Face(self.points[8], self.points[6], self.points[7]),
        Face(self.points[9], self.points[8], self.points[1])]

        #This function returns the middle point of a segment.
    def middlePoint(self,p_1, p_2):
        tempPoint = Point(0,0,0)
        tempPoint.x = 0.5*(p_2.x+p_1.x) 
        tempPoint.y = 0.5*(p_2.y+p_1.y) 
        tempPoint.z = 0.5*(p_2.z+p_1.z) 
        return tempPoint
        
    def subdivide(self,level):
       #Recursion defined by level of subdivision.
        for i in range(level):
            newFaces=set([])
            #We compute the middle point of each segment of a face
            for elem in self.faces:
                mid_1 = self.middlePoint(elem.p_1,elem.p_2)
                mid_2 = self.middlePoint(elem.p_2,elem.p_3)
                mid_3 = self.middlePoint(elem.p_3,elem.p_1)
             #and then create new faces with respect to those points.
                newFaces.add(Face(elem.p_1,mid_1,mid_3))
                newFaces.add(Face(elem.p_2,mid_2,mid_1))
                newFaces.add(Face(elem.p_3,mid_3,mid_2))
                newFaces.add(Face(mid_1,mid_2,mid_3))
            self.faces=newFaces
        self.pointsToReturn=set([])
        #Once we have reached the desired level of subdivision, we extract all the points from the resulting faces.
        for elem in self.faces:
            self.pointsToReturn.add(elem.p_1.toTup())
            self.pointsToReturn.add(elem.p_2.toTup())
            self.pointsToReturn.add(elem.p_3.toTup())
        
        return self.pointsToReturn

        

            
            






