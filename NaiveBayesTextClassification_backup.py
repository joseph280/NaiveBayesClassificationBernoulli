#                     Joseph Aguilar Feener
#                          17/10/2017
#     Naive Bayes Text Classifier with Bernoulli Distributions

path = '/home/joseph/Documents/AI/Machine Learning/databases/smsspamcollection/SMSSpamCollectionClean'
TRAINING_SET = 5000
TEST_SET = 500
# 5574 total values in the SMS dataset


def create_dictionary():
    words_dict = {}
    with open(path) as f:
        for line in f:
            words_list = line.split()
            first = True
            for word in words_list:
                if first:
                    first = False
                else:
                    if word not in words_dict:
                        words_dict[word] = 0
    f.close
    return words_dict


def calculate_probabilities(prob_spam_vec2, prob_ham_vec2, sp, h):
    for word_value in prob_spam_vec2:
        prob_spam_vec2[word_value] = (prob_spam_vec2[word_value]+1) / (sp+2)
    for word_value in prob_ham_vec2:
        prob_ham_vec2[word_value] = (prob_ham_vec2[word_value]+1) / (h+2)
    return


def count_values(first_bool, spam_bool_val, spam_val, ham_val):
    if first_bool:
        first_bool = False
        if word == 'spam':
            spam_val += 1
            spam_bool_val = True
        else:
            ham_val += 1
    else:
        if spam_bool_val:
            prob_spam_vec[word] += 1
        else:
            prob_ham_vec[word] += 1
    return first_bool, spam_bool_val, spam_val, ham_val


def print_dict(d):
    for keys, values in d.items():
        print(keys)
        print(values)
    return


spam, ham, c, k, accuracy = 0, 0, 0, 0, 0
actual_dict = create_dictionary()
prob_spam_vec = actual_dict.copy()
prob_ham_vec = actual_dict.copy()
with open(path) as f:
    for line in f:
        c += 1
        words_list = line.split()
        first = True
        spam_bool = False
        for word in words_list:
            first, spam_bool, spam, ham = count_values(first, spam_bool, spam, ham)
        if c >= TRAINING_SET:
            break
    prob_spam = spam / TRAINING_SET
    prob_ham = ham / TRAINING_SET
    print('prob SPAM = '+str(prob_spam))
    print('prob HAM = '+str(prob_ham))
    print('SPAM quantities: '+str(spam))
    print('HAM quantities: '+str(ham))
    calculate_probabilities(prob_spam_vec, prob_ham_vec, spam, ham)
    for line2 in f:
        k += 1
        first_bool = True
        words_list2 = line2.split()
        res_prob_spam = prob_spam
        res_prob_ham = prob_ham
        for word2 in words_list2:
            if first_bool:
                first_bool = False
                real_class = 'SPAM' if word == 'spam' else 'HAM'
                print('Line number: '+str(c+k)+' real value = ' + real_class)
            else:
                if word2 in actual_dict:
                    # prob_spam_SMS, prob_ham_SM = classify_test_set(prob_spam_vec, prob_ham_vec, prob_spam, prob_ham, word2)
                    res_prob_spam *= prob_spam_vec[word2]
                    res_prob_ham *= prob_ham_vec[word2]
        classifier_says = 'SPAM' if res_prob_spam > res_prob_ham else 'HAM'
        print('The classifier says: It is ' + classifier_says + ' with spam value: '+str(res_prob_spam)+' and ham value: '+str(res_prob_ham))
        if real_class == classifier_says:
            accuracy += 1
        if k >= TEST_SET:
            break
    accuracy = (accuracy*100) /TEST_SET
    print('Accuracy: '+str(accuracy)+'%')