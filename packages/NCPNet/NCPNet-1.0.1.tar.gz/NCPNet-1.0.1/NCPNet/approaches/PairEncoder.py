import torch
import torch_geometric.transforms as T
import torch.nn as nn
from torch_geometric.nn import GCNConv,SAGEConv,GATConv,GatedGraphConv,ChebConv,GINConv,DeepGCNLayer
from torch.nn import Sequential, Linear, BatchNorm1d, ReLU,LayerNorm
from torch.nn.init import xavier_normal_,xavier_uniform_,uniform_
import torch.nn.functional as F

class NeighEnco(torch.nn.Module):
    def __init__(self,config) -> None:
        super().__init__()
        self.model_config = config
        self.lin=Linear(self.model_config['out_channels'],1)
        self.zero_holder=torch.zeros(size=(1,self.model_config['out_channels']),device=self.model_config['device'])
        uniform_(self.lin.weight.data,a=0.2,b=0.8)

    def forward(self,z,neighbor=None):
        z_=torch.cat([self.zero_holder,z],dim=0)
        z_=z_.detach()
        n,l=neighbor.size(0),neighbor.size(1)
        neighbor=neighbor.view(-1) 
        x=F.embedding(neighbor,z_)
        x=x.view(n,l,x.size(1))
        x=torch.sum(x,dim=1,keepdim=False)
        x=self.lin(x)
        x=x.view(-1)
        x=torch.relu(x)
        return x
class Lookup_neighbor_embedding(torch.nn.Module):
    def __init__(self,config) -> None:
        super().__init__()
        self.model_config = config
        self.zero_holder=torch.nn.Parameter(torch.zeros(size=(1,self.model_config['out_channels']),device=self.model_config['device']),requires_grad=False)


    def forward(self,z,neighbor=None):
        z_=torch.cat([self.zero_holder,z],dim=0)
        z_=z_.detach()
        n,l=neighbor.size(0),neighbor.size(1)
        neighbor=neighbor.view(-1) 
        x=F.embedding(neighbor,z_)
        x=x.view(n,l,x.size(1))
        return x
class NeighEnco2(torch.nn.Module):
    def __init__(self,config) -> None:
        super().__init__()
        self.model_config = config
        self.lookupneigh=Lookup_neighbor_embedding(config)
        self.conv1=torch.nn.Conv1d(config['out_channels'],int(config['out_channels']*0.5),kernel_size=1,bias=False)

        self.act_f1=nn.LeakyReLU(0.05)
        self.dp1=torch.nn.Dropout(inplace=True)
        
        self.conv2=torch.nn.Conv1d(int(config['out_channels']*0.5),config['out_channels']-int(config['out_channels']*0.5),kernel_size=1,bias=False)
        self.act_f2=nn.LeakyReLU(0.05)
        self.dp2=torch.nn.Dropout(inplace=True)
    def forward(self,z,neighbor=None):
        x=self.lookupneigh(z,neighbor)
        x=x.permute((0,2,1)).contiguous()
        x=self.conv1(x)
        x=self.act_f1(x)
        x1=self.dp1(x)
        x2=self.conv2(x1)
        x2=self.act_f2(x2)
        x2=self.dp2(x2)
        x=torch.cat([x1,x2],dim=1)
        x=F.adaptive_max_pool1d(x,1).squeeze()
    
        #x=x.mean(dim=2)
        return x