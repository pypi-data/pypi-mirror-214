"""
Layer class for GANs
"""

import sys
import numpy as np

from .Layer import Layer

class GAN_Layer(Layer):
    """
    Layer class for GANs    
    """

    def __init__(self, n_neurons, r, n_layers, activation, loss, bias=False,
                 batch_size=1, lamb=0.0, on_gpu=False, **kwargs):

        super().__init__(n_neurons, r, n_layers, activation, loss, bias=bias,
                         batch_size=batch_size, lamb=lamb, 
                         on_gpu=on_gpu, **kwargs)

    # def compute_loss(self, y_i):
               
    #     # only compute if in an output layer
    #     assert self.layer_rp1 is None, "must be an output layer"
        
    #     self.L_i = - y_i * np.log(self.h) - (1 - y_i) * np.log(1 - self.h) 

    # def compute_delta_oo(self, y_i):
      
    #     # if the neuron is in the output layer, initialze delta_oo
    #     assert self.layer_rp1 is None, "must be an output layer"

    #     self.delta_ho = -1 / (self.h - (1 - y_i))

    #     # compute the loss function
    #     self.compute_loss(y_i)

    # def back_prop(self, y_i):

    #     if self.r == self.n_layers:
    #         self.compute_delta_oo(y_i)
    #     else:
    #         self.compute_delta_ho()

    #     # do not compute the loss gradient in the input layer, this is done
    #     # in the output layer of the Generator
    #     if self.r > 0:
    #         self.compute_L_grad_W()

    # def back_prop_G(self):

    #     if self.r < self.n_layers:
    #         self.compute_delta_ho()

    #     self.compute_L_grad_W()