from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import torch
import biasGAN

def checkData(data):
    score = 0
    data = data.drop(["Unnamed: 0"], axis=1)
    #todo: handle 2 string solumns

    #calculate deviation of feature importance in order to get balanced features
    featureImportanceScore=0
    X = data.drop(["default"], axis=1)
    y = data["default"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    ss = StandardScaler()
    X_train_scaled = ss.fit_transform(X_train)

    pca = PCA().fit(X_train_scaled)

    loadings = pd.DataFrame(
        data=pca.components_.T * np.sqrt(pca.explained_variance_),
        columns=[f'PC{i}' for i in range(1, len(X_train.columns) + 1)],
        index=X_train.columns
    )
    loadings.head()
    pc1_loadings = loadings.sort_values(by='PC1', ascending=False)[['PC1']]
    pc1_loadings = pc1_loadings.reset_index()
    pc1_loadings.columns = ['Attribute', 'CorrelationWithPC1']

    print(pc1_loadings['Attribute'])
    print(pc1_loadings['CorrelationWithPC1'].apply(abs))
    featureImportance = pc1_loadings['CorrelationWithPC1'].apply(abs)
    deviation = featureImportance.std()

    if deviation >= 0.4:
        featureImportanceScore += 10
        print('Feature Importance is significantly unbalanced')
    elif deviation >= 0.3:
        featureImportanceScore += 7
        print('Feature Importance is strongly unbalanced')
    elif deviation >= 0.2:
        featureImportanceScore += 7
        print('Feature Importance is unbalanced')
    elif deviation >= 0.1:
        featureImportanceScore += 7
        print('Feature Importance is slightly unbalanced')
    else:
        featureImportanceScore += 0

    featureImportance = pd.concat([pc1_loadings['Attribute'], pc1_loadings['CorrelationWithPC1']], axis=1)
    print(str(featureImportance))

    print("Feature Importance checkt with score: " + str(featureImportanceScore))


    #check balance of binary variables
    unbalancedScore = 0

    binary_columns = []
    i = 0
    for column in data:
        if (len(data[column].unique()) == 2):
            binary_columns.append(i)
        i = i + 1

    for column in binary_columns:
        data_0 = data.iloc[:, column-1] < 1
        print(data_0)

        percentage = data_0.size / data.size

        if percentage <= 10 or percentage >= 90:
            unbalancedScore += 10
            print('Column: ' + str(column) + ' is significantly unbalanced')
        elif percentage <= 20 or percentage >= 80:
            unbalancedScore += 7
            print('Column: ' + str(column) + ' is strongly unbalanced')
        elif percentage <= 30 or percentage >= 70:
            unbalancedScore += 5
            print('Column: ' + str(column) + ' is unbalanced')
        elif percentage <= 40 or percentage >= 60:
            unbalancedScore += 2
            print('Column: ' + str(column) + ' is slightly unbalanced')
        else:
            unbalancedScore += 0

    print("Balance of binary variables checkt with score: " + str(unbalancedScore))

    #check columns for bias-driving features
    biasDriverScore = 0
    biasDrivers = ["sex", "gender", "sexuality", "age", "race", "ethnicity", "religion", "belief", "minority", "denomination", "confession", 'address', "city", "postcode", "zip", "street"]
    columnNames = data.columns

    for column in columnNames:
        for biasDriver in biasDrivers:
            if column == biasDriver:
                biasDriverScore += 25
                print("The column " + str(column) + "might be a bias-driving feature")


    print("Bias driving columns are checkt with score: " + str(biasDriverScore))

    #check for extremly high correlation for the outcome variables
    correlationScore =0
    for column in columnNames:
        correlation = data["default"].corr(data[column])
        print(column + " corrlates with default by a p-value of " + str(correlation))
        if correlation >= 0.9 or correlation <= -0.9 :
            correlationScore += 10
            print("There is a significant correlation between " + str(column) + ' and default which might cause a bias')
            #todo: correct student T-Test
    print("Balance of binary variables checkt with score: " + str(correlationScore))

    #todo: sum possible score
    score = featureImportanceScore + unbalancedScore + biasDriverScore + correlationScore
    print("Data checked, Bias Score is at: " + str(score))

    return score

def generateData(data):
    #generator=biasGAN.DenseGenerator
    generator = torch.load("/models/unbiased_gen_2506")
    generator.eval()

    #discriminator = biasGAN.DenseDiscriminator
    discriminator = torch.load("/models/unbiased_disc_2506")
    discriminator.eval()
    # todo: generate data

    data = "./exampleData/unbiased/balancedData.csv"

    return data



def replaceCategoricals(data):

    data = data.replace(to_replace="MT04PA", value=0)
    data = data.replace(to_replace="MT15PA", value=1)
    data = data.replace(to_replace="MT01RA", value=2)
    data = data.replace(to_replace="MT12RA", value=3)

    data = data.replace(to_replace="MZ10CD", value=0)
    data = data.replace(to_replace="MZ11CD", value=1)
    data = data.replace(to_replace="MZ01CD", value=2)
