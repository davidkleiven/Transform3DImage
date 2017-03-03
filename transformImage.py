import sys
import tkinter as tk
import transform3DApp as tf3
import numpy as np

def extractDimensions( fname ):
    splitFname = fname.split("_")
    if ( len(splitFname) != 5 ):
        msg = "Unexpected format of the filename. Should be prefix_resolution_Nx_Ny_Nz.raw"
        raise( Exception(msg) )
    res = int( splitFname[1] )
    Nx = int( splitFname[2] )
    Ny = int( splitFname[3] )
    Nz = int( splitFname[4].split(".")[0] )
    return res, Nx, Ny, Nz

def main( argv ):
    if ( len(argv) < 1 ) or ( len(argv) > 2 ):
        print ( "Usage: python3 transformImage.py rawBinaryFile.raw --order=(C,F)" )
        return
    fname = argv[0]
    order = "C"
    for arg in argv:
        if ( arg.find("--order=") != -1 ):
            order = arg.split("--order=")[1]
    try:
        root = tk.Tk()
        root.wm_title("3D Image Transformer")
        ci = tf3.ControlInterface( root )
        res, Nx, Ny, Nz = extractDimensions( fname )
        ci.img.pixels = np.fromfile(fname, dtype=np.uint8)
        ci.img.prefix = fname.split("_")[0]+"Rotated"
        ci.img.resolution = res
        ci.img.order = order

        if ( len(ci.img.pixels) != Nx*Ny*Nz ):
            print ("Expected length: %d. Length of array from file %d"%(Nx*Ny*Nz, len(ci.img.pixels)))
            return 1

        ci.img.pixels = ci.img.pixels.reshape((Nx,Ny,Nz), order=order)

        root.mainloop()
    except Exception as exc:
        print (str(exc))
        return 1
    return 0

if __name__ == "__main__":
    main( sys.argv[1:] )
