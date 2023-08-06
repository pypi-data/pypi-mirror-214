import random

import yaml
from .utils import load_config
from itertools import product
import os
import numpy as np
import matplotlib.pyplot as plt
import shutil

class Base_Task:
    def __init__(self,configs,search_method='random',overwrite=True):
        self.search_method=search_method
        if isinstance(configs,str):
            self.meta_config=load_config(configs)
        elif isinstance(configs,dict):
            self.meta_config=configs
        if self.meta_config['Train']['task_save'] is False:
            import socket
            from datetime import datetime
            current_time = datetime.now().strftime('%b%d')
            task_save='Task-'+current_time + '_' + socket.gethostname()
            self.meta_config['Train'].update({'task_save':task_save})
        else:
            task_save=self.meta_config['Train']['task_save']
        self.task = []
        self.task_save=task_save
        self.logdir=os.path.join('runs',self.task_save)
        if overwrite and os.path.isdir(self.logdir):
            shutil.rmtree(self.logdir)
        os.mkdir(self.logdir)
        self.parse_config(self.meta_config)
    def parse_config(self,configs):
        leaf_dict=self.find_leaf(configs)
        per_hypermeters=[]
        per_keys=[]
        for k in leaf_dict:
            if isinstance(leaf_dict[k],list):
                per_hypermeters.append(leaf_dict[k])
                per_keys.append(k)
            else:
                per_hypermeters.append([leaf_dict[k]])
                per_keys.append(k)
        hypermeters=product(*per_hypermeters)
        for m in hypermeters:
            single_task={}
            for t,v in enumerate(m):
                single_task[per_keys[t]]=v
            self.task.append(single_task)
    def __iter__(self):
        if hasattr(self,'task'):
            if self.search_method=='random':
                return self.random_search()
            elif self.search_method=='plain':
                return iter(self.task)
            else:
                raise NotImplemented('not implemented %s search method'%self.search_method)
        else:
            raise ModuleNotFoundError('task config is not found...')
    def __len__(self):
        return len(self.task)
    def random_search(self):
        if hasattr(self,'task'):
            tasks_iter=self.task.copy()
            random.shuffle(tasks_iter)
            return iter(tasks_iter)
    def find_leaf(self,conf_dict):
        res= {}
        for k,v in conf_dict.items():
            if isinstance(v,dict):
                if len(v.keys())==1:
                    l=list(v.keys())
                    res.update({k:l[0]})
                res.update(self.find_leaf(conf_dict[k]))
            else:
                #leaf dict
                if k in res:
                    raise KeyError('Config file error..Keys are duplicated in config file..')
                res.update({k:conf_dict[k]})
        return res
    @staticmethod
    def linkpred_task_report(dir):
        files=os.listdir(dir)
        task_folders=[]
        for f in files:
            if os.path.isdir(os.path.join(dir,f)):
                task_folders.append(f)
        results=[]
        configs=[]
        for folder in task_folders:
            with open(os.path.join(dir,folder,'best_result.yaml'),'r') as fin:
                res=yaml.load(fin)
                results.append(res)
            with open(os.path.join(dir,folder,'config.yaml'),'r') as fin:
                config=yaml.load(fin)
                configs.append(config)
        x_config={}
        for config in configs:
            for k,v in config.items():
                if k in x_config:
                    x_config[k].append(v)
                else:
                    x_config[k]=[v]
        pop_list=[]
        for k,v in x_config.items():
            if len(set(v))==1:
                pop_list.append(k)
        for i in pop_list:
            x_config.pop(i)
        
        
        
        y_total=['AUC','F1','Accuracy','Precision','Recall']
        report={i:{} for i in y_total}
        for ylabel in y_total:
            for x_name,v_value in x_config.items():
                x,y=[],[]
                for k,c in enumerate(configs):
                    if c[x_name]==v_value[k]:
                        x.append(c[x_name])
                        y.append(results[k][ylabel])
                w=sorted(zip(x,y),key=lambda x:x[0])
                x,y=np.array([n[0] for n in w]),np.array([n[1] for n in w])
                fig,ax=plt.subplots(ncols=1,nrows=1,figsize=(6,6))
                ax.plot(x,y,label=y_total)
                ax.set_title('%s-%s-plot'%(x_name,ylabel))
                ax.set_xlim([0,1])
                ax.set_ylim([0.4,1])
                report[ylabel][x_name]={'x':x.tolist(),'y':y.tolist()}
                fig.savefig(os.path.join(dir,'%s-%s-plot.png'%(x_name,ylabel)))
        with open(os.path.join(dir,'plot_save.yaml'),'w') as fin:
            yaml.dump(report,fin)





