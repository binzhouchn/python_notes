# -*- coding: utf-8 -*-
"""
__title__ = 'baseline'
__author__ = 'from yj'
__mtime__ = '2018/8/20'
"""

import lightgbm as lgb


class Model(object):
    def __init__(self, X, y, learning_rate=0.1, metric='auc', application='binary', feval=None, seed=0):
        """params
        :param learning_rate:
        :param metric: https://lightgbm.readthedocs.io/en/latest/Parameters.html#metric-parameters
            binary: 'auc', 'binary_error', 'binary_logloss'
            multiclass: 'multi_error', 'multi_logloss'

        :param application: regression binary multiclass

        :param feval:
            def feval(y_pred, data):
                y_true = data.get_label()
                return '1 / (1 + rmse)', 1 /(rmse(y_true, y_pred) + 1), True

        :param seed:
        :param stratified:
        """
        self.lgb_data = lgb.Dataset(X, y)
        self.metric = metric
        self.application = application
        self.feval = feval
        self.seed = seed
        self.stratified = True

        self.iter_best = None
        self.model = None

        self.params = {
            'application': application,
            'learning_rate': learning_rate,
            'metric': metric,

            'boosting': 'gbdt',  # 'rf', 'dart', 'goss'
            'max_depth': -1,
            'num_leaves': 2 ** 6 - 1,

            'min_split_gain': 0,
            'min_child_weight': 0.01,

            'bagging_fraction': 0.8,
            'feature_fraction': 0.8,
            'lambda_l1': 0,
            'lambda_l2': 0.1,

            'scale_pos_weight': 1,

            'num_threads': 32,
        }

    def cv(self, nfold=5, return_model=False):

        if self.application == 'regression':
            self.stratified = False
        elif self.application in ('multiclass', 'multiclassova'):
            self.num_class = len(set(self.lgb_data.get_label()))
            self.params['num_class'] = self.num_class
        elif self.application == 'binary' and 'scale_pos_weight' in self.params:
            self.params.pop('scale_pos_weight')

        res = lgb.cv(
            self.params,
            self.lgb_data,
            num_boost_round=2000,
            nfold=nfold,
            stratified=self.stratified,
            early_stopping_rounds=50,
            verbose_eval=50,
            show_stdv=True,
            seed=self.seed,
            feval=self.feval
        )

        self.iter_best = len(res['%s-mean' % self.metric])
        if return_model:
            print("\nTrain Model ...")
            self.model = lgb.train(self.params, self.lgb_data, self.iter_best)
