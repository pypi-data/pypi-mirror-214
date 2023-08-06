import numpy as np
import torch
import os
import time
from sklearn.metrics import accuracy_score,roc_auc_score,recall_score,f1_score,auc,precision_recall_curve,roc_curve,precision_score
from tensorboardX import SummaryWriter
from torch_geometric.data.dataset import Dataset
import yaml
from zmq import device
from .utils import dict_sequential
import matplotlib.pyplot as plt
from torch_geometric.data import Data
import tqdm
class Base_Trainer:
    def __init__(self,config,model,logdir=None):
        self.trainer_config= config
        self.model=model

        self.loss_function=self.get_loss_function(self.trainer_config['loss'])
        self.iter=0
        self.eval_indicator=[]
        self.parameters=[p for p in self.model.parameters() if p.requires_grad]
        self.optimizer=self.get_optimizer(self.trainer_config['optimizer'],self.parameters,self.trainer_config['lr'],self.trainer_config['weight_decay'])
        self.result_process=[]
        self.logdir=self.get_log_dir(logdir)
        self.best_result=None
        self.train_graph=None
        self.current_result=None

        self.writer=SummaryWriter(logdir=self.logdir) if self.trainer_config['use_tensor_board'] else None
    def get_log_dir(self,logdir=None):
        if logdir is None:
            import socket
            from datetime import datetime
            current_time = datetime.now().strftime('%b%d_%H-%M-%S')
            logdir = os.path.join(
                'runs', self.trainer_config['task_save'],current_time + '_' + socket.gethostname())
        return logdir
    def reset(self):
        self.model.reset()
        self.iter=0
        self.optimizer = self.get_optimizer(self.trainer_config['optimizer'], self.parameters, self.trainer_config['lr'],
                                            self.trainer_config['weight_decay'])
    def update(self,*args,**kwargs):
        '''template method'''
        raise NotImplemented('update is not implemented')
    def get_loss_function(self,loss_name,**kwargs):
        if loss_name=='bcelogits':
            loss=torch.nn.BCEWithLogitsLoss(**kwargs)
        elif loss_name=='bce':
            loss=torch.nn.BCELoss(**kwargs)
        elif loss_name=='nll':
            loss=torch.nn.NLLLoss(**kwargs)
        elif loss_name=='cro_en':
            loss=torch.nn.CrossEntropyLoss(**kwargs)
        elif loss_name=='mse':
            loss=torch.nn.MSELoss(**kwargs)
        else:
            raise NotImplemented('%s is not implemented'%loss_name)
        return loss
    @staticmethod
    def get_optimizer(name, parameters, lr, weight_decay=0):
        if name == 'sgd':
            return torch.optim.SGD(parameters, lr=lr, weight_decay=weight_decay)
        elif name == 'rmsprop':
            return torch.optim.RMSprop(parameters, lr=lr, weight_decay=weight_decay)
        elif name == 'adagrad':
            return torch.optim.Adagrad(parameters, lr=lr, weight_decay=weight_decay)
        elif name == 'adam':
            return torch.optim.Adam(parameters, lr=lr, weight_decay=weight_decay)
        elif name == 'adamax':
            return torch.optim.Adamax(parameters, lr=lr, weight_decay=weight_decay)
        else:
            raise Exception("Unsupported optimizer: {}".format(name))
    def excecute_epoch(self,train_loader,test_loader,**kargs):
        for ep in range(self.trainer_config['epoch']):
            t0=time.time()
            train_result={'Training_Loss':0,'ep':ep}
            for k,batch in enumerate(train_loader):

                loss_result=self.update(batch)
                if self.writer:
                    self.writer.add_scalar('Training Loss',loss_result,global_step=self.iter)
                train_result['Training_Loss']+=loss_result
                self.iter +=1
            train_result['Training_Loss']=train_result['Training_Loss']/len(train_loader)
            train_result['time_cost']=time.time()-t0
            self.logging(train_result,'train')

            if ep%self.trainer_config['eval_step']==0 and ep>0:
                result=self.evaluate(test_loader)
                result.update({'Iter':self.iter,'ep':ep})
                self.logging(result,'test')
                self.eval_indicator.append({'acc':result['Accuracy'],'eval_loss':result['Loss'],'epoch':ep+1})
                self.update_best_res(result)
                self.current_result=result
                self.result_analysis()
                if 'fulldata' in kargs:
                    self.predictions_ana(test_loader,kargs['fulldata'])
        with open(os.path.join(self.logdir,'final_result.yaml'),'w') as fin:
            self.current_result.pop('ROC')
            self.current_result.pop('PR-curve')
            yaml.dump(dict_sequential(self.current_result),fin)
        torch.save(self.model,os.path.join(self.logdir,'checkpoint_final_model.pt'))

    def update_best_res(self,result,mode='Accuracy'):
        if self.best_result is None:
            self.best_result=result
        else:
            if result[mode]>self.best_result[mode]:
                self.best_result=result
                torch.save(self.model,os.path.join(self.logdir,'checkpoint_best_model.pt'))
    @torch.no_grad()
    def eval_result(self, batch):
        '''template method'''
        raise NotImplemented
    def evaluate(self,data_loader):
        '''template method'''
        raise NotImplemented('')

    def auto_early_stop(self):
        if len(self.eval_indicator)>=5:
            acc_list=[self.eval_indicator[-1]['acc'] for i in range(len(self.eval_indicator))]
            stride=3
            smooth_acc=[]
            for i in range(len(self.eval_indicator)-stride+1):
                smooth_acc.append(sum(acc_list[i:i+stride])/stride)
            if smooth_acc[-1]<smooth_acc[-2] and smooth_acc[-2]<smooth_acc[-3]:
                return True
        return False
    def result_analysis(self):
        '''template method'''
        raise NotImplemented
    def logging(self):
        '''template method'''
        raise NotImplemented
#class linkStrenPre(Base_Trainer):
    def update(self,batch):
        self.model.train()
        self.optimizer.zero_grad()
        if len(batch)==6:
            x, edge_index, edge_attr, edge_label_index, edge_label,neighbor=batch
            out=self.model(x=x,edge_index=edge_index,edge_label_index=edge_label_index,neighbor=neighbor)
        elif len(batch)==5:
            x,edge_index, edge_attr, edge_label_index, edge_label=batch
            out=self.model(x=x,edge_index=edge_index,edge_label_index=edge_label_index)
        loss = self.loss_function(out, edge_attr)
        loss.backward()
        self.optimizer.step()
        return loss.detach().item()

    @torch.no_grad()
    def eval_result(self,batch):
        self.model.eval()
        if len(batch)==6:
            x, edge_index, edge_attr, edge_label_index, edge_label,neighbor=batch
            out=self.model(x=x,edge_index=edge_index,edge_label_index=edge_label_index,neighbor=neighbor)
        elif len(batch)==5:
            x,edge_index, edge_attr, edge_label_index, edge_label=batch
            out=self.model(x=x,edge_index=edge_index,edge_label_index=edge_label_index)
        return out,edge_label
    def evaluate(self,data_loader):
        total_loss=0
        y_pred_list,y_list=[],[]
        for batch in data_loader:
            y_pred,y=self.eval_result(batch)
            
            loss=self.loss_function(y_pred,y)
            true_y,outcpu=y.cpu().numpy(),y_pred.cpu().numpy()
            y_pred_list.append(outcpu)
            y_list.append(true_y)
            total_loss+=loss.detach().item()
        total_loss=total_loss/len(y_pred_list)
        total_y_pred=np.concatenate(y_pred_list,axis=0)
        total_y=np.concatenate(y_list,axis=0)

        auc=roc_auc_score(total_y,total_y_pred)
        fpr,tpr,threshold = roc_curve(total_y, total_y_pred)
        yoden_index=np.argmax(tpr-fpr)
        tau=threshold[yoden_index]
        predictions=total_y_pred>tau
        predictions=predictions.astype(dtype=np.int32)

        acc=accuracy_score(total_y,predictions)
        f1=f1_score(total_y,predictions)
        pre=precision_score(total_y,predictions)
        rec=recall_score(total_y,predictions)
        ROC_curve=roc_curve(total_y,total_y_pred)
        PR_curve=precision_recall_curve(total_y,total_y_pred)
        result={'Loss':total_loss,'Accuracy':acc,'Precision':pre,'Recall':rec,'F1':f1,'AUC':auc,'ROC':ROC_curve,'PR-curve':PR_curve,'tau':tau}
        return result
    def logging(self,result,mode='train'):
        if mode=='train':
            print('|::Training::|Epoch:%d|Iter:%d |Training loss:%.4f|epoch_time_cost:%.1f s|'%(result['ep'],self.iter,result['Training_Loss'],result['time_cost']))
        elif mode=='test':
            if self.writer:
                self.writer.add_scalar('Testing Loss',result['Loss'],global_step=self.iter)
                self.writer.add_scalar('Accuracy',result['Accuracy'],global_step=self.iter)
                self.writer.add_scalar('AUC',result['AUC'],global_step=self.iter)
            print('|::Testing::|Epoch:%d|Iter:%d|Loss:%.4f|Accuracy:%.3f|AUC:%.3f|'%(result['ep'],self.iter,result['Loss'],result['Accuracy'],result['AUC']))
    def result_analysis(self,mode='Accuracy'):
        if hasattr(self,'best_result') and self.best_result is not None:
            record_result=self.best_result.copy()
            fpr,tpr,threshold=record_result.pop('ROC')

            roc_array=np.stack((fpr,tpr,threshold),axis=0)
            preci,recc,_=record_result.pop('PR-curve')
            pr_array = np.stack((preci,recc), axis=0)
            record_result=dict_sequential(record_result)
            np.save(os.path.join(self.logdir,'ROC.npz'),roc_array)
            np.save(os.path.join(self.logdir,'PR_curve.npz'),pr_array)

            with open(os.path.join(self.logdir,'best_result.yaml'),'w') as fin:
                yaml.dump(record_result,fin)
            with open(os.path.join(self.logdir,'config.yaml'),'w') as fin:
                yaml.dump(self.trainer_config,fin)
            fig,ax=plt.subplots(ncols=1,nrows=1,figsize=(5,5))
            ax.plot(fpr, tpr, label='ROC curve (auc= %0.3f)' % record_result['AUC'])
            ax.legend(loc="lower right")
            fig.savefig(os.path.join(self.logdir,'ROC_curve.png'))
    
    @torch.no_grad()
    def predictions_ana(self,data_loader,dataset):
        total_loss=0
        y_pred_list,y_list=[],[]
        test_edge,test_edge_label=[],[]
        for batch in data_loader:
            _, _, _, edge_label_index, edge_label = batch
            y_pred,y=self.eval_result(batch)
            loss=self.loss_function(y_pred,y)
            test_edge.append(edge_label_index.cpu())
            test_edge_label.append(edge_label.cpu())
            true_y,outcpu=y.cpu().numpy(),y_pred.cpu().numpy()
            y_pred_list.append(outcpu)
            y_list.append(true_y)
            total_loss+=loss.detach().item()
        test_edge=torch.cat(test_edge,dim=1)
        test_edge=test_edge.T.numpy()
        test_edge_label=torch.cat(test_edge_label,dim=0)
        test_edge_label= test_edge_label.numpy()

        total_loss=total_loss/len(y_pred_list)
        total_y_pred=np.concatenate(y_pred_list,axis=0)
        total_y=np.concatenate(y_list,axis=0)

        auc=roc_auc_score(total_y,total_y_pred)
        fpr,tpr,threshold = roc_curve(total_y, total_y_pred)
        yoden_index=np.argmax(tpr-fpr)
        tau=threshold[yoden_index]
        predictions=total_y_pred>tau
        predictions=predictions.astype(dtype=np.int32)

        acc=accuracy_score(total_y,predictions)
        f1=f1_score(total_y,predictions)
        pre=precision_score(total_y,predictions)
        rec=recall_score(total_y,predictions)
        ROC_curve=roc_curve(total_y,total_y_pred)
        PR_curve=precision_recall_curve(total_y,total_y_pred)
        result={'Loss':total_loss,'Accuracy':acc,'Precision':pre,'Recall':rec,'F1':f1,'AUC':auc,'ROC':ROC_curve,'PR-curve':PR_curve,'tau':tau}

        mistakes_index=np.where(total_y!=predictions)
        mistakes_edge=test_edge[mistakes_index]
        mistakes_label=test_edge_label[mistakes_index]
        mistakes_logits=total_y_pred[mistakes_index]
        ID2neu={v:k for k,v in dataset.neu2ID.items()}
  

        txt_edges=[]
        for k,e in enumerate(mistakes_edge):
            e1,e2=tuple(e)
            txt_edges.append([ID2neu[e1],ID2neu[e2],mistakes_label[k],mistakes_logits[k]])
        
        wrt_str='\n'.join(['%s\t%s\t%d\t%f'%(i[0],i[1],i[2],i[3]) for i in txt_edges])

        with open(os.path.join(self.logdir,'mistakes_predictions_iter%d.txt'%(self.iter)),'w') as fin:
            fin.write(wrt_str)
        

        print('Test num:%d,error prediction:%d,FP/(FP+FN):%.2f'%(len(predictions),len(mistakes_edge),sum(mistakes_label)/len(mistakes_edge)))

    @torch.no_grad()
    def eval_reconstruct(self,full_data,train_data):
        num_node=full_data.num_nodes
        full_data=full_data.to(device='cpu')
        g=torch.ones(size=(num_node,num_node))-torch.eye(num_node)
        g=g.to_sparse().indices()

        index_loader=torch.split(g,500000,dim=1)

        model=torch.load(os.path.join(self.logdir,'checkpoint_best_model.pt'))

        model.to(device='cpu')
        model.eval()
        x,edge_index=train_data.x,train_data.edge_index
        x,edge_index=x.to(device='cpu') if x is not None else None,edge_index.to(device='cpu')
        z = model.node_Enco(x, edge_index)
        res=[]

        for batch in index_loader:
            out=model.Deco(z,batch)
            res.append(out)
        pred_graph_logits=torch.cat(res,dim=0)

        pred_graph=pred_graph_logits>self.best_result['tau']
        pred_graph=pred_graph.to(dtype=torch.int64)
        print(pred_graph.sum())
        half_g=torch.stack([full_data.edge_index[1],full_data.edge_index[0]],dim=0)
        full_g=torch.cat([full_data.edge_index,half_g],dim=1)
        pred_graph=torch.sparse_coo_tensor(g,pred_graph,size=(num_node,num_node)).to_dense()
        ground_truth=torch.sparse_coo_tensor(full_g,torch.ones(full_g.size(1)),size=(num_node,num_node)).to_dense()

        reconstruct_error=torch.abs(pred_graph-ground_truth).sum()
        print(reconstruct_error)


class LinkPred_trainer(Base_Trainer):

    def update(self,batch):
        torch.save(self.model,'/data/users/wgj/project/NDGNN_Neurips22_Realeased/runs/tsne_savemodel-%d.pt'%self.iter)
        self.model.train()
        self.optimizer.zero_grad()
        if len(batch)==6:
            x, edge_index, edge_attr, edge_label_index, edge_label,neighbor=batch
            out=self.model(x=x,edge_index=edge_index,edge_label_index=edge_label_index,neighbor=neighbor)
        elif len(batch)==5:
            x,edge_index, edge_attr, edge_label_index, edge_label=batch
            out=self.model(x=x,edge_index=edge_index,edge_label_index=edge_label_index)
        loss = self.loss_function(out, edge_label)
        loss.backward()
        self.optimizer.step()
        return loss.detach().item()

    @torch.no_grad()
    def eval_result(self,batch):
        self.model.eval()
        if len(batch)==6:
            x, edge_index, edge_attr, edge_label_index, edge_label,neighbor=batch
            out=self.model(x=x,edge_index=edge_index,edge_label_index=edge_label_index,neighbor=neighbor)
        elif len(batch)==5:
            x,edge_index, edge_attr, edge_label_index, edge_label=batch
            out=self.model(x=x,edge_index=edge_index,edge_label_index=edge_label_index)
        return out,edge_label
    def evaluate(self,data_loader):
        total_loss=0
        y_pred_list,y_list=[],[]
        for batch in data_loader:
            y_pred,y=self.eval_result(batch)
            
            loss=self.loss_function(y_pred,y)
            true_y,outcpu=y.cpu().numpy(),y_pred.cpu().numpy()
            y_pred_list.append(outcpu)
            y_list.append(true_y)
            total_loss+=loss.detach().item()
        total_loss=total_loss/len(y_pred_list)
        total_y_pred=np.concatenate(y_pred_list,axis=0)
        total_y=np.concatenate(y_list,axis=0)

        auc=roc_auc_score(total_y,total_y_pred)
        fpr,tpr,threshold = roc_curve(total_y, total_y_pred)
        yoden_index=np.argmax(tpr-fpr)
        tau=threshold[yoden_index]
        predictions=total_y_pred>tau
        predictions=predictions.astype(dtype=np.int32)

        acc=accuracy_score(total_y,predictions)
        f1=f1_score(total_y,predictions)
        pre=precision_score(total_y,predictions)
        rec=recall_score(total_y,predictions)
        ROC_curve=roc_curve(total_y,total_y_pred)
        PR_curve=precision_recall_curve(total_y,total_y_pred)
        result={'Loss':total_loss,'Accuracy':acc,'Precision':pre,'Recall':rec,'F1':f1,'AUC':auc,'ROC':ROC_curve,'PR-curve':PR_curve,'tau':tau}
        return result
    def logging(self,result,mode='train'):
        if mode=='train':
            print('|::Training::|Epoch:%d|Iter:%d |Training loss:%.4f|epoch_time_cost:%.1f s|'%(result['ep'],self.iter,result['Training_Loss'],result['time_cost']))
        elif mode=='test':
            if self.writer:
                self.writer.add_scalar('Testing Loss',result['Loss'],global_step=self.iter)
                self.writer.add_scalar('Accuracy',result['Accuracy'],global_step=self.iter)
                self.writer.add_scalar('AUC',result['AUC'],global_step=self.iter)
            print('|::Testing::|Epoch:%d|Iter:%d|Loss:%.4f|Accuracy:%.3f|AUC:%.3f|'%(result['ep'],self.iter,result['Loss'],result['Accuracy'],result['AUC']))
    def result_analysis(self,mode='Accuracy'):
        if hasattr(self,'best_result') and self.best_result is not None:
            record_result=self.best_result.copy()
            fpr,tpr,threshold=record_result.pop('ROC')

            roc_array=np.stack((fpr,tpr,threshold),axis=0)
            preci,recc,_=record_result.pop('PR-curve')
            pr_array = np.stack((preci,recc), axis=0)
            record_result=dict_sequential(record_result)
            np.save(os.path.join(self.logdir,'ROC.npz'),roc_array)
            np.save(os.path.join(self.logdir,'PR_curve.npz'),pr_array)

            with open(os.path.join(self.logdir,'best_result.yaml'),'w') as fin:
                yaml.dump(record_result,fin)
            with open(os.path.join(self.logdir,'config.yaml'),'w') as fin:
                yaml.dump(self.trainer_config,fin)
            fig,ax=plt.subplots(ncols=1,nrows=1,figsize=(5,5))
            ax.plot(fpr, tpr, label='ROC curve (auc= %0.3f)' % record_result['AUC'])
            ax.legend(loc="lower right")
            fig.savefig(os.path.join(self.logdir,'ROC_curve.png'))
    
    @torch.no_grad()
    def predictions_ana(self,data_loader,dataset):
        total_loss=0
        y_pred_list,y_list=[],[]
        test_edge,test_edge_label=[],[]
        for batch in data_loader:
            _, _, _, edge_label_index, edge_label = batch
            y_pred,y=self.eval_result(batch)
            loss=self.loss_function(y_pred,y)
            test_edge.append(edge_label_index.cpu())
            test_edge_label.append(edge_label.cpu())
            true_y,outcpu=y.cpu().numpy(),y_pred.cpu().numpy()
            y_pred_list.append(outcpu)
            y_list.append(true_y)
            total_loss+=loss.detach().item()
        test_edge=torch.cat(test_edge,dim=1)
        test_edge=test_edge.T.numpy()
        test_edge_label=torch.cat(test_edge_label,dim=0)
        test_edge_label= test_edge_label.numpy()

        total_loss=total_loss/len(y_pred_list)
        total_y_pred=np.concatenate(y_pred_list,axis=0)
        total_y=np.concatenate(y_list,axis=0)

        auc=roc_auc_score(total_y,total_y_pred)
        fpr,tpr,threshold = roc_curve(total_y, total_y_pred)
        yoden_index=np.argmax(tpr-fpr)
        tau=threshold[yoden_index]
        predictions=total_y_pred>tau
        predictions=predictions.astype(dtype=np.int32)

        acc=accuracy_score(total_y,predictions)
        f1=f1_score(total_y,predictions)
        pre=precision_score(total_y,predictions)
        rec=recall_score(total_y,predictions)
        ROC_curve=roc_curve(total_y,total_y_pred)
        PR_curve=precision_recall_curve(total_y,total_y_pred)
        result={'Loss':total_loss,'Accuracy':acc,'Precision':pre,'Recall':rec,'F1':f1,'AUC':auc,'ROC':ROC_curve,'PR-curve':PR_curve,'tau':tau}

        mistakes_index=np.where(total_y!=predictions)
        mistakes_edge=test_edge[mistakes_index]
        mistakes_label=test_edge_label[mistakes_index]
        mistakes_logits=total_y_pred[mistakes_index]
        ID2neu={v:k for k,v in dataset.neu2ID.items()}
  

        txt_edges=[]
        for k,e in enumerate(mistakes_edge):
            e1,e2=tuple(e)
            txt_edges.append([ID2neu[e1],ID2neu[e2],mistakes_label[k],mistakes_logits[k]])
        
        wrt_str='\n'.join(['%s\t%s\t%d\t%f'%(i[0],i[1],i[2],i[3]) for i in txt_edges])

        with open(os.path.join(self.logdir,'mistakes_predictions_iter%d.txt'%(self.iter)),'w') as fin:
            fin.write(wrt_str)
        

        print('Test num:%d,error prediction:%d,FP/(FP+FN):%.2f'%(len(predictions),len(mistakes_edge),sum(mistakes_label)/len(mistakes_edge)))

    @torch.no_grad()
    def eval_reconstruct(self,full_data,train_data):
        num_node=full_data.num_nodes
        full_data=full_data.to(device='cpu')
        g=torch.ones(size=(num_node,num_node))-torch.eye(num_node)
        g=g.to_sparse().indices()

        index_loader=torch.split(g,500000,dim=1)

        model=torch.load(os.path.join(self.logdir,'checkpoint_best_model.pt'))

        model.to(device='cpu')
        model.eval()
        x,edge_index=train_data.x,train_data.edge_index
        x,edge_index=x.to(device='cpu') if x is not None else None,edge_index.to(device='cpu')
        z = model.node_Enco(x, edge_index)
        res=[]

        for batch in index_loader:
            out=model.Deco(z,batch)
            res.append(out)
        pred_graph_logits=torch.cat(res,dim=0)

        pred_graph=pred_graph_logits>self.best_result['tau']
        pred_graph=pred_graph.to(dtype=torch.int64)
        print(pred_graph.sum())
        half_g=torch.stack([full_data.edge_index[1],full_data.edge_index[0]],dim=0)
        full_g=torch.cat([full_data.edge_index,half_g],dim=1)
        pred_graph=torch.sparse_coo_tensor(g,pred_graph,size=(num_node,num_node)).to_dense()
        ground_truth=torch.sparse_coo_tensor(full_g,torch.ones(full_g.size(1)),size=(num_node,num_node)).to_dense()

        reconstruct_error=torch.abs(pred_graph-ground_truth).sum()
        print(reconstruct_error)
