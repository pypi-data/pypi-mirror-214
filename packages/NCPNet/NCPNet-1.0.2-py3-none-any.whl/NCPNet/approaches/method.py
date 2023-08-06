
import torch
#from torch_geometric.nn import GCNConv
#from torch.nn import Sequential, Linear, BatchNorm1d, ReLU,LayerNorm
from .Encoder import GCN,GCN2,MLP,node_attr_encoder
from .Decoder import LinkPred
from .PairEncoder import NeighEnco,NeighEnco2
class Net(torch.nn.Module):
    def __init__(self,config):
        super(Net,self).__init__()
        self.train_config=config
        node_encoder=self.train_config['node_encoder']
        if 'pair_encoder' in self.train_config:
            pair_encoder=self.train_config['pair_encoder']
            self.use_pair_enco=True
            if'gamma' in self.train_config:
                self.gamma=self.train_config['gamma']
            else:
                self.gamma=0.5
        else:
            self.use_pair_enco=False

        decoder=self.train_config['Model']
        namespace=globals()
        if decoder in namespace and node_encoder in namespace:
            Deco_cls,node_Enco_cls=namespace[decoder],namespace[node_encoder]
            self.Deco,self.node_Enco=Deco_cls(config),node_Enco_cls(config)
        else:
            raise ModuleNotFoundError('%s or %s not found'%(decoder,node_encoder))
        if self.use_pair_enco:
            if pair_encoder in namespace:
                pair_encoder_cls=namespace[pair_encoder]
                self.pair_Enco=pair_encoder_cls(config)
                self.ga=torch.nn.parameter.Parameter(data=torch.tensor([self.gamma]),requires_grad=False)
            else:
                raise ModuleNotFoundError('%s not found'%(pair_encoder))
    def forward(self,*args,**kwargs):

        z=self.node_Enco(x=kwargs['x'],edge_index=kwargs['edge_index'])
        #x1=self.Deco(z,edge_label_index=kwargs['edge_label_index'])
        if self.use_pair_enco:

            out=self.Deco(z,edge_label_index=kwargs['edge_label_index'],neighbor=kwargs['neighbor'])
        else:
            out=self.Deco(z,edge_label_index=kwargs['edge_label_index'])
        return out
    @torch.no_grad()
    def NodeCla_inference(self,x_all, subgraph_loader):
        xs = []
        for batch in subgraph_loader:
            batch.to(device=self.train_config['device'])
            x = x_all[batch.n_id.to(x_all.device)]
            x=self.node_Enco.node_attr_layer(x)
            x = self.node_Enco.conv1(x, batch.edge_index)
            x=self.node_Enco.relu1(x)
            xs.append(x[:batch.batch_size].cpu())
        x_all = torch.cat(xs, dim=0).to(device=self.train_config['device'])
        xs = []
        for batch in subgraph_loader:
            batch.to(device=self.train_config['device'])
            x = x_all[batch.n_id.to(x_all.device)]
            x = self.node_Enco.conv2(x, batch.edge_index)
            xs.append(x[:batch.batch_size].cpu())
        x_all = torch.cat(xs, dim=0).to(device=self.train_config['device'])
        return x_all




