import numpy as np 



class Transformer:
    '''
    Axis=-1 for 2D
    Axis = 0,1,2 for 3D
    '''
    def __init__(self,dim=2):
        self.dim = dim

    def rotation(self,deg,axis=0):
        '''
        deg -> rotation angle from x-axis if dimension 2D
        axis -> rotation about axis 0,1,2 (x,y,z-axis) for 3D
        '''
        rad = np.radians(deg)
        if self.dim==2:
            c,s = np.cos(rad),np.sin(rad)
            xcap_goes_to = [c,s]
            ycap_goes_to = [-s,c]
            return np.column_stack((xcap_goes_to,ycap_goes_to))


    def reflection(self,deg):
        '''
        deg -> slope angle of line of reflection for 2D
        '''
        rad = np.radians(deg)
        if self.dim==2:
            c,s = np.cos(2*rad),np.sin(2*rad)
            xcap_goes_to = [c,s]
            ycap_goes_to = [s,-c]
            return np.column_stack((xcap_goes_to,ycap_goes_to))

    
    def projection(self,deg):
        '''
        deg -> slope angle of line onto which we want to project
        '''

        rad = np.radians(deg)
        if self.dim==2:
            cc,cs,ss = np.cos(rad)**2,np.cos(rad)*np.sin(rad),np.sin(rad)**2
            xcap_goes_to = [cc,cs]
            ycap_goes_to = [cs,ss]
            return np.column_stack((xcap_goes_to,ycap_goes_to))


