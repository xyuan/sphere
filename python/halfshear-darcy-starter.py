#!/usr/bin/env python
import sphere
import numpy
import sys

# launch with:
# $ ipython halfshear-darcy-starter.py <device> <fluid> <c_phi> <k_c> <sigma_0> <mu>

device = int(sys.argv[1])
wet = int(sys.argv[2])
c_phi = float(sys.argv[3])
k_c = float(sys.argv[4])
sigma0 = float(sys.argv[5])
mu = float(sys.argv[6])

if wet == 1:
    fluid = True
else:
    fluid = False
    
sim = sphere.sim('halfshear-sigma0=' + str(sigma0), fluid=False)
print('Input: ' + sim.sid)
sim.readlast()

sim.fluid = fluid
if fluid:
    sim.id('halfshear-darcy-sigma0=' + str(sigma0) + '-k_c=' + str(k_c) + \
            '-mu=' + str(mu) + '-shear')
else:
    sim.id('halfshear-sigma0=' + str(sigma0) + '-shear')

sim.checkerboardColors(nx=6,ny=3,nz=6)
sim.cleanup()
sim.adjustUpperWall()
sim.zeroKinematics()

#sim.shear(0.0/20.0)

if fluid:
    #sim.num[2] *= 2
    sim.num[:] /= 2
    #sim.L[2] *= 2.0
    #sim.initFluid(mu = 1.787e-6, p = 600.0e3, cfd_solver = 1)
    sim.initFluid(mu = 1.787e-6, p = 0.0, cfd_solver = 1)
    sim.setFluidBottomNoFlow()
    sim.setFluidTopFixedPressure()
    #sim.setDEMstepsPerCFDstep(100)
    sim.setMaxIterations(2e5)
    sim.beta_f[0] = mu
    sim.k_c[0] = k_c

sim.w_devs[0] = sigma0
sim.w_m[0] = numpy.abs(sigma0*sim.L[0]*sim.L[1]/sim.g[2])

sim.setStiffnessNormal(36.4e9)
sim.setStiffnessTangential(36.4e9/3.0)
sim.mu_s[0] = 0.5
sim.mu_d[0] = 0.5
sim.setDampingNormal(0.0)
sim.setDampingTangential(0.0)
#sim.deleteAllParticles()
sim.fixvel[:] = -1.0

#sim.initTemporal(total = 20.0, file_dt = 0.01, epsilon=0.07)
sim.initTemporal(total = 1.0e-4, file_dt = 1.0e-5, epsilon=0.07)

# Fix lowermost particles
#dz = sim.L[2]/sim.num[2]
#I = numpy.nonzero(sim.x[:,2] < 1.5*dz)
#sim.fixvel[I] = 1

sim.run(dry=True)
sim.run(device=device)
sim.writeVTKall()
#sim.visualize('walls')
#sim.visualize('fluid-pressure')
