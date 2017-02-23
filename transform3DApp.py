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
        self.create3Dsurface()
        plt.show( block=False )

class ControlInterface:
    def __init__( self, master ):
        self.root = master
        self.img = Image3D()

        self.rotXLab = tk.Label( self.root, text="RotX")
        self.rotX = tk.Entry( self.root, width=60 )
        self.rotYLab = tk.Label( self.root, text="RotY")
        self.rotY = tk.Entry( self.root, width=60)
        self.rotZLab = tk.Label( self.root, text="RotZ")
        self.rotZ = tk.Entry( self.root, width=60)

        self.updateButton = tk.Button( self.root, text="Update", command=self.update )

        self.grid()

        self.imgIsCentered = False

    def grid( self ):
        self.rotXLab.grid(row=0,column=0)
        self.rotX.grid(row=0, column=1)
        self.rotYLab.grid(row=1,column=0)
        self.rotY.grid(row=1,column=1)
        self.rotZLab.grid(row=2,column=0)
        self.rotZ.grid(row=2,column=1)
        self.updateButton.grid(row=3,column=1)

    def update( self ):
        if ( not self.imgIsCentered ):
            self.img.center()
            self.imgIsCentered = True
        rotX = float( self.rotX.get() )
        rotY = float( self.rotY.get() )
        rotZ = float( self.rotZ.get() )

        ZERO_ANGLE = 0.0001
        if ( np.abs(rotX) > ZERO_ANGLE ):
            self.img.rotateX( rotX )
        if ( np.abs(rotY) > ZERO_ANGLE ):
            self.img.rotateY( rotY )
        if ( np.abs(rotZ) > ZERO_ANGLE ):
            self.img.rotateZ( rotZ )

        self.img.updatePlots()
