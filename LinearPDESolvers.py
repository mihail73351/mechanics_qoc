import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as splin


class ExplicitEulerSolver:

    def __init__(self, hs, cCoef):
        '''
        Input
        float[] hs -- the steps of the discretization, [d+1], the first is the time
        '''
        super(ExplicitEulerSolver,self).__init__()

        self.hs = hs
        self.cCoef = cCoef
        self.dim = hs.shape[0]-1
        print(self.dim)


    def solveBVProblem1D(self, uInits, numSteps, rightPart=None, spaceGrid=None):
        '''
            Solves Dirichlet Boundary-Value Problem
            Input
            float[] uInits -- two initial layers of shape [2,...dims...]
            int numSteps -- number of time steps
            funcHandler rightPart -- right part depending on time and space (t,x)
            float[][] spaceGrid -- space grid of points
        '''

        #trim inits
        uSol = [ (uInits[0,...])[None,...], (uInits[1,...])[None,...] ]
        shape= np.array(list(uSol[0].shape)[1:])-2#-2 for dirichlet, trimmed shape for later restoration
        uSol[0] = np.take(uSol[0],np.arange(1,uSol[0].shape[1]-1),axis=1)
        uSol[1] = np.take(uSol[1],np.arange(1,uSol[1].shape[1]-1),axis=1)
        uSol[0] = np.reshape(uSol[0], newshape=(-1,), order='C')[None,:]
        uSol[1] = np.reshape(uSol[1], newshape=(-1,), order='C')[None,:]

        #assembling iteration matrix
        diags = self.hs[0]**2 *np.concatenate([self.cCoef**2 /(self.hs[1]**2) * np.ones([1,shape[0]]),
                    (2/(self.hs[0]**2) - 2*self.cCoef**2 /(self.hs[1]**2) ) * np.ones([1,shape[0]]),
                     self.cCoef**2  /(self.hs[1]**2) * np.ones([1,shape[0]])],axis=0)
        offsets = np.array([-1,0,1])
            
        C = sps.spdiags(diags,offsets, m=len(diags[1]),n=len(diags[1]), format="csr")

        for i in np.arange(numSteps-1):
            if(rightPart is None):
                toAdd = C@uSol[-1][0,:] - uSol[-2][0,:]
            else:
                toAdd = C@uSol[-1][0,:] - uSol[-2][0,:] + np.reshape(rightPart(self.hs[0]*(i+2),spaceGrid),newshape=(-1,))
            uSol.append(toAdd[None,:])

        uSol=np.concatenate(uSol, axis=0)
        toShape= tuple([uSol.shape[0]] + [shape[j] for j in np.arange(len(shape))])
        return np.pad(np.reshape(uSol, newshape=toShape), pad_width=[(0,0)]+[(1,1) for _ in np.arange(self.dim)])