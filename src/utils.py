"""Функции для предобработки данных"""


def prefilter_items(data_train, item_features, take_n_popular=5000):
    # Уберем самые популярные товары (их и так купят)
    popularity = data_train.groupby('item_id')['user_id'].nunique().reset_index()
    popularity['share_unique_users'] = popularity['user_id'] / data_train['user_id'].nunique()
    
    top_popular = popularity[popularity['share_unique_users'] > 0.5].item_id.tolist()
    data_train = data_train[~data_train['item_id'].isin(top_popular)]
    
    # Уберем самые НЕ популярные товары (их и так НЕ купят)
    top_notpopular = popularity[popularity['share_unique_users'] < 0.01].item_id.tolist()
    data_train = data_train[~data_train['item_id'].isin(top_notpopular)]
    
    # Уберем товары, которые не продавались за последние 12 месяцев
    last_12 = data_train.loc[data_train['week_no'] > (data_train['week_no'].nunique() - 52)]
    current_items = last_12.item_id.unique().tolist()
    data_train = data_train[data_train['item_id'].isin(current_items)]
    
    # Уберем не интересные для рекоммендаций категории (department)
    deps = ['GROCERY', 'PASTRY', 'MEAT-PCKGD', 'SEAFOOD-PCKGD', 'PRODUCE', 
            'NUTRITION', 'DELI', 'COSMETICS', 'MEAT', 'SEAFOOD', 'MISC SALES TRAN', 
            'SALAD BAR', 'GRO BAKERY', 'FROZEN GROCERY', 'SPIRITS', 'RESTAURANT',
            'RX', 'MEAT-WHSE', 'DAIRY DELI', 'CHEF SHOPPE', 'HBC', 'DELI/SNACK BAR', 'PORK']
    proper_deps = item_features.loc[item_features['department'].isin(deps), 'item_id'].tolist()
    data_train = data_train[data_train['item_id'].isin(proper_deps)]
    
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.    
    # Уберем слишком дорогие товарыs
    without_outliers = data_train[(data_train['sales_value']/data_train['quantity']).between(0.99, 99.)]
    not_cheep_or_expensive = without_outliers.item_id.unique().tolist()
    data_train = data_train[data_train['item_id'].isin(not_cheep_or_expensive)]
    
    # Оставим топ-N товаров
    popularity = data_train.groupby('item_id')['quantity'].count().reset_index()
    popularity.rename(columns={'quantity': 'n_sold'}, inplace=True)

    top_N = popularity.sort_values('n_sold', ascending=False).head(take_n_popular).item_id.tolist()
    data_train = data_train[data_train['item_id'].isin(top_N)]
    
    items = data_train['item_id'].unique().tolist()
    
    return items