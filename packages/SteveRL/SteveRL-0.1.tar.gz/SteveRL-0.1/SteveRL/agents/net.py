import math
import torch
import torch.nn as nn
from torch import Tensor
from torch.distributions.normal import Normal


"""DQN"""

class QNetBase(nn.Module):
    def __init__(self,state_dim:int,action_dim:int):
        super().__init__()
        self.explore_rate =0.125

        self.state_dim =state_dim
        self.action_dim =action_dim
        self.net =None

        self.state_avg= nn.Parameter(torch.zeros((state_dim,)),requires_grad=False)
        self.state_std =nn.Parameter(torch.zeros((state_dim,)),requires_grad=False)
        self.value_avg =nn.Parameter(torch.zeros((1,)),requires_grad=False)
        self.value_std = nn.Parameter(torch.zeros((1,)), requires_grad=False)

    def state_norm(self,state:Tensor)->Tensor:
        return  (state -self.state_avg)/self.state_std

    def value_norm(self,value:Tensor)->Tensor:
        return (value- self.value_avg)/self.value_std


"""Actor (policy network)"""

class ActorBase(nn.Module):
    def __init__(self,state_dim:int,action_dim:int):
        super().__init__()
        self.state_dim =state_dim
        self.action_dim =action_dim
        self.net =None
        self.explore_noise_std =None
        self.ActionDist =torch.distributions.normal.Normal

        self.state_avg = nn.Parameter(torch.zeros((state_dim,)), requires_grad=False)
        self.state_std = nn.Parameter(torch.ones((state_dim,)), requires_grad=False)

    def state_norm(self,state:Tensor)->Tensor:
        x = self.state_std
        y = self.state_avg
        return (state -self.state_avg)/self.state_std





"""Critic (value network)"""

class CriticBase(nn.Module):
    def __init__(self,state_dim:int,action_dim:int):
        super().__init__()
        self.state_dim =state_dim
        self.action_dim =action_dim
        self.net = None

        self.state_avg = nn.Parameter(torch.zeros((state_dim,)), requires_grad=False)
        self.state_std = nn.Parameter(torch.ones((state_dim,)), requires_grad=False)
        self.value_avg = nn.Parameter(torch.zeros((1,)), requires_grad=False)
        self.value_std = nn.Parameter(torch.ones((1,)), requires_grad=False)

    def state_norm(self, state: Tensor) -> Tensor:
        return (state - self.state_avg) / self.state_std  # todo state_norm

    def value_re_norm(self, value: Tensor) -> Tensor:
        return value * self.value_std + self.value_avg  # todo value_norm


def bulid_mlp(dims:[int],activation: nn= None,if_raw_out:bool =True)-> nn.Sequential:

    if activation is None:
        activation =nn.ReLU
    net_list =[]
    for i in range(len(dims)-1):
        net_list.extend([nn.Linear(dims[i],dims[i+1]),activation()])
    if if_raw_out:
        del net_list[-1]  # delete the activation function of the output layer to keep raw output
    return nn.Sequential(*net_list)

def layer_init_with_orthogonal(layer, std=1.0, bias_const=1e-6):
    torch.nn.init.orthogonal_(layer.weight, std)
    torch.nn.init.constant_(layer.bias, bias_const)