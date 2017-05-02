import sys
import numpy as np
import matplotlib as mpl
mpl.rcParams["svg.fonttype"] = "none"
mpl.rcParams["font.size"] = 12
mpl.rcParams["axes.unicode_minus"] = False
from matplotlib import pyplot as plt
from scipy import ndimage
import tkinter as tk
from skimage import measure as skmeasure
from mpl_toolkits.mplot3d import Axes3D
import h5py as h5

class Image3D:
    def __init__(self):
        self.pixels = None

        self.fig = plt.figure()
        self.axXY = self.fig.add_subplot(2,2,1)
        self.axXZ = self.fig.add_subplot(2,2,2)
        self.axYZ = self.fig.add_subplot(2,2,3)
        self.axXY.set_title( "XY-plane" )
        self.axXZ.set_title( "XZ-plane" )
        self.axYZ.set_title( "YZ-plane" )
        self.ax3D = self.fig.add_subplot(2,2,4, projection="3d")
        self.cmap = "bone"
        self.origColor = None
        self.render3D = True
        self.prefix = ""
        self.resolution = 0
        self.order = "C"

    def checkState( self ):
        if ( self.pixels is None ):
            raise( Exception("No pixels are given!") )
        elif ( len(self.pixels.shape) != 3 ):
            raise( Exception("Image is not 3D!") )

    def projectYZ( self ):
        self.checkState()
        return self.pixels.sum(axis=0)

    def projectXZ( self ):
        self.checkState()
        return self.pixels.sum(axis=1)

    def projectXY( self ):
        self.checkState()
        return self.pixels.sum(axis=2)

    def rotateX( self, angleDeg ):
        self.pixels = ndimage.rotate(self.pixels, angleDeg, axes=(1,2), reshape=False)

    def rotateY( self, angleDeg ):
        self.pixels = ndimage.rotate(self.pixels, angleDeg, axes=(0,2), reshape=False)

    def rotateZ( self, angleDeg ):
        self.pixels = ndimage.rotate(self.pixels, angleDeg, axes=(1,0), reshape=False)

    def center( self ):
        self.checkState()
        com = ndimage.measurements.center_of_mass( self.pixels )
        ndimage.shift( self.pixels, com )

    def showProjections( self ):
        self.axXY.imshow( self.projectXY(), cmap=self.cmap)#, aspect="auto" )
        self.axXZ.imshow( self.projectXZ(), cmap=self.cmap)#, aspect="auto" )
        self.axYZ.imshow( self.projectYZ(), cmap=self.cmap)#, aspect="auto" )

    def create3Dsurface( self ):
        self.ax3D.clear()
        verts, faces = skmeasure.marching_cubes( self.pixels, self.pixels.max()/1.1, spacing=(0.1,0.1,0.1) )
        self.ax3D.plot_trisurf( verts[:,0], verts[:,1], faces, verts[:,2], cmap="Spectral", lw=0,vmin=np.nanmin(verts[:,2]), vmax=np.nanmax(verts[:,2]))


    def updatePlots( self ):
        self.showProjections()
        if ( self.render3D ):
            self.create3Dsurface()
        plt.show( block=False )

    def save( self, hdf5=False ):
        outfname = self.prefix+"_%d_%d_%d_%d.raw"%(self.resolution, self.pixels.shape[0], self.pixels.shape[1], self.pixels.shape[2])
        self.pixels.ravel(order=self.order).tofile( outfname )
        print ("The new transformed array is written to %s"%(outfname))

        if ( hdf5 ):
            outfname = self.prefix+"_%d_%d_%d_%d.h5"%(self.resolution, self.pixels.shape[0], self.pixels.shape[1], self.pixels.shape[2])
            with h5.File( outfname, 'w' ) as hf:
                hf.create_dataset( "voxels", data=self.pixels )


class ControlInterface:
    def __init__( self, master ):
        self.root = master
        self.img = Image3D()

        self.rotXLab = tk.Label( self.root, text="RotX")
        self.rotX = tk.Entry( self.root, width=20 )
        self.rotX.insert(0, 0.0)
        self.rotYLab = tk.Label( self.root, text="RotY")
        self.rotY = tk.Entry( self.root, width=20)
        self.rotY.insert(0, 0.0)
        self.rotZLab = tk.Label( self.root, text="RotZ")
        self.rotZ = tk.Entry( self.root, width=20)
        self.rotZ.insert(0,0.0)
        self.rotP90XB = tk.Button( self.root, text="+90", command=self.rotP90X )
        self.rotM90XB = tk.Button( self.root, text="FlipX", command=self.flipX )
        self.rotP90YB = tk.Button( self.root, text="+90", command=self.rotP90Y )
        self.rotM90YB = tk.Button( self.root, text="FlipY", command=self.flipY )
        self.rotP90ZB = tk.Button( self.root, text="+90", command=self.rotP90Z )

        self.updateButton = tk.Button( self.root, text="Update", command=self.update )
        self.renderButtonValue = tk.IntVar()
        self.render3Dbutton = tk.Checkbutton( self.root, text="Render 3D", variable=self.renderButtonValue )
        self.render3Dbutton.select()

        self.saveButton = tk.Button( self.root, text="Save", command=self.save)

        self.grid()

        self.imgIsCentered = False

    def grid( self ):
        self.rotXLab.grid(row=0,column=0)
        self.rotX.grid(row=0, column=1)
        self.rotYLab.grid(row=1,column=0)
        self.rotY.grid(row=1,column=1)
        self.rotZLab.grid(row=2,column=0)
        self.rotZ.grid(row=2,column=1)
        self.rotP90XB.grid(row=0,column=2)
        self.rotM90XB.grid(row=0,column=3)
        self.rotP90YB.grid(row=1,column=2)
        self.rotM90YB.grid(row=1,column=3)
        self.rotP90ZB.grid(row=2,column=2)
        self.render3Dbutton.grid(row=3,column=0)
        self.updateButton.grid(row=3,column=1)
        self.saveButton.grid(row=3,column=2)

    def update( self ):
        if ( not self.imgIsCentered ):
            self.img.center()
            self.imgIsCentered = True
        rotX = float( self.rotX.get() )
        rotY = float( self.rotY.get() )
        rotZ = float( self.rotZ.get() )

        if ( int(self.renderButtonValue.get()) == 1 ):
            self.img.render3D = True
        else:
            self.img.render3D = False

        ZERO_ANGLE = 0.0001
        if ( np.abs(rotX) > ZERO_ANGLE ):
            self.img.rotateX( rotX )
        if ( np.abs(rotY) > ZERO_ANGLE ):
            self.img.rotateY( rotY )
        if ( np.abs(rotZ) > ZERO_ANGLE ):
            self.img.rotateZ( rotZ )

        self.img.updatePlots()

    def rotP90X( self ):
        #self.img.pixels = np.rot90( self.img.pixels, axes=(0,1) )
        self.img.pixels = self.img.pixels.transpose((0,2,1))
    def flipX( self ):
        #self.img.pixels = np.rot90( self.img.pixels, k=3, axes=(0,1) )
        self.img.pixels = np.flipud( self.img.pixels )
        #self.img.pixels = self.img.pixels.transpose((0,2,1))
    def rotP90Y( self ):
        #self.img.pixels = np.rot90( self.img.pixels, axes=(0,2) )
        self.img.pixels = self.img.pixels.transpose((2,1,0))

    def rotP90Z( self ):
        #self.img.pixels = np.rot90( self.img.pixels, axes=(0,2) )
        self.img.pixels = self.img.pixels.transpose((1,0,2))
    def flipY( self ):
        #self.img.pixels = np.rot90( self.img.pixels, k=3, axes=(0,2) )
        self.img.pixels = self.img.pixels.transpose((2,1,0))
    def save( self ):
        self.img.save( hdf5=True )
