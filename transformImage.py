import sys
import tkinter as tk
import transform3DApp as tf3
import numpy as np

def extractDimensions( fname ):
    splitFname = fname.split("_")
    if ( len(splitFname) != 5 ):
        msg = "Unexpected format of the filename. Should be prefix_resolution_Nx_Ny_Nz.raw"
        raise( Exception(msg) )
    Nx = int( splitFname[2] )
    Ny = int( splitFname[3] )
    Nz = int( splitFname[4].split(".")[0] )
    return Nx, Ny, Nz

def main( argv ):
    if ( len(argv) != 1 ):
        print ( "Usage: python3 transformImage.py rawBinaryFile.raw" )
        return
    fname = argv[0]
    try:
        root = tk.Tk()
        root.wm_title("3D Image Transformer")
        ci = tf3.ControlInterface( root )
        Nx, Ny, Nz = extractDimensions( fname )
        ci.img.pixels = np.fromfile(fname, dtype=np.uint8)
        print (ci.img.pixels)

        if ( len(ci.img.pixels) != Nx*Ny*Nz ):
            print ("Expected length: %d. Length of array from file %d"%(Nx*Ny*Nz, len(ci.img.pixels)))
            return 1

        ci.img.pixels = ci.img.pixels.reshape((Ny,Nx,Nz))

        root.mainloop()
    except Exception as exc:
        print (str(exc))
        return 1
    return 0

if __name__ == "__main__":
    main( sys.argv[1:] )
