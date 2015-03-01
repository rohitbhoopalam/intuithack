"""
Author: Rohit Bhoopalam
"""
import nltk

def read_screen_user_file():
    _user_screen = {}

    f = open("../screen_to_users.tsv", "r")
    i = 0
    for screen_user in f:
        screen, user = screen_user.split()

        try:
            _user_screen[int(user)].append(int(screen))
        except KeyError:
            _user_screen[int(user)] = [int(screen)]

        i += 1
        print i
    
    return _user_screen

def read_user_label_file():
    _user_label = {}

    f = open("../user_labels.tsv", "r")
    i = 0
    for user_label in f:
        user, label = user_label.split()
        _user_label[int(user)] = int(label)
        i += 1
    
    return _user_label

def get_train_data(_user_screen, _user_label):
    _train_data = {}

    i = 0
    for user in _user_label:
        try:
            label = _user_label[user]
            screens = _user_screen[user]
            for screen in screens:
                try:
                    _train_data[(screen, label)] += 1
                except KeyError:
                    _train_data[(screen, label)] = 1
        except KeyError:
            pass

        print i, 'training'
        i += 1

    return _train_data

def get_score(zero, one, case):
    if case == 0:
        return float(zero+1.0)/float(zero + one + 2)
    return float(one+1.0)/float(zero + one + 2)

def predict_labels(_train_data, test_users, _user_screen):
    predicted_data = []

    i = 0
    for user in test_users:
        zero_score = 1
        one_score = 1

        screens = []
        try:
            screens = _user_screen[user]
        except KeyError:
            print "No user data available for user ", user
        for screen in screens:
            try:
                zero = _train_data[(screen, 0)]
            except KeyError:
                zero = 0
            try:
                one = _train_data[(screen, 1)]
            except KeyError:
                one = 0

            zero_score *= get_score(zero, one, 0)
            one_score *= get_score(zero, one, 1)

        if one_score>zero_score:
            predicted_data.append((user, 1))
        else:
            predicted_data.append((user, 0))

        print i, 'predicting'
        i += 1

    return predicted_data

def features(user, _user_screen):
    f = {}
    try:
        screens = _user_screen[user]
    except KeyError:
        screens = []
    for screen in screens:
        f[str(screen)] = 1

    return f 

def train_nltk(_user_screen, _user_label):
    featuresets = []
    i = 0
    for user in _user_label:
        print 'training', i
        featuresets.append((features(user, _user_screen), _user_label[user]))
        i+=1
        if i == 100000:
            return nltk.NaiveBayesClassifier.train(featuresets)

    #featuresets = [(features(user, _user_screen), _class) for (user, _class) in _user_label.items()[:50000]]
    return nltk.NaiveBayesClassifier.train(featuresets)
            
def write_to_file(_user_label):
    f = open('problem2_naive2.tsv', 'wa')

    for user, label in _user_label:
        f.write(str(user) + "\t" + str(label) + "\n")

    f.close()
    return

def predict_labels_nltk(_classifier, _test_users, _user_screen):
    predicted_data = []

    i = 0
    for user in _test_users:
        _class = _classifier.classify(features(user, _user_screen))
        predicted_data.append((user, _class))
        print i, "predicting"
        i += 1

    return predicted_data

if __name__ == "__main__":
    user_screen = read_screen_user_file()
    user_label = read_user_label_file()
    #train_data = get_train_data(user_screen, user_label)
    print "training data"
    classifier = train_nltk(user_screen, user_label)
    test_users = set(user_screen.keys()) - set(user_label.keys())
    user_labels = predict_labels_nltk(classifier, test_users, user_screen)
    write_to_file(user_labels)
