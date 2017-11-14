def count_values(first_bool, spam_bool_val, spam_val, ham_val, prob_spam_vec_val, prob_ham_vec_val, word):
    if first_bool:
        first_bool = False
        if word == 'spam':
            spam_val += 1
            spam_bool_val = True
        else:
            ham_val += 1
    else:
        if spam_bool_val:
            prob_spam_vec_val[word] += 1
        else:
            prob_ham_vec_val[word] += 1
    return first_bool, spam_bool_val, spam_val, ham_val


def calculate_probabilities(prob_spam_vec2, prob_ham_vec2, sp, h):
    for word_value in prob_spam_vec2:
        prob_spam_vec2[word_value] = (prob_spam_vec2[word_value]+1) / (sp+2)
    for word_value in prob_ham_vec2:
        prob_ham_vec2[word_value] = (prob_ham_vec2[word_value]+1) / (h+2)
    return


def create_dictionary(db):
    words_dict = {}
    for line in db:
        words_list = line.split()
        first = True
        for word in words_list:
            if first:
                first = False
            else:
                if word not in words_dict:
                    words_dict[word] = 0
    return words_dict


def print_dict(d):
    for keys, values in d.items():
        print(keys)
        print(values)
    return


def naive_bayes_classification_bernoulli_learning(db, classes):
    actual_dict = create_dictionary(db)
    prob_spam_vec = actual_dict.copy()
    prob_ham_vec = actual_dict.copy()
    spam, ham, c = 0, 0, 0
    for line in db:
        c += 1
        words_list = line.split()
        first = True
        spam_bool = False
        for word in words_list:
            first, spam_bool, spam, ham = count_values(first, spam_bool, spam, ham, prob_spam_vec, prob_ham_vec, word)
    prob_spam = spam / c
    prob_ham = ham / c
    print('prob SPAM = '+str(prob_spam))
    print('prob HAM = '+str(prob_ham))
    print('SPAM quantities: '+str(spam))
    print('HAM quantities: '+str(ham))

    print('SPAM VECTOR quantities: '+str(prob_spam_vec))
    print('HAM VECTOR quantities: '+str(prob_ham_vec))
    calculate_probabilities(prob_spam_vec, prob_ham_vec, spam, ham)
    return actual_dict, prob_spam_vec, prob_ham_vec, prob_spam, prob_ham


def naive_bayes_classification_bernoulli_classify(db, actual_dict, prob_spam_vec, prob_ham_vec, p_spam, p_ham,):
    k, accuracy = 0, 0
    for line2 in db:
        k += 1
        first_bool = True
        words_list2 = line2.split()
        res_prob_spam = p_spam
        res_prob_ham = p_ham
        print(str(p_spam)+'*&!@^#############################################')
        for word2 in words_list2:
            if first_bool:
                first_bool = False
                real_class = 'SPAM' if word2 == 'spam' else 'HAM'
                print('Line number: '+str(k)+' real value = ' + real_class)
            else:
                if word2 in actual_dict:
                    res_prob_spam *= prob_spam_vec[word2]
                    res_prob_ham *= prob_ham_vec[word2]
        classifier_says = 'SPAM' if res_prob_spam > res_prob_ham else 'HAM'
        print('The classifier says: It is ' + classifier_says + ' with spam value: '+str(res_prob_spam)+' and ham value: '+str(res_prob_ham))
        if real_class == classifier_says:
            accuracy += 1
    accuracy = (accuracy*100) / k
    print('Accuracy: '+str(accuracy)+'%')
    print('Accuracy: '+str(k))
    return
