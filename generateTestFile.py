import numpy as np

def ellipticFunction(X,Y,Z):
    R =  (X/1.0)**2 + (Y/0.5)**2 + (Z/0.25)**2
    values = np.zeros(R.shape)
    values[R<1.0] = np.sqrt(1.0 - values[R<1.0])
    return values

def main():
    x = np.linspace( -1.0, 1.0, 101 )
    y = np.linspace( -1.0, 1.0, 150 )
    z = np.linspace( -1.0, 1.0, 200 )

    X,Y,Z = np.meshgrid(x,y,z)

    values = ellipticFunction( X,Y,Z )
    values *= (255.0/values.max())

    # Convert to uint8
    values = values.astype(np.uint8)

    res = 200
    # Save in raw binary format
    fname = "exampleFile_%d_%d_%d_%d.raw"%(res,values.shape[0],values.shape[1],values.shape[2])
    values.tofile( fname )

    print ("Example file written to %s"%(fname))

if __name__ == "__main__":
    main()
