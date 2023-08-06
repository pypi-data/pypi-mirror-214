

import os.path as osp
from torch.nn import init
from torch.nn import Sequential, LSTM,Linear, BatchNorm1d, ReLU,LayerNorm,Dropout,Bilinear
import torch
import torch_geometric.transforms as T
import torch.nn.functional as F
from .PairEncoder import NeighEnco2

class dot_predictor(torch.nn.Module):
    def forward(self,e1,e2):
        x=e1*e2
        x=x.sum(dim=-1)
        x=x.view(-1)
        x=torch.sigmoid(x)
        return x
class mlp_predictor(torch.nn.Module):
    def __init__(self,config) -> None:
        super().__init__()
        self.mlp=torch.nn.Sequential(Linear(config['out_channels']*2,256,bias=True),Dropout(inplace=True),ReLU(inplace=True),\
            Linear(256,128,bias=True),Dropout(inplace=True),ReLU(inplace=True),Linear(128,1,bias=False))
   
    def forward(self,e1,e2):
        x=torch.cat((e1,e2),1)
        x=self.mlp(x)
        x=torch.sigmoid(x)
        x=x.view(-1)
        return x
class mlptri_predictor(torch.nn.Module):
    def __init__(self,config) -> None:
        super().__init__()
        self.mlp=torch.nn.Sequential(Linear(config['out_channels']*3,256,bias=True),Dropout(inplace=True),ReLU(inplace=True),\
            Linear(256,128,bias=True),Dropout(inplace=True),ReLU(inplace=True),Linear(128,1,bias=False))
    def forward(self,e1,e2,n):
        x=torch.cat((e1,e2,n),1)
        x=self.mlp(x)
        x=torch.sigmoid(x)
        x=x.view(-1)
        return x
class lstm_predictor(torch.nn.Module):
    def __init__(self,config) -> None:
        super().__init__()
        self.hidden_size=128
        self.num_layers=1
        self.lstm=LSTM(config['out_channels'], self.hidden_size, self.num_layers, batch_first=True)
        self.mlp = Sequential(
            Linear(self.hidden_size, 75),
            ReLU(),
            Linear(75, 1)
        )
    def forward(self,e1,e2,n=None):
        if n is not None:
            x=torch.stack((e1,e2,n),1)
        else:
            x=torch.stack((e1,e2),1)
            
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = out[:, -1, :]
        x=self.mlp(out)
        x=torch.sigmoid(x)
        x=x.view(-1)
        return x
    

class biliear_predictor(torch.nn.Module):
    def __init__(self,config) -> None:
        super().__init__()
        self.bilin=Bilinear(in1_features=config['out_channels'],in2_features=config['out_channels'],out_features=config['out_channels'])
        #Linear(config['out_channels']*2,self.dim)
    def forward(self,e1,e2):
        x=self.bilin(e1,e2)
        x=x.sum(dim=-1)
        x=x.view(-1)
        return x

class joint_predictor(torch.nn.Module):
    def __init__(self,config) -> None:
        super().__init__()
        self.model_config = config
        self.mlp=torch.nn.Sequential(Linear(config['out_channels']*2,256,bias=True),Dropout(inplace=True),ReLU(inplace=True),\
            Linear(256,config['out_channels'],bias=True))
        self.lin1=torch.nn.Linear(config['out_channels'],1,bias=True)

    def forward(self,x1,x2,x3):
        x=torch.cat((x1,x2),1)
        p1=self.mlp(x)
        p=torch.stack([p1,x3],dim=1)
        p=p.permute(0,2,1)
        p=F.adaptive_max_pool1d(p,1).squeeze()
        p=self.lin1(p)
        p=p.view(-1)
        p=torch.sigmoid(p)
        return p
    def forward_emb(self,x1,x2,x3):
        x=torch.cat((x1,x2),1)
        p1=self.mlp(x)
        p=torch.stack([p1,x3],dim=1)
        p=p.permute(0,2,1)
        p=F.adaptive_max_pool1d(p,1).squeeze()
        return p


class LinkPred(torch.nn.Module):
    def __init__(self,config):
        super(LinkPred, self).__init__()
        if 'score_func' in config:
            if config['score_func']=='dot':
                self.predictor=dot_predictor()
            elif config['score_func']=='mlp':
                self.predictor=mlp_predictor(config)
            elif config['score_func']=='joint':
                self.predictor=joint_predictor(config)
            elif config['score_func']=='mlptri':
                self.predictor=mlptri_predictor(config)
            elif config['score_func']=='lstm':
                self.predictor=lstm_predictor(config)
                
        else:
            self.predictor=dot_predictor()
        if 'pair_encoder' in config:
            self.use_neighbor_enco=True
            self.nei_encoder=NeighEnco2(config)
        else:
            self.use_neighbor_enco=False
    def forward(self, z=None, edge_label_index=None,**kwargs):
        x1,x2=z[edge_label_index[0]],z[edge_label_index[1]]
        
        if 'neighbor' in kwargs and self.use_neighbor_enco:
            x3=self.nei_encoder(z,kwargs['neighbor'])
            x=self.predictor(x1,x2,x3)
        else:
            x=self.predictor(x1,x2)
        return x
