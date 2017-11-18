#                     Joseph Aguilar Feener
#                          17/10/2017
#     Naive Bayes Text Classifier with Bernoulli Distributions

import NaiveBayesClassificationBernoulli as nbcb
import random
import numpy as np
from tkinter import *

path = '/home/joseph/Documents/AI/Machine Learning/databases/smsspamcollection/SMSSpamCollectionClean'
# 5574 total values in the SMS dataset


def print_list(d):
    print('PROB HAM VEC LETS GO:::: ')
    # print(*d, sep='\n')
    for k in d:
        print(str(sorted(k.items())))
    return


def length_db(data):
    k = 0
    for line in data:
        k += 1
    return k


def random_generate_db(data, quantity):
    if len(data) > quantity:
        random_db = []
        updated_db = data
        for i in range(quantity):
            val = random.randint(0, len(updated_db)-1)
            random_db.append(updated_db[val])
            del updated_db[val]
            # print('Len Updated db : '+str(len(updated_db)))
    else:
        return data
    return random_db, updated_db


def generate_db(data, start, end):
    k = 0
    new_data = []
    for line in data:
        k += 1
        if (k > start) and (k <= end):
            new_data.append(line)
    return new_data


def join_dicts(v2, v3):
    words_dict2 = v2.pop()
    for words_bag2 in v2:
        for word2 in words_bag2:
            if word2 in words_dict2:
                words_dict2[word2] = (words_dict2[word2]+words_bag2[word2])/2.0
            else:
                words_dict2[word2] = words_bag2[word2]
    words_dict3 = v3.pop()
    for words_bag3 in v3:
        for word3 in words_bag3:
            if word3 in words_dict3:
                words_dict3[word3] = (words_dict3[word3]+words_bag3[word3])/2.0
            else:
                words_dict3[word3] = words_bag3[word3]
    return words_dict2, words_dict3


def set_to_zero(v2, v3):
    for val2 in v2:
        v2[val2] = 0
    for val3 in v3:
        v3[val3] = 0
        print(v3[val3])
        return v2, v3


def calc_media_vects(v2, v3, fullv2, fullv3):
    nwords2, nwords3 = set_to_zero(fullv2.copy(), fullv3.copy())
    new_v2, new_v3 = set_to_zero(fullv2.copy(), fullv3.copy())
    print(type(v2))
    print(new_v2)
    print("*")
    print(new_v3)
    for words_bag2 in v2:
        for word2 in words_bag2:
            new_v2[word2] += words_bag2[word2]
            nwords2[word2] += 1
    for words_bag3 in v3:
        for word3 in words_bag3:
            new_v3[word3] += words_bag3[word3]
            nwords3[word3] += 1
    for word_val2 in new_v2:
        print("*")
        new_v2[word_val2] = new_v2[word_val2] / nwords2[word_val2]
    for word_val3 in new_v3:
        new_v3[word_val3] = new_v3[word_val3] / nwords3[word_val3]
    return new_v2, new_v3


def validation_method_choose():
    mText = input_validation.get()
    print('values ISSS ' + mText)
    if mText == 'RS':
        mEntry = Entry(mGui, textvariable=percentage_sets).pack()
        mButton = Button(mGui, text='Insert', command=main_execution_random_sampling, fg='black', bg='white').pack()
    elif mText == 'KF':
        mEntry = Entry(mGui, textvariable=n_folds).pack()
        mButton = Button(mGui, text='Insert', command=main_execution_k_folds, fg='black', bg='white').pack()
        n_folds.set(5)
    else:
        mLabel2 = Label(mGui, text='Sorry, validation method not found. Retry please.').pack()
    return


def main_execution_random_sampling():
    with open(path) as f:
        db_entire = f.read()
        db = db_entire.splitlines()
        len_db = length_db(db)
        perc_db = (percentage_sets.get() / 100)*len_db
        new_db = generate_db(db, 0, perc_db)
        dict_actual, prob_spam_vec, prob_ham_vec, spam, ham = nbcb.naive_bayes_classification_bernoulli_learning\
            (new_db, ['spam', 'ham'])
        new_db = generate_db(db, perc_db, len_db)
        nbcb.naive_bayes_classification_bernoulli_classify(new_db, dict_actual, prob_spam_vec, prob_ham_vec,
                                                           spam, ham)
        return


def main_execution_k_folds():
    dict_actual, prob_spam_vec, prob_ham_vec, spam, ham = [], [], [], [], []
    print("What's your problem?")
    with open(path) as f:
        db_entire = f.read()
        db = db_entire.splitlines()
        len_db = length_db(db) # After the improvements it's the same
        # print("((((((((((((^^^^", str(len_db))
        print("((((((((((((^^^^", str(len(db)))

        folds_number = n_folds.get()

        for x in range(0, folds_number-1):
            rand_db, db = random_generate_db(db, int(len_db/folds_number))
            # print("Len DB", str(len(db)))
            # print("Len Rand_DB", str(len(rand_db)))
            dict_actual_new, prob_spam_vec_new, prob_ham_vec_new, spam_new, ham_new = nbcb\
                .naive_bayes_classification_bernoulli_learning(rand_db, ['spam', 'ham'])
            prob_ham_vec.append(prob_ham_vec_new)
            prob_spam_vec.append(prob_spam_vec_new)
            spam.append(spam_new)
            ham.append(ham_new)

        # print(str(dict_actual_new))
        # print(' prob_spam_vec = ' + str(prob_spam_vec_new))
        print(' spam mean: '+str(np.mean(spam)))
        print('dict_actual dim: ' + str(len(dict_actual)))
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        # print_list(prob_ham_vec)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        print_list(prob_spam_vec)
        print('length:  ' + str(len(prob_spam_vec)))

        new_prob_spam_vec, new_prob_ham_vec = join_dicts(prob_spam_vec, prob_ham_vec)

        print(sorted(new_prob_spam_vec.items()))
        print('length:  ' + str(len(new_prob_spam_vec)))

        # new2_prob_spam_vec, new2_prob_ham_vec = calc_media_vects(prob_spam_vec,
        #                                     prob_ham_vec, new_prob_spam_vec, new_prob_ham_vec)

        nbcb.naive_bayes_classification_bernoulli_classify(db, dict_actual_new, new_prob_spam_vec,
                                                           new_prob_ham_vec, np.mean(spam), np.mean(ham))

        return


mGui = Tk()
n_folds = IntVar()
percentage_sets = IntVar()
input_validation = StringVar()
v = IntVar()
mGui.geometry('750x450+500+300')
mGui.title(' Naive Bayes Text Classifier with Bernoulli Distributions')
mLabel = Label(mGui, text='Please insert the validation method (Random Sampling / K-folds): ').pack()
Radiobutton(mGui, text="RS", variable=input_validation, value='RS').pack(anchor=W)
Radiobutton(mGui, text="KF", variable=input_validation, value='KF').pack(anchor=W)

input_validation.set('KF')

mButton = Button(mGui, text='Insert', command=validation_method_choose, fg='black', bg='white').pack()
print(str(v))
mGui.mainloop()




