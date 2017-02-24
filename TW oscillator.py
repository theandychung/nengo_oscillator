import matplotlib.pyplot as plt
import nengo
from nengo.utils.functions import piecewise
import math

import numpy as np



#initial values
I = 0.11
gamma = 2.1
beta = 0.1
eta = 0.35

tau=.1;
model = nengo.Network(label='WT Oscillator')
with model:
    inp = nengo.Node(I)
    oscillator = nengo.Ensemble(850, dimensions=2, radius=20)
 #                               neuron_type=nengo.Sigmoid(tau_ref=0.002))
     # osc to osc connection
    def feedback(x):
        x,y = x
        dx =  3 * x - x**3 + 2 - y
        dy = eta * (gamma * (1 + math.tanh(x / beta)) - y)
        return [tau*dx+x, tau*dy+y]
    nengo.Connection(oscillator, oscillator, function=feedback, synapse=tau)
    # inp to osc connection
    nengo.Connection(inp,oscillator[0], transform = tau)

################################################################################
#probes
    oscillatorx_pr = nengo.Probe(oscillator[0],synapse=tau/10)
    #oscillatory_pr = nengo.Probe(oscillator[1], synapse=tau / 10)
    #inp_probe = nengo.Probe(inp,synapse = tau/10)

#run
with nengo.Simulator(model) as sim:
    sim.run(33)

#plot
import matplotlib.pyplot as plt
plt.plot(sim.trange(),sim.data[oscillatorx_pr], label="Oscillator x output")
#plt.plot(sim.trange(),sim.data[oscillator_yprobe], label="Oscillator y output")

#plt.plot(sim.trange(), sim.data[inp_probe], 'r', label="Input")
plt.title("Time Domain")
plt.xlabel("Time (s)")
plt.ylabel("x activity")
plt.ylim(-5, 5);
plt.legend();
plt.show()
#prettify()
#plt.legend(['$x_0$', '$x_1$', '$\omega$']);