import torch
import torch_geometric.transforms as T
from torch_geometric.nn import GCNConv,GINConv
from torch.nn import Sequential, Linear, BatchNorm1d, ReLU,LayerNorm
from torch.nn.init import xavier_normal_,xavier_uniform_
import torch.nn.functional as F
import numpy as np
from torch_geometric.nn.conv import MessagePassing
class node_attr_encoder(torch.nn.Module):
    def __init__(self, config):
        super(node_attr_encoder, self).__init__()
        self.model_config = config
        self.drop1 = torch.nn.Dropout(inplace=True)
        if (self.model_config['num_node']) is None or (self.model_config['use_type_info']):
            self.x_embddings = torch.nn.Linear(self.model_config['type_dim'], self.model_config['dim'], bias=False)
        else:
            self.x = torch.nn.Parameter(
                torch.empty(size=(self.model_config['num_node'], self.model_config['dim']), dtype=torch.float32),
                requires_grad=True)
            xavier_normal_(self.x)

    def forward(self, x):
        if (self.model_config['num_node']) is None or (self.model_config['use_type_info']):
            x = self.x_embddings(x)
            x = self.drop1(x)
        else:
            x = self.x
        return x
class convLayer(torch.nn.Module):
    def __init__(self,conv:MessagePassing,use_type_info=None,activation='relu',dropout='0.5'):
        self.conv=conv
        if activation=='relu':
            self.activ=torch.nn.ReLU()
        else:
            pass
        if dropout is not None:
            self.drop=torch.nn.Dropout(inplace=True)
    def forward(self, x=None, edge_index=None,
                edge_weight = None):
        x=self.conv(x,edge_index,edge_weight=edge_weight)
        if hasattr(self,'activ'):
            x=self.activ(x)
        x=self.activ(x)
        if hasattr(self,'drop'):
            x=self.drop(x)
        return x

class GCN(torch.nn.Module):
    def __init__(self, config):
        super().__init__()
        self.model_config = config
        self.node_attr_layer=node_attr_encoder(config)
        self.conv1=GCNConv(self.model_config['dim'], self.model_config['hidden_channels'])
        
        
        self.relu1=torch.nn.ReLU()
        self.drop1=torch.nn.Dropout(inplace=True)
        self.conv2 = GCNConv(self.model_config['hidden_channels'], self.model_config['out_channels'])

    def forward(self,x=None, edge_index=None):

        x=self.node_attr_layer(x)
       
        x=self.conv1(x,edge_index)
        x=self.relu1(x)
        x=self.drop1(x)
        x=self.conv2(x,edge_index)
        return x

class MLP(torch.nn.Module):
    def __init__(self,config):
        super().__init__()
        self.model_config = config
        self.node_attr_layer=node_attr_encoder(config)
        
        #self.convs = torch.nn.ModuleList()
        self.conv1=torch.nn.Linear(self.model_config['dim'], self.model_config['hidden_channels'])
        self.relu1=torch.nn.ReLU()
        self.drop1=torch.nn.Dropout(inplace=True)
        self.conv2=torch.nn.Linear(self.model_config['hidden_channels'], self.model_config['out_channels'])
    def forward(self,x=None, edge_index=None):
        x=self.node_attr_layer(x)
        x=self.conv1(x)
        x=self.relu1(x)
        x=self.drop1(x)
        x=self.conv2(x)
        return x
class GCN2(torch.nn.Module):
    def __init__(self, config):
        super().__init__()
        self.model_config = config
        self.node_attr_layer=node_attr_encoder(config)
        self.num_layers=config['num_layer']
        self.hidden=config['hidden_channels']
        self.out_channel=config['out_channels']
        self.conv1=GCNConv(self.model_config['dim'], self.out_channel)
        self.convs = torch.nn.ModuleList()
        for i in range(self.num_layers - 1):
            self.convs.append(Sequential(
                        ReLU(),
                        torch.nn.Dropout(inplace=True),
                        GCNConv(self.out_channel,self.out_channel),
                    ))
    def forward(self,x=None, edge_index=None):
        x=self.node_attr_layer(x)
        x=self.conv1(x,edge_index)
        for conv in self.convs:
            x=conv[0](x)
            x=conv[1](x)
            x=conv[2](x,edge_index)
        return x 
class GIN(torch.nn.Module):
    def __init__(self, config):
        super().__init__()
        self.model_config = config
        self.num_layers=config['num_layer']
        self.hidden=config['hidden_channels']
        self.out_channel=config['out_channels']
        self.node_attr_layer=node_attr_encoder(config)
        nn1=Sequential(Linear(self.model_config['dim'], 128),torch.nn.ReLU(),Linear(128, self.out_channel))
        self.conv1 = GINConv(nn1, train_eps=True)
        self.convs = torch.nn.ModuleList()
        for i in range(self.num_layers - 1):
            self.convs.append(
                GINConv(
                    Sequential(
                        Linear(self.out_channel, 256),
                        ReLU(),
                        Linear(256,self.out_channel),
                        ReLU()
                    ), train_eps=True))
    def forward(self,x=None, edge_index=None):
        x=self.node_attr_layer(x)
        x=self.conv1(x,edge_index)
        for conv in self.convs:
            x=conv(x,edge_index)
        return x


if __name__=='__main__':
    pass