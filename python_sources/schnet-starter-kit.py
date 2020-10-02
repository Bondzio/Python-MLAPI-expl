#!/usr/bin/env python
# coding: utf-8

# # Introduction
# I share a simple example which employ SchNet for predicting coupling constants.
# I hope this kernel helps beginners of DNN and will be used as a starter kit.
# 
# The core idea is same as Heng's, which employ GNN as a feature exstractor.
# Two feature vectors are concatenated and thrown into regression header.
# More details of his idea and discussions can be read in below pages.
# 
# * Which graph CNN is the best (with starter kit at LB -1.469)?<br>https://www.kaggle.com/c/champs-scalar-coupling/discussion/93972#latest-591759
# 
# Due to the limitation of Kaggle kernel, the model in not trained completely in this Kernel.
# You would achieve better score by continuing training procedure longer.

# #  A  big thanks to [toshik](https://www.kaggle.com/toshik)

# # Install packages
# In this example, I use chainer chemistry which offer an implementation of SchNet.
# This library can be install by PIP.
# * Chainer Chemistry: A Library for Deep Learning in Biology and Chemistry<br>https://github.com/pfnet-research/chainer-chemistry

# In[ ]:


get_ipython().system('pip uninstall -y tensorflow')
get_ipython().system('pip install chainer-chemistry==0.5.0')


# # Import packages
# Next, I import main packages. Other sub-modules are imported later.

# In[ ]:


import random
import numpy as np
import pandas as pd
import chainer
import chainer_chemistry
from IPython.display import display


# # Load dataset
# In this example, 90% of training data is used actual training data, and the other 10% is used for validation.
# Each dataset is grouped by molecule_name name for following procedures.

# In[ ]:


def load_dataset():

    train = pd.merge(pd.read_csv('../input/champs-scalar-coupling/train.csv'),
                     pd.read_csv('../input/champs-scalar-coupling/scalar_coupling_contributions.csv'))

    test = pd.read_csv('../input/champs-scalar-coupling/test.csv')

    counts = train['molecule_name'].value_counts()
    moles = list(counts.index)

    random.shuffle(moles)

    num_train = int(len(moles) * 0.9)
    train_moles = sorted(moles[:num_train])
    valid_moles = sorted(moles[num_train:])
    test_moles = sorted(list(set(test['molecule_name'])))

    valid = train.query('molecule_name not in @train_moles')
    train = train.query('molecule_name in @train_moles')

    train.sort_values('molecule_name', inplace=True)
    valid.sort_values('molecule_name', inplace=True)
    test.sort_values('molecule_name', inplace=True)

    return train, valid, test, train_moles, valid_moles, test_moles

train, valid, test, train_moles, valid_moles, test_moles = load_dataset()

train_gp = train.groupby('molecule_name')
valid_gp = valid.groupby('molecule_name')
test_gp = test.groupby('molecule_name')

structures = pd.read_csv('../input/champs-scalar-coupling/structures.csv')
structures_groups = structures.groupby('molecule_name')


# ## train data

# In[ ]:


display(train.head())


# ## validation data

# In[ ]:


display(valid.head())


# ## test data

# In[ ]:


display(test.head())


# ## structures

# In[ ]:


display(structures.head())


# # Preprocessing
# I implemented a class named `Graph` whose instances contain molecules.
# The distances between atoms are calculated in the initializer of this class.
# ## Define Graph class

# In[ ]:


from scipy.spatial import distance


class Graph:

    def __init__(self, points_df, list_atoms):

        self.points = points_df[['x', 'y', 'z']].values

        self._dists = distance.cdist(self.points, self.points)

        self.adj = self._dists < 1.5
        self.num_nodes = len(points_df)

        self.atoms = points_df['atom']
        dict_atoms = {at: i for i, at in enumerate(list_atoms)}

        atom_index = [dict_atoms[atom] for atom in self.atoms]
        one_hot = np.identity(len(dict_atoms))[atom_index]

        bond = np.sum(self.adj, 1) - 1
        bonds = np.identity(len(dict_atoms))[bond - 1]

        self._array = np.concatenate([one_hot, bonds], axis=1).astype(np.float32)

    @property
    def input_array(self):
        return self._array

    @property
    def dists(self):
        return self._dists.astype(np.float32)


# ## Convert into graph object
# Each dataset is represented as a list of Graphs and prediction targets.

# In[ ]:


list_atoms = list(set(structures['atom']))
print('list of atoms')
print(list_atoms)
    
train_graphs = list()
train_targets = list()
print('preprocess training molecules ...')
for mole in train_moles:
    train_graphs.append(Graph(structures_groups.get_group(mole), list_atoms))
    train_targets.append(train_gp.get_group(mole))

valid_graphs = list()
valid_targets = list()
print('preprocess validation molecules ...')
for mole in valid_moles:
    valid_graphs.append(Graph(structures_groups.get_group(mole), list_atoms))
    valid_targets.append(valid_gp.get_group(mole))

test_graphs = list()
test_targets = list()
print('preprocess test molecules ...')
for mole in test_moles:
    test_graphs.append(Graph(structures_groups.get_group(mole), list_atoms))
    test_targets.append(test_gp.get_group(mole))


# ## Convert into chainer's dataset
# This type of dataset can be handled by `DictDataset`.
# Graph objects and prediction targets are merged as a `DictDataset`.

# In[ ]:


from chainer.datasets.dict_dataset import DictDataset

train_dataset = DictDataset(graphs=train_graphs, targets=train_targets)
valid_dataset = DictDataset(graphs=valid_graphs, targets=valid_targets)
test_dataset = DictDataset(graphs=test_graphs, targets=test_targets)


# In[ ]:





# # Model
# ## Build SchNet model
# The prediction model is implemented as follows.
# First, fully connected layer is applied to input arrays to align dimensions.
# Next, SchNet layer is applied for feature extraction.
# Finally, features vectors are concatenated and thrown into three layers MLP.
# I add batch-normalization layers like ResNet.

# In[ ]:


from chainer import reporter
from chainer import functions as F
from chainer import links as L
from chainer_chemistry.links import SchNetUpdate
from chainer_chemistry.links import GraphLinear, GraphBatchNormalization

class SchNetUpdateBN(SchNetUpdate):

    def __init__(self, *args, **kwargs):
        super(SchNetUpdateBN, self).__init__(*args, **kwargs)
        with self.init_scope():
            self.bn = GraphBatchNormalization(args[0])

    def __call__(self, h, adj, **kwargs):
        v = self.linear[0](h)
        v = self.cfconv(v, adj)
        v = self.linear[1](v)
        v = F.softplus(v)
        v = self.linear[2](v)
        return h + self.bn(v)

class SchNet(chainer.Chain):

    def __init__(self, num_layer=3):
        super(SchNet, self).__init__()

        self.num_layer = num_layer

        with self.init_scope():
            self.gn = GraphLinear(512)
            for l in range(self.num_layer):
                self.add_link('sch{}'.format(l), SchNetUpdateBN(512))

            self.interaction1 = L.Linear(128)
            self.interaction2 = L.Linear(128)
            self.interaction3 = L.Linear(4)

    def __call__(self, input_array, dists, pairs_index, targets):

        out = self.predict(input_array, dists, pairs_index)
        loss = F.mean_absolute_error(out, targets)
        reporter.report({'loss': loss}, self)
        return loss

    def predict(self, input_array, dists, pairs_index, **kwargs):

        h = self.gn(input_array)

        for l in range(self.num_layer):
            h = self['sch{}'.format(l)](h, dists)

        h = F.concat((h, input_array), axis=2)

        concat = F.concat([
            h[pairs_index[:, 0], pairs_index[:, 1], :],
            h[pairs_index[:, 0], pairs_index[:, 2], :],
            F.expand_dims(dists[pairs_index[:, 0],
                                pairs_index[:, 1],
                                pairs_index[:, 2]], 1)
        ], axis=1)

        h1 = F.leaky_relu(self.interaction1(concat))
        h2 = F.leaky_relu(self.interaction2(h1))
        out = self.interaction3(h2)

        return out

model = SchNet(num_layer=3)
model.to_gpu(device=0)


# In[ ]:





# # Training preparation
# ## Make samplers
# For mini-batch training, I implement a sampler named `SameSizeSampler`.
# The molecules which have same number of atoms are selected simultaneously.

# In[ ]:


from chainer.iterators import OrderSampler

class SameSizeSampler(OrderSampler):

    def __init__(self, structures_groups, moles, batch_size,
                 random_state=None, use_remainder=False):

        self.structures_groups = structures_groups
        self.moles = moles
        self.batch_size = batch_size
        if random_state is None:
            random_state = np.random.random.__self__
        self._random = random_state
        self.use_remainder = use_remainder

    def __call__(self, current_order, current_position):

        batches = list()

        atom_counts = pd.DataFrame()
        atom_counts['mol_index'] = np.arange(len(self.moles))
        atom_counts['molecular_name'] = self.moles
        atom_counts['num_atom'] = [len(self.structures_groups.get_group(mol))
                                   for mol in self.moles]

        num_atom_counts = atom_counts['num_atom'].value_counts()

        for count, num_mol in num_atom_counts.to_dict().items():
            if self.use_remainder:
                num_batch_for_this = -(-num_mol // self.batch_size)
            else:
                num_batch_for_this = num_mol // self.batch_size

            target_mols = atom_counts.query('num_atom==@count')['mol_index'].values
            random.shuffle(target_mols)

            devider = np.arange(0, len(target_mols), self.batch_size)
            devider = np.append(devider, 99999)

            if self.use_remainder:
                target_mols = np.append(
                    target_mols,
                    np.repeat(target_mols[-1], -len(target_mols) % self.batch_size))

            for b in range(num_batch_for_this):
                batches.append(target_mols[devider[b]:devider[b + 1]])

        random.shuffle(batches)
        batches = np.concatenate(batches).astype(np.int32)

        return batches

batch_size = 8
train_sampler = SameSizeSampler(structures_groups, train_moles, batch_size)
valid_sampler = SameSizeSampler(structures_groups, valid_moles, batch_size,
                                use_remainder=True)
test_sampler = SameSizeSampler(structures_groups, test_moles, batch_size,
                               use_remainder=True)


# ## Make iterators, oprimizer
# Iterators for data feeding is made as below.

# In[ ]:


train_iter = chainer.iterators.SerialIterator(
    train_dataset, batch_size, order_sampler=train_sampler)

valid_iter = chainer.iterators.SerialIterator(
    valid_dataset, batch_size, repeat=False, order_sampler=valid_sampler)

test_iter = chainer.iterators.SerialIterator(
    test_dataset, batch_size, repeat=False, order_sampler=test_sampler)


# ## Make optimizer
# Adam is used as an optimizer.

# In[ ]:


from chainer import optimizers
optimizer = optimizers.Adam(alpha=1e-3)
optimizer.setup(model)


# ## Make updator
# Since the model receives input arrays separately, I implement an original converter.
# `input_array` and `dists` are exstracted from `Graph` object and `pair_index` and `targets` are exstracted from `targets` object.
# `targets` is added only for training.
# When this converter is used for evaluation, `targets` is not added.

# In[ ]:


from chainer import training
from chainer.dataset import to_device

def coupling_converter(batch, device):

    list_array = list()
    list_dists = list()
    list_targets = list()
    list_pairs_index = list()

    with_target = 'fc' in batch[0]['targets'].columns

    for i, d in enumerate(batch):
        list_array.append(d['graphs'].input_array)
        list_dists.append(d['graphs'].dists)
        if with_target:
            list_targets.append(
                d['targets'][['fc', 'sd', 'pso', 'dso']].values.astype(np.float32))

        sample_index = np.full((len(d['targets']), 1), i)
        atom_index = d['targets'][['atom_index_0', 'atom_index_1']].values

        list_pairs_index.append(np.concatenate([sample_index, atom_index], axis=1))

    input_array = to_device(device, np.stack(list_array))
    dists = to_device(device, np.stack(list_dists))
    pairs_index = np.concatenate(list_pairs_index)

    array = {'input_array': input_array, 'dists': dists, 'pairs_index': pairs_index}

    if with_target:
        array['targets'] = to_device(device, np.concatenate(list_targets))

    return array

updater = training.StandardUpdater(train_iter, optimizer,
                                   converter=coupling_converter, device=0)
trainer = training.Trainer(updater, (40, 'epoch'), out="result")


# # Training extensions
# ## Evaluator
# I implemented an Evaluator which measure validation score during training.
# The prediction for test data is also calculated in this evaluator and the submision file is generated.

# In[ ]:


from chainer.training.extensions import Evaluator
from chainer import cuda

class TypeWiseEvaluator(Evaluator):

    def __init__(self, iterator, target, converter, device, name,
                 is_validate=False, is_submit=False):

        super(TypeWiseEvaluator, self).__init__(
            iterator, target, converter=converter, device=device)

        self.is_validate = is_validate
        self.is_submit = is_submit
        self.name = name

    def calc_score(self, df_truth, pred):

        target_types = list(set(df_truth['type']))

        diff = df_truth['scalar_coupling_constant'] - pred

        scores = 0
        metrics = {}

        for target_type in target_types:

            target_pair = df_truth['type'] == target_type
            score_exp = np.mean(np.abs(diff[target_pair]))
            scores += np.log(score_exp)

            metrics[target_type] = scores

        metrics['ALL_LogMAE'] = scores / len(target_types)

        observation = {}
        with reporter.report_scope(observation):
            reporter.report(metrics, self._targets['main'])

        return observation

    def evaluate(self):
        iterator = self._iterators['main']
        eval_func = self._targets['main']

        iterator.reset()
        it = iterator

        y_total = []
        t_total = []

        for batch in it:
            in_arrays = self.converter(batch, self.device)
            with chainer.no_backprop_mode(), chainer.using_config('train', False):
                y = eval_func.predict(**in_arrays)

            y_data = cuda.to_cpu(y.data)
            y_total.append(y_data)
            t_total.extend([d['targets'] for d in batch])

        df_truth = pd.concat(t_total, axis=0)
        y_pred = np.sum(np.concatenate(y_total), axis=1)

        if self.is_submit:
            submit = pd.DataFrame()
            submit['id'] = df_truth['id']
            submit['scalar_coupling_constant'] = y_pred
            submit.drop_duplicates(subset='id', inplace=True)
            submit.sort_values('id', inplace=True)
            submit.to_csv('kernel_schnet.csv', index=False)

        if self.is_validate:
            return self.calc_score(df_truth, y_pred)

        return {}

trainer.extend(
    TypeWiseEvaluator(iterator=valid_iter, target=model, converter=coupling_converter, 
                      name='valid', device=0, is_validate=True))
trainer.extend(
    TypeWiseEvaluator(iterator=test_iter, target=model, converter=coupling_converter,
                      name='test', device=0, is_submit=True))


# ## Other extensions
# ExponentialShift is set as a learning rate scheduler.
# An extension which turn off training mode is also set to deactivate normalizatoin from second epoch.
# 
# Log options are set to report the metrics.
# This helps us to analyze the result of training.

# In[ ]:


trainer.extend(training.extensions.ExponentialShift('alpha', 0.99999))

from chainer.training import make_extension

def stop_train_mode(trigger):
    @make_extension(trigger=trigger)
    def _stop_train_mode(_):
        chainer.config.train = False
    return _stop_train_mode

trainer.extend(stop_train_mode(trigger=(1, 'epoch')))

trainer.extend(
    training.extensions.observe_value(
        'alpha', lambda tr: tr.updater.get_optimizer('main').alpha))

trainer.extend(training.extensions.LogReport())
trainer.extend(training.extensions.PrintReport(
    ['epoch', 'elapsed_time', 'main/loss', 'valid/main/ALL_LogMAE', 'alpha']))


# # Training
# ## Run
# I tuned number of epochs to prevent timeout.
# SchNet tends to be underfitting, longer training makes the model better basically.

# In[ ]:


chainer.config.train = True
trainer.run()


# ## Check output

# In[ ]:


submit = pd.read_csv('kernel_schnet.csv')
display(submit.head())
print('shape: {}'.format(submit.shape))


# # For more improvement
# This example can be improved by below ways.
# * Train more
# * Tune hyperparameters
# * Add original feature
# * Try different GNNs
# * Blend with Gradient Boosting Machines
# 
# You can start with this kernel and don't forget upvote :)
# 
# # References
# 
# * SchNet: A continuous-filter convolutional neural network for modeling quantum interactions<br>https://arxiv.org/abs/1706.08566
# * SchNet - a deep learning architecture for molecules and materials<br>https://arxiv.org/abs/1712.06113
# 
