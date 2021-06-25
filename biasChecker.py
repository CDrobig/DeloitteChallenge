def checkData(data):
    score = 0

    unbalanced = unbalancedScore(data)
    score + unbalanced
    print("data checked!")

    return score


def unbalancedScore(data):
    unbalancedScore = 0

    binary_columns = []
    i = 0
    for column in data:
        if (len(data[column].unique()) == 2):
            binary_columns.append(i)
        i = i + 1

    for column in binary_columns:
        data_0 = data[data[column] < 1]
        percentage = data_0.size/data.size

        if percentage <= 10 or percentage >= 90:
            unbalancedScore += 10
            print('Column: ' + column + ' is significantly unbalanced')
        elif percentage <= 20 or percentage >= 80:
            unbalancedScore += 7
            print('Column: ' + column + ' is strongly unbalanced')
        elif percentage <= 30 or percentage >= 70:
            unbalancedScore += 5
            print('Column: ' + column + ' is unbalanced')
        elif percentage <= 40 or percentage >= 60:
            unbalancedScore += 2
            print('Column: ' + column + ' is slightly unbalanced')
        else:
            unbalancedScore+= 0
        return unbalancedScore
