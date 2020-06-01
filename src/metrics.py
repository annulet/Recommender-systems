"""Metrics"""

import numpy as np


def precision_at_k(recommended_list, bought_list):
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    recommended_list = recommended_list
    flags = np.isin(bought_list, recommended_list)
    precision = flags.sum() / len(recommended_list)
    return precision


def money_precision_at_k(recommended_list, bought_list, prices_recommended):    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    prices_recommended = np.array(prices_recommended)
    
    recommended_list = recommended_list
    prices_recommended = prices_recommended
    flags = np.isin(recommended_list, bought_list)
    precision = (prices_recommended * flags).sum() / prices_recommended.sum()
    return precision


def recall_at_k(recommended_list, bought_list):
    
    bought_list = np.array(bought_list)
    
    recommended_list = np.array(recommended_list)
    
    flags = np.isin(bought_list, recommended_list)
    
    recall = flags.sum() / len(bought_list)
    
    return recall


def money_recall_at_k(recommended_list, bought_list, prices_recommended, prices_bought):
    
    bought_list = np.array(bought_list)
    recommended_list = np.array(recommended_list)
    prices_recommended = np.array(prices_recommended)
    prices_bought = np.array(prices_bought)
 
    recommended_list = recommended_list
    prices_recommended = prices_recommended

    flags = np.isin(recommended_list, bought_list)

    recall = (prices_recommended * flags).sum() / prices_bought.sum()
    
    return recall