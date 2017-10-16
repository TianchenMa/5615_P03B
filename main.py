from data_examining.data_fetch import fetch_data
import os
from sklearn.model_selection import train_test_split
# from sklearn.datasets import make_regression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
from visualization.visual_utils import distribution_fig, box_whisker, histo
from scripts.rbf_test import rbf_svm_influence




def ml_process(customer, feature, label):
    feature_name = feature
    print(feature_name)
    X_customers = customer[feature_name]
    y_customers = customer[label]
    X_train, X_test, y_train, y_test = train_test_split(X_customers, y_customers, random_state=0)
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    cmap = cm.get_cmap('gnuplot')
    scatterr = pd.plotting.scatter_matrix(X_train, c=y_train, marker='o', s=40, hist_kwds={'bins': 15}, figsize=(9, 9),
                                         cmap=cmap)

    rf = GaussianNB()

    rf.fit(X_train, y_train)

    # pcc(rf, X_train, y_train, X_test, y_test, 'output')

    x = X_customers
    y = rf.predict(x)
    print(len(x),len(y))

    print('score (training): {:.3f}'
          .format(rf.score(X_train, y_train)))
    print('score (test): {:.3f}'
          .format(rf.score(X_test, y_test)))

    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X_train[feature_name[1]], X_train[feature_name[1]], X_train[feature_name[2]], c=y_train, marker='o', s=100)
    ax.set_xlabel(feature_name[0])
    ax.set_ylabel(feature_name[1])
    ax.set_zlabel(feature_name[2])
    plt.show()




if __name__ == '__main__':
    # looping to wait for the commands from customer
    while(1):
        raw_cmd = input("Enter command: ")
        cmd = raw_cmd.split()
        if not cmd:
            print("You need to enter a command...")
            continue
        if cmd[0].lower() == 'fetch':
            customer = fetch_data('source_datasets/{}'.format(cmd[1]))
            # print(customer.values)
        elif cmd[0].lower() == 'list':
            files = os.listdir('source_datasets')
            for f in files:
                print(f +' '+ str(files.index(f)))

        elif cmd[0].lower() == 'print':
            cols = customer.columns.values.tolist()
            paras = {}
            for c in cols:
                print(c  +' '+ str(cols.index(c)))
                paras[cols.index(c)] = c
                # print(paras)
        elif cmd[0].lower() == 'ml':
            feature_tags = cmd[1:-1]
            features = []
            for f in feature_tags:
                features.append(paras[int(f)])
            label = paras[int(cmd[-1])]
            ml_process(customer, features, label)
        elif cmd[0].lower() == 'fig':
            if cmd[1].lower() == '0':
                distribution_fig(customer=customer)
            elif cmd[1].lower() == '1':
                box_whisker(customer)
            elif cmd[1].lower() == '2':
                histo(customer)
            elif cmd[1].lower() == 'all':
                distribution_fig(customer=customer)
                box_whisker(customer)
                histo(customer)
        elif cmd[0].lower() == 'influ_fig':
            rbf_svm_influence()
