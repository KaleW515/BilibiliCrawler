import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np


def merge_data():
    msg_data = pd.read_csv('msg.csv')
    rank_data = pd.read_csv('rank.csv')
    result = []
    for index, msg_tup in msg_data.iterrows():
        for index_r, rank_tup in rank_data.iterrows():
            if int(msg_tup['aid']) == int(rank_tup['aid']):
                try:
                    zoom_num = ((int(rank_tup['coins']) / int(msg_tup['coin'])) + (
                        int(rank_tup['play']) / int(msg_tup['view'])) + (
                        int(rank_tup['review']) / int(msg_tup['danmaku']))) / 3
                    if zoom_num < 0.6:
                        break
                    temp_tuple = {
                        'aid': msg_tup['aid'],
                        'view': rank_tup['play'],
                        'danmaku': rank_tup['review'],
                        'replay': str(int(int(msg_tup['reply']) * zoom_num)),
                        'favorite': str(int(int(msg_tup['favorite']) * zoom_num)),
                        'coins': rank_tup['coins'],
                        'share': str(int(int(msg_tup['share']) * zoom_num)),
                        'like': str(int(int(msg_tup['like']) * zoom_num)),
                        'no_reprint': msg_tup['no_reprint'],
                        'pts': rank_tup['pts'],
                    }
                    result.append(temp_tuple)
                    del rank_tup
                except:
                    pass
    return result


def merge_0_1():
    mer_data = pd.read_csv('merge.csv')
    result_1 = []
    result_0 = []
    for index, mer_tup in mer_data.iterrows():
        if int(mer_tup['no_reprint']) == 1:
            result_1.append(mer_tup)
        else:
            result_0.append(mer_tup)
    column = ['aid', 'view', 'danmaku', 'replay', 'favorite', 'coins',
              'share', 'like', 'no_reprint', 'pts']
    data_0 = pd.DataFrame(columns=column, data=result_0)
    data_1 = pd.DataFrame(columns=column, data=result_1)
    data_0.to_csv('merge_0.csv', index=False)
    data_1.to_csv('merge_1.csv', index=False)


def write_csv(msg):
    column = ['aid', 'view', 'danmaku', 'replay', 'favorite', 'coins',
              'share', 'like', 'no_reprint', 'pts']
    data = pd.DataFrame(columns=column, data=msg)
    data.to_csv('merge.csv', index=False)


def main():
    result = merge_data()
    write_csv(result)


def read_data():
    mer_data = pd.read_csv('merge.csv')
    sns.pairplot(mer_data,
                 x_vars=['aid', 'view', 'danmaku', 'replay',
                         'favorite', 'coins', 'share', 'like', 'no_reprint'],
                 y_vars='pts', size=7, aspect=0.8, kind='reg')
    plt.show()


def reg():
    mer_data = pd.read_csv('merge_1.csv')
    feature_cols = ['view', 'danmaku', 'replay',
                    'favorite', 'coins', 'share', 'like']
    X = mer_data[feature_cols]
    Y = mer_data['pts']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=1)
    lin_reg = LinearRegression()
    model = lin_reg.fit(X_train, Y_train)
    print(lin_reg.intercept_)
    print(lin_reg.coef_)
    Y_pred = lin_reg.predict(X_test)
    plt.figure()
    plt.plot(range(len(Y_pred)), Y_pred, 'b', label="predict")
    plt.plot(range(len(Y_pred)), Y_test, 'r', label="test")
    plt.legend(loc="upper right")
    plt.xlabel("the number of pts")
    plt.ylabel('values of pts')
    plt.show()


if __name__ == '__main__':
    # main()
    # read_data()
    # merge_0_1()
    reg()
