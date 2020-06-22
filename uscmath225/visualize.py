import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np

from jupyterthemes import jtplot
jtplot.style(ticks=True, grid=True)


class MatrixClassifier:
    
    def __init__(self):
        0==0

    def analyze(self,M):
        
        self.isSquare = M.shape[0]==M.shape[1]

        if self.isSquare:
            self.det = np.linalg.det(M)
        
        self.columnLengths = np.diag(M.T @ M)
        self.areAxesOrderPreserved = True if self.det > 0 else False
        self.stretch = np.abs(self.det)


        self.isStretchOne = np.abs(self.stretch-1) < 0.00001
        self.areAllColumnsUnitLength = np.all(np.abs(self.columnLengths-1) < 0.00001)

        return { "isSquare":self.isSquare, \
                 "isStretchOne":self.isStretchOne, \
                 "areAxesOrderPreserved": self.areAxesOrderPreserved,
                 "areAllColumnsUnitLength": self.areAllColumnsUnitLength
        }



        
    def isRotation(self,M):
        # M.T M must equal identity, think why

        self.analyze(M)
        
        test = [self.isSquare , self.isStretchOne ,  self.areAllColumnsUnitLength , self.areAxesOrderPreserved]
        if np.all(test):
            #return angle of rotation
            angle = np.degrees( np.arctan2   (    M[1,0]  ,  M[0,0]   )    ) 
            return {"angle":angle}
        else:
            return False


    def isReflection(self,M):
        self.analyze(M)

        test = [self.isSquare, self.isStretchOne, self.areAxesOrderPreserved==False , self.areAllColumnsUnitLength ]
        if np.all(test):
            angle = np.degrees( np.arctan2   (    M[1,0]  ,  M[0,0]   )    )  / 2
            return {"angle":angle}
        else:
            return False


    def isProjection(self,M):
        self.analyze(M)
        if self.stretch < 0.00001:
            angle = np.degrees(np.arctan2(M[1,0],M[0,0]))
            return {"angle":angle}
        else:
            return False

        

class Visualizer:

    def __init__(self,dim=2,figsize=(5,5)):
        self.dim = dim
        self.figsize = figsize
        self.plt = plt
        plt.ion()


        self.MCS = MatrixClassifier()

        #https://www.interviewqs.com/ddi_code_snippets/dynamic_update_plot_loop_ipython

    def vector(self,v,alt=False,axes_range=None,**kwargs):
        '''
        v -> vector
        alt -> Alternate plot (contrasted to primary plot) -> doubles hatch when hatch given, else uses hatch->xxx (useful when plotting one vector as transform of another vector of same color)
        axes_range -> [xmin,xmax,ymin,ymax(,zmax,zmin)]
        rest parameters same as that of pyplot.quiver - 
            color -> red,green,blue,etc.
            linestyle -> {'dashed',''-', '--', '-.', ':', '', (offset, on-off-seq), ...}
            hatch 	{'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}
        '''
        if type(axes_range) == type(None):
            axes_range = np.array([-1,1,-1,1])*np.linalg.norm(v)*2

        if not ("hatch" in kwargs):
            if alt:
                hatch="xxx"
            else:
                hatch=""


        if "hatch" in kwargs:
            #print('---------'*10)
            # if both hatch and alt are True
            if alt:
                # double the effect
                if not kwargs['hatch']==None:
                    hatch = kwargs["hatch"]*2
                else:
                    hatch = kwargs["hatch"]
            else:
                hatch = kwargs['hatch']

        kwargs["hatch"] = hatch

        #set axes range
        plt.axis(axes_range)

        if self.dim==2:
            plt.rcParams['figure.figsize'] = self.figsize
            plt.quiver(*v,scale=1,units='xy',**kwargs)
            



    def matrix(self,m,plot_std_bases=True,axes_range=None,colors=["red","green","blue"],**kwargs):
        '''
        m -> matrix
        plot_std_bases -> show standard bases as well
        axes_range -> [xmin,xmax,ymin,ymax(,zmax,zmin)]
        colors -> colors for axes
                  eg:  [red,green(,blue)]
        rest parameters same as that of pyplot.quiver - 
            linestyle -> {'dashed',''-', '--', '-.', ':', '', (offset, on-off-seq), ...}
            hatch 	{'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}
        '''

        if type(axes_range) == type(None):
            axes_range = np.array([-1,1,-1,1])*max(list(map(np.linalg.norm,m.T)))*2

        if self.dim ==2:

            
            if plot_std_bases:
                #plot xcap and ycap
                std_bases=np.array([[1,0],[0,1]])
                self.matrix(std_bases,plot_std_bases=False,axes_range=axes_range,colors=colors,**kwargs)
               


            #plot columns of the matrix 
            xcap_goes_to = m[:,0]
            ycap_goes_to = m[:,1]
            
            # use alt plot only when plotting std_bases as well, otherwise do not use alt and plot primary
            # if plot_std_bases=True -> the columns of matrix need to be hatched -> alt=True
            self.vector(xcap_goes_to,alt= plot_std_bases , axes_range=axes_range, color=colors[0],**kwargs)
            self.vector(ycap_goes_to,alt= plot_std_bases ,axes_range=axes_range,color=colors[1],**kwargs)

            # Classify matrices and plot appropriate visualization helper diagrams/figures
            rot,ref,proj = self.MCS.isRotation(m), self.MCS.isReflection(m), self.MCS.isProjection(m)
            # #if one of rot or ref, then draw the angle as a line and also draw a unit circle
            if plot_std_bases and (rot or ref or proj):
                if rot:
                    angle = rot["angle"]
                    title = f"Rotation @ {angle:.2f} \N{DEGREE SIGN}"
                elif ref:
                    angle = ref["angle"]
                    title = f"Reflection @ {angle:.2f} \N{DEGREE SIGN}"
                elif proj:
                    angle = proj["angle"]
                    title = f"Projection @ {angle:.2f} \N{DEGREE SIGN}"

                self.line(angle)
                self.circle((0,0),1)
                
                plt.title(title)



    def circle(self,center,radius,color="black"):
        c=plt.Circle((0,0),1,color='black',fill=False)
        plt.gcf().gca().add_artist(c)

    def line(self,slope_angle,fmt="b--"):
        x=np.arange(-10,10)
        rad = np.radians(slope_angle)
        y=np.tan(rad)*x
        plt.plot(x,y,fmt)


    def show(self):
        plt.pause(0.01)
        plt.show()
