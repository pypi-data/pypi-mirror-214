from hashlib import new
from typing import Optional, Callable, List

import os.path as osp
import numpy as np
from sklearn import neighbors

import torch
from torch.utils.data import DataLoader,Sampler
import torch_geometric
from torch_geometric.data import InMemoryDataset, download_url
from torch_geometric.io import read_planetoid_data
from torch_geometric.data import Data
from torch_geometric.utils import negative_sampling
import networkx as nx
import random

class HemiBrain(InMemoryDataset):
    r"""
    Args:
        root (string): Root directory where the dataset should be saved.
        transform (callable, optional): A function/transform that takes in an
            :obj:`torch_geometric.data.Data` object and returns a transformed
            version. The data object will be transformed before every access.
            (default: :obj:`None`)
        pre_transform (callable, optional): A function/transform that takes in
            an :obj:`torch_geometric.data.Data` object and returns a
            transformed version. The data object will be transformed before
            being saved to disk. (default: :obj:`None`)
    """

    url = 'null'

    def __init__(self, root: str,split='node', transform: Optional[Callable] = None,
                 pre_transform: Optional[Callable] = None,process=False,restore_split=None,device=None):

        super().__init__(root, transform, pre_transform)
        if device is None:
            self.device='cpu'
        else:
            self.device=device
        if process:
            self._process()
        if restore_split is None:
            self.data, self.slices = torch.load(self.processed_paths[0],map_location=self.device)
        elif isinstance(restore_split,str):
            self.data= torch.load(restore_split,map_location=self.device)
        self.data, self.slices = self.collate([self.data])

    @property
    def num_edges(self):
        return self.data.edge_index.size(0)
    @property
    def edge_index(self):
        return self.data.edge_index
    @property
    def y(self):
        return self.data.y
    
    @property
    def num_nodes(self):
        return self.data.num_nodes
    @property
    def raw_dir(self) -> str:
        return osp.join(self.root, 'raw')

    @property
    def processed_dir(self) -> str:
        return osp.join(self.root, 'processed')

    @property
    def raw_file_names(self) -> List[str]:
        return ['edges.txt','edges_ROI.txt','nuron-label.txt','neuron2ID.txt']

    @property
    def processed_file_names(self) -> str:
        return 'data.pt'
    @property
    def neu2ID(self):
        if hasattr(self,'neu2ID_dict'):
            return self.neu2ID_dict
        else:
            neu2ID={}
            with open(osp.join(self.raw_dir,'neuron2ID.txt'),'r') as fin:
                for i in fin.readlines():
                    line=i.strip().split(',')
                    neu2ID[line[0]]=int(line[1])
            self.neu2ID_dict=neu2ID
            return self.neu2ID_dict
    @property
    def label2ID(self):
        if hasattr(self,'label2ID_dict'):
            return self.label2ID_dict
        else:
            self.neuron2label_dict={}
            with open(osp.join(self.raw_dir,'neuron-label.txt'),'r') as fin:
                for i in fin.readlines():
                    line = i.strip().split('\t')
                    self.neuron2label_dict[line[0]]=line[1]
            label_set= set(self.neuron2label_dict.values())
            self.label2ID_dict={l:k for k,l in enumerate(label_set)}
            return self.label2ID_dict
    @property
    def neuron2label(self):
        if hasattr(self,'neuron2label_dict'):
            return self.neuron2label_dict
        else:
            self.neuron2label_dict={}
            with open(osp.join(self.raw_dir,'neuron-label.txt'),'r') as fin:
                for i in fin.readlines():
                    line = i.strip().split('\t')
                    self.neuron2label_dict[line[0]]=line[1]
            label_set= set(self.neuron2label_dict.values())
            self.label2ID_dict={l:k for k,l in enumerate(label_set)}
            return self.neuron2label_dict
    @property
    def typedim(self):
        if hasattr(self,'cache_type_dim'):
            return self.cache_type_dim
        else:
            label2ID=self.label2ID
            self.cache_type_dim=len(label2ID.keys())
            return self.cache_type_dim

    @staticmethod
    def read_data(raw_dir):
        neu2ID={}
        with open(osp.join(raw_dir,'neuron2ID.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(',')
                neu2ID[line[0]]=int(line[1])
        ID2neu={v:k for k,v in neu2ID.items()}
        edge_index=[]
        edge_attr=[]
        with open(osp.join(raw_dir,'edges.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(',')
                if len(line)==3:
                    edge_index.append([neu2ID[line[0]],neu2ID[line[1]]])
                    edge_attr.append([int(line[2])])

        edge_index=torch.Tensor(edge_index)
        edge_index=torch.transpose(edge_index,0,1)
        edge_index=edge_index.to(dtype=torch.int64)
        edge_attr=torch.Tensor(edge_attr)
        neuron2label={}
        with open(osp.join(raw_dir,'neuron-label.txt'),'r') as fin:
            for i in fin.readlines():
                line = i.strip().split('\t')
                neuron2label[line[0]]=line[1]
        label_set= set(neuron2label.values())
        label2ID={l:k for k,l in enumerate(label_set)}

        y=[]
        for i_neuron in range(len(ID2neu)):
            label_x=neuron2label[ID2neu[i_neuron]]
            y.append(label2ID[label_x])
        y=torch.tensor(y)

        x=torch.nn.functional.one_hot(y)
        x=x.to(dtype=torch.float32)

        return Data(x=x,edge_index=edge_index,y=y,edge_attr=edge_attr,neu2ID=neu2ID,label2ID=label2ID)

    def process(self):
        data = self.read_data(self.raw_dir)
        data = data if self.pre_transform is None else self.pre_transform(data)
        torch.save(self.collate([data]), self.processed_paths[0])
    def manual_split(self,path):
        label2ID={}
        with open(osp.join(path,'label2ID.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    label2ID[line[0]]=int(line[1])
        neu2ID={}
        with open(osp.join(path,'neu2ID.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    neu2ID[line[0]]=int(line[1])
        
        for k,v in self.neu2ID.items():
            if neu2ID[k]!=v:
                raise ValueError('this file doesn`t match this object(%s)'%__name__)

        test_edge_index=[]
        with open(osp.join(path,'test_edge_list.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    n1,n2=int(line[0]),int(line[1])
                    test_edge_index.append([n1,n2])
        test_edge_index=torch.tensor(test_edge_index).T
        
  
        train_edge_index=[]
        with open(osp.join(path,'train_edge_list.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    n1,n2=int(line[0]),int(line[1])
                    train_edge_index.append([n1,n2])
        train_edge_index=torch.tensor(train_edge_index).T

        total_edges=test_edge_index.size(1)+train_edge_index.size(1)
        if test_edge_index.size(1)>int(total_edges*0.1):
            test_edge_index=test_edge_index[:,:int(total_edges*0.1)]

        test_edge_index=test_edge_index.to(device=self.data.x.device)
        train_edge_index=train_edge_index.to(device=self.data.x.device)


        test_data=Data(x=self.data.x,y=self.data.y,edge_index=test_edge_index,neu2ID=neu2ID,label2ID=label2ID)
        train_data=Data(x=self.data.x,y=self.data.y,edge_index=train_edge_index,neu2ID=neu2ID,label2ID=label2ID)
        return train_data,test_data





    def __repr__(self) -> str:
        return 'HemiBrain'

class LinkPred_Loader:
    def __init__(self,config,dataset: InMemoryDataset):
        self.dataset=dataset
        self.loader_config=config
        if 'negtive_num' in self.loader_config:
            self.negtive_num=self.loader_config['negtive_num']
        else:
            self.negtive_num=1

        if 'batch_size' in self.loader_config:
            self.batch_size=self.loader_config['batch_size']
        else:
            if dataset.edge_index.size(1)*(self.negtive_num+1)*self.loader_config['dim']<int(8*1024*1024*1024/12):
                self.batch_size=dataset.edge_index.size(1)
            else:
                self.batch_size=min(500000,dataset.edge_index.size(1))
        self.step=0
    def __iter__(self):
        self.step=0

        neg_edge_index = negative_sampling(
            edge_index=self.dataset.edge_index, num_nodes=self.dataset.num_nodes,
            num_neg_samples=self.dataset.edge_index.size(1)*self.negtive_num, method='sparse')
        self.edge_label_index = torch.cat(
            [self.dataset.edge_index, neg_edge_index],
            dim=-1
        )
        
        self.edge_label = torch.cat([
            self.dataset.edge_index.new_ones(self.dataset.edge_index.size(1),dtype=torch.float32),neg_edge_index.new_zeros(neg_edge_index.size(1),dtype=torch.float32)
        ], dim=0)
        perm = torch.randperm(self.edge_label_index.size(1),device=self.edge_label.device)
        self.batch_index=torch.split(perm,self.batch_size)
        # split_num=ceil(self.edge_label_index.size(1)/self.batch_size)
        # self.batchs_edge_index=torch.hsplit(self.edge_label_index,split_num)
        self.edge_label_index=self.edge_label_index.T
        self.edge_label=self.edge_label.T
        return self
    def __next__(self):
        if self.step>=len(self.batch_index):
            raise StopIteration
        else:
            ind=self.batch_index[self.step]
            edge_label_index=torch.nn.functional.embedding(ind,self.edge_label_index)
            edge_label_index=edge_label_index.T
            edge_label=torch.nn.functional.embedding(ind,self.edge_label)
            edge_label=edge_label.T
            batch=(self.dataset.x,self.dataset.edge_index,self.dataset.edge_attr,edge_label_index,edge_label)
            self.step+=1
        return batch
    def __len__(self):
        return len(self.batch_index)
class LinkPred_PairNeigh_Loader(LinkPred_Loader):
    def __init__(self,config,dataset: InMemoryDataset,nxg:nx.Graph,hop=1):
        self.dataset=dataset
        self.loader_config=config
        if 'negtive_num' in self.loader_config:
            self.negtive_num=self.loader_config['negtive_num']
        else:
            self.negtive_num=1

        if 'batch_size' in self.loader_config:
            self.batch_size=self.loader_config['batch_size']
        else:
            if dataset.edge_index.size(1)*(self.negtive_num+1)*self.loader_config['dim']<int(8*1024*1024*1024/12):
                self.batch_size=dataset.edge_index.size(1)
            else:
                self.batch_size=min(500000,dataset.edge_index.size(1))
        self.nxg={}
        for n in nxg.nodes():
            self.nxg[n]=set(nxg[n])
        for i in range(dataset.num_nodes):
            if i not in self.nxg:
                self.nxg[i]=set([])
        for i in range(hop-1):
            for n in self.nxg.keys():
                q=list(self.nxg[n])
                for j in q:
                    if j !=n:
                        for kj in self.nxg[j]:
                            if kj not in self.nxg[n] and kj!=n:
                                self.nxg[n].add(kj)
        self.cached_nxg_neighbors=None
        self.step=0
        self.max_pad_num=None
    def get_neighboor(self,edge_index,mode='inter',max_num=30):
        edge_index_list=edge_index.cpu().T.tolist()
        res=[]
     
        if mode=='inter':
  
            for edges in edge_index_list:
                u,v=tuple(edges)
                u_set,v_set=self.nxg[u],self.nxg[v]

                pair=u_set.intersection(v_set)
                pair=pair.difference({u,v})
                neigh=list(pair)
                if len(neigh)>max_num:
                    #random.sample(neigh,max_num)
                    res.append(random.sample(neigh,max_num))
                else:
                    res.append(neigh)
        res=[torch.tensor(i,dtype=torch.int32)+1 for i in res]
        out=torch.nn.utils.rnn.pad_sequence(res,batch_first=False).T
        return out
    def __iter__(self):
        self.step=0
        neg_edge_index = negative_sampling(
            edge_index=self.dataset.edge_index, num_nodes=self.dataset.num_nodes,
            num_neg_samples=self.dataset.edge_index.size(1)*self.negtive_num, method='sparse')
        if self.cached_nxg_neighbors is None:
            self.cached_nxg_neighbors=self.get_neighboor(self.dataset.edge_index)

        neg_nxg_neighbors=self.get_neighboor(neg_edge_index)

        if neg_nxg_neighbors.size(1)<self.cached_nxg_neighbors.size(1):
            d=self.cached_nxg_neighbors.size(1)-neg_nxg_neighbors.size(1)
            neg_nxg_neighbors=torch.cat([neg_nxg_neighbors,torch.zeros(size=(neg_nxg_neighbors.size(0),d),dtype=torch.int32)],dim=1)
        elif neg_nxg_neighbors.size(1)>self.cached_nxg_neighbors.size(1):
            d=neg_nxg_neighbors.size(1)-self.cached_nxg_neighbors.size(1)
            self.cached_nxg_neighbors=torch.cat([self.cached_nxg_neighbors,torch.zeros(size=(self.cached_nxg_neighbors.size(0),d),dtype=torch.int32)],dim=1)
        assert self.cached_nxg_neighbors.size(1)==neg_nxg_neighbors.size(1)

        self.neighbors=torch.cat([self.cached_nxg_neighbors,neg_nxg_neighbors],dim=0)
        self.neighbors=self.neighbors.to(device=self.loader_config['device'])
        self.edge_label_index = torch.cat(
            [self.dataset.edge_index, neg_edge_index],
            dim=-1
        )
        
        self.edge_label = torch.cat([
            self.dataset.edge_index.new_ones(self.dataset.edge_index.size(1),dtype=torch.float32),neg_edge_index.new_zeros(neg_edge_index.size(1),dtype=torch.float32)
        ], dim=0)
        perm = torch.randperm(self.edge_label_index.size(1),device=self.edge_label.device)
        self.batch_index=torch.split(perm,self.batch_size)
        # split_num=ceil(self.edge_label_index.size(1)/self.batch_size)
        # self.batchs_edge_index=torch.hsplit(self.edge_label_index,split_num)
        self.edge_label_index=self.edge_label_index.T
        self.edge_label=self.edge_label.T
        return self
    def __next__(self):
        if self.step>=len(self.batch_index):
            raise StopIteration
        else:
            ind=self.batch_index[self.step]
            edge_label_index=torch.nn.functional.embedding(ind,self.edge_label_index)
            edge_label_index=edge_label_index.T
            edge_label=torch.nn.functional.embedding(ind,self.edge_label)
            #edge_label=self.edge_label[ind]
            edge_label=edge_label.T
            batch_neighbor=torch.nn.functional.embedding(ind,self.neighbors)
            batch=(self.dataset.x,self.dataset.edge_index,self.dataset.edge_attr,edge_label_index,edge_label,batch_neighbor)
            self.step+=1
        return batch
    def __len__(self):
        return len(self.batch_index)

class NodeCla_Loader:
    '''for small graph'''
    def __init__(self,dataset: InMemoryDataset):
        self.dataset=dataset
        self.batch_num=1
        self.step=0
    def __iter__(self):
        self.step=0
        return self
    def __next__(self):
        if self.step >= self.batch_num:
            raise StopIteration
        batch=(self.dataset.x, self.dataset.edge_index,self.dataset.edge_attr,self.dataset.y,self.dataset.train_mask,self.dataset.test_mask)
        self.step+=1
        return batch
class Scale_NodeCla_Loader:
    def __init__(self,dataset: InMemoryDataset,subgraph_num=40,shuffle=True):
        self.dataset=dataset
        self.batch_num=subgraph_num
        self.step=0
        self.subgraph_num=subgraph_num
        self.chunk_size=int(self.dataset.edge_index.size()[1]/self.subgraph_num)
        self.shuffle=shuffle
        #self.update()
    def update(self):
        edge_index=self.dataset.edge_index
        edge_idx=np.arange(0,edge_index.size()[1])
        if self.shuffle:
            np.random.shuffle(edge_idx)
        device=edge_index.data.device
        self.iter_idx=torch.split(torch.from_numpy(edge_idx).to(device=device),self.chunk_size)
    def __iter__(self):
        self.update()
        return self
    def __next__(self):
        if self.step >= self.batch_num:
            raise StopIteration
        else:
            batch_id=self.iter_idx[self.step]
            batch_edge_index=torch.nn.functional.embedding(batch_id,self.dataset.edge_index.T)
            batch_edge_index=batch_edge_index.T
            batch=(self.dataset.x, batch_edge_index,self.dataset.edge_attr,self.dataset.y,self.dataset.train_mask,self.dataset.test_mask)
            self.step+=1
        return batch

class Celegans19(InMemoryDataset):
    r"""
    Args:
        root (string): Root directory where the dataset should be saved.
        name (string): The name of the dataset (:obj:`"Male"`,
            :obj:`"Hermaphrodite"`).
        transform (callable, optional): A function/transform that takes in an
            :obj:`torch_geometric.data.Data` object and returns a transformed
            version. The data object will be transformed before every access.
            (default: :obj:`None`)
        pre_transform (callable, optional): A function/transform that takes in
            an :obj:`torch_geometric.data.Data` object and returns a
            transformed version. The data object will be transformed before
            being saved to disk. (default: :obj:`None`)
    """

    url = 'null'

    def __init__(self, root: str,name='male',split='node', transform: Optional[Callable] = None,
                 pre_transform: Optional[Callable] = None,process=False):
        self.name=name
        if name=='male':
            self.data_prefix='MaleWorm'
        elif name=='herm':
            self.data_prefix='HermaphroditeWorm'

        super().__init__(root, transform, pre_transform)
        if process:
            self._process()
        self.data, self.slices = torch.load(self.processed_paths[0])
        self.data, self.slices = self.collate([self.data])

    @property
    def raw_dir(self) -> str:
        return osp.join(self.root, 'raw')

    @property
    def processed_dir(self) -> str:
        return osp.join(self.root, 'processed')

    @property
    def raw_file_names(self) -> List[str]:
        return ['HermaphroditeWorm-cell-type.txt','HermaphroditeWorm-edge_list.txt','MaleWorm-cell-type.txt','MaleWorm-edge_list.txt']

    @property
    def processed_file_names(self) -> str:
        return '%s-data.pt'%self.name
    @property
    def neu2ID(self):
        if hasattr(self,'neu2ID_dict'):
            return self.neu2ID_dict
        else:
            Neuron2Type={}
            with open(osp.join(self.raw_dir,'%s-cell-type.txt'%(self.data_prefix)),'r') as fin:
                for i in fin.readlines():
                    line=i.strip().split('\t')
                    if len(line)==2:
                        Neuron2Type[line[0]]=line[1]
            self.neuron2label_dict=Neuron2Type
            Neuron2ID={k:v for v,k in enumerate(Neuron2Type.keys())}
            self.neu2ID_dict=Neuron2ID
            type_set=set(Neuron2Type.values())
            Type2id={k:v for v,k in enumerate(type_set)}
            self.label2ID_dict=Type2id
        return self.neu2ID_dict
    @property
    def label2ID(self):
        if hasattr(self,'label2ID_dict'):
            return self.neu2ID_dict
        else:
            Neuron2Type={}
            with open(osp.join(self.raw_dir,'%s-cell-type.txt'%(self.data_prefix)),'r') as fin:
                for i in fin.readlines():
                    line=i.strip().split('\t')
                    if len(line)==2:
                        Neuron2Type[line[0]]=line[1]
            self.neuron2label_dict=Neuron2Type
            Neuron2ID={k:v for v,k in enumerate(Neuron2Type.keys())}
            self.neu2ID_dict=Neuron2ID
            type_set=set(Neuron2Type.values())
            Type2id={k:v for v,k in enumerate(type_set)}
            self.label2ID_dict=Type2id
        return self.label2ID_dict
    @property
    def typedim(self):
        if hasattr(self,'cache_type_dim'):
            return self.cache_type_dim
        else:
            label2ID=self.label2ID
            self.cache_type_dim=len(label2ID.keys())
            return self.cache_type_dim
    @property
    def neuron2label(self):
        if hasattr(self,'neuron2label_dict'):
            return self.neu2ID_dict
        else:
            Neuron2Type={}
            with open(osp.join(self.raw_dir,'%s-cell-type.txt'%(self.data_prefix)),'r') as fin:
                for i in fin.readlines():
                    line=i.strip().split('\t')
                    if len(line)==2:
                        Neuron2Type[line[0]]=line[1]
            self.neuron2label_dict=Neuron2Type
            Neuron2ID={k:v for v,k in enumerate(Neuron2Type.keys())}
            self.neu2ID_dict=Neuron2ID
            type_set=set(Neuron2Type.values())
            Type2id={k:v for v,k in enumerate(type_set)}
            self.label2ID_dict=Type2id
        return self.neuron2label_dict
    
    @staticmethod
    def read_data(raw_dir,data_prefix):
        Neuron2Type={}
        with open(osp.join(raw_dir,'%s-cell-type.txt'%(data_prefix)),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split('\t')
                if len(line)==2:
                    Neuron2Type[line[0]]=line[1]
        Neuron2ID={k:v for v,k in enumerate(Neuron2Type.keys())}
        type_set=set(Neuron2Type.values())
        Type2id={k:v for v,k in enumerate(type_set)}

        edge_index_list=[]
        edge_weight=[]
        edge_attr=[]
        with open(osp.join(raw_dir,'%s-edge_list.txt'%(data_prefix)),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split('\t')
                if len(line)==4:
                    pre,post=Neuron2ID[line[0]],Neuron2ID[line[1]]
                    edge_index_list.append([pre,post])
                    edge_weight.append(float(line[2]))
                    edge_attr.append(1 if line[3]=='chem' else 0)
        

        edge_index=torch.tensor(edge_index_list)
        edge_weight=torch.tensor(edge_weight)
        edge_weight=edge_weight.to(torch.float32)
        edge_attr=torch.tensor(edge_attr)
        y=[Type2id[v] for _,v in Neuron2Type.items()]
        
        y=torch.tensor(y)

        x=torch.nn.functional.one_hot(y)
        x=x.to(dtype=torch.float32)
        edge_index=edge_index.T

        return Data(x=x,edge_index=edge_index,y=y,edge_attr=edge_attr,edge_weight=edge_weight)

    def process(self):
        data = self.read_data(self.raw_dir,self.data_prefix)
        data = data if self.pre_transform is None else self.pre_transform(data)
        torch.save(self.collate([data]), self.processed_paths[0])
    def manual_split(self,path):
        label2ID={}
        with open(osp.join(path,'label2ID.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    label2ID[line[0]]=int(line[1])
        neu2ID={}
        with open(osp.join(path,'neu2ID.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    neu2ID[line[0]]=int(line[1])
        
        for k,v in self.neu2ID.items():
            if neu2ID[k]!=v:
                raise ValueError('this file doesn`t match this object(%s)'%__name__)

        test_edge_index=[]
        with open(osp.join(path,'test_edge_list.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    n1,n2=int(line[0]),int(line[1])
                    test_edge_index.append([n1,n2])
        test_edge_index=torch.tensor(test_edge_index).T
        test_edge_index=test_edge_index.to(device=self.data.x.device)
        test_edge_label_index=torch.ones(test_edge_index.size(1),device=self.data.x.device)

        train_edge_index=[]
        with open(osp.join(path,'train_edge_list.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    n1,n2=int(line[0]),int(line[1])
                    train_edge_index.append([n1,n2])
        train_edge_index=torch.tensor(train_edge_index).T
        train_edge_index=train_edge_index.to(device=self.data.x.device)
        train_edge_label_index=torch.ones(train_edge_index.size(1),device=self.data.x.device)

        test_data=Data(x=self.data.x,y=self.data.y,edge_index=test_edge_index,edge_label_index=test_edge_label_index,neu2ID=neu2ID,label2ID=label2ID)
        train_data=Data(x=self.data.x,y=self.data.y,edge_index=train_edge_index,edge_label_index=train_edge_label_index,neu2ID=neu2ID,label2ID=label2ID)
        return train_data,test_data

    def __repr__(self) -> str:
        return 'Celegans19-%s'%self.name
class Celegans19_herm(Celegans19):
    def __init__(self,*args,**kwargs):
        kwargs['mode']='herm'
        super(self,Celegans19_herm).__init__(*args,**kwargs)

class NxGraph(InMemoryDataset):
    url=None
    def __init__(self, root: Optional[str] = None, nxg='barbell',transform: Optional[Callable] = None, pre_transform: Optional[Callable] = None, pre_filter: Optional[Callable] = None,**kwargs):
        
        
        self.kwargs=kwargs
        if isinstance(nxg,str):

            self.name=nxg
            self.nxg=self.create_graph(self.name,**self.kwargs)

        elif isinstance(nxg,nx.Graph):
            self.nxg=nxg
            self.name=str(nxg)
        super().__init__(root, transform, pre_transform)
        self.data=torch_geometric.utils.from_networkx(self.nxg)
        self.data = self.data if self.pre_transform is None else self.pre_transform(self.data)
        self.data, self.slices = self.collate([self.data])
    @staticmethod
    def create_graph(opt,*args,**kwargs):

        if opt=='barbell':

            if ('m1' in kwargs) and ('m2' in kwargs):
                m1,m2=kwargs.pop('m1'),kwargs.pop('m2')
                nxg=nx.barbell_graph(m1,m2,**kwargs)
            raise ValueError('Barbell graph options error:%s'%str(kwargs))
        
        return nxg
    