import numpy as np
import torch
import yaml
import os
from collections.abc import Iterable
from typing import Union, Tuple
import copy
import torch
from torch import Tensor
from torch_geometric.data import Data
from torch_geometric.utils import add_self_loops, negative_sampling
from torch_geometric.transforms import BaseTransform
import networkx as nx
def load_config(path):
    if os.path.isfile(path):
        with open(path,'r') as fin:
            config=yaml.safe_load(fin)
        return config
    else:
        raise FileNotFoundError('Not found config file..')
def dict_sequential(obj):
    if isinstance(obj,dict):
        back={}

        for k,v in obj.items():
            back[k]=dict_sequential(v)
    elif isinstance(obj,np.ndarray) or isinstance(obj,torch.Tensor):
        back=obj.tolist()
    elif isinstance(obj,str):
        back=obj
    elif isinstance(obj,Iterable):
        back=[]
        for i in obj:
            back.append(dict_sequential(i))
    elif isinstance(obj,float):
        back=float(obj)
    elif isinstance(obj,int):
        back=int(obj)
    elif hasattr(obj,'__str__'):
        return str(obj)
    return back
def edge_index2Graph(edge_index,Start_G=None,directed=False):
        if torch.is_tensor(edge_index):
            edge_index=edge_index.T.tolist()
        if not Start_G:
            G=nx.Graph()
        else:
            G=Start_G
        G.add_edges_from(edge_index)
        if not directed:
            G.to_undirected()
        return G
def get_ticks(types: list):
    loc=[0]
    ticks=[]
    last=types[0]
    for k,i in enumerate(types):
        if i!=last:
            loc.append(k)
        last=i
        if i not in ticks:
            ticks.append(i)
    
    loc.append(len(types))
    res_loc=[]
    print(loc)
    last=loc[0]
    for k,i in enumerate(loc[1:]):
        res_loc.append((last+i)/2)
        last=i
    assert len(res_loc)==len(ticks)
    return res_loc,ticks


