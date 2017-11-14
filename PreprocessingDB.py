import string


path = '/home/joseph/Documents/AI/Machine Learning/databases/smsspamcollection/SMSSpamCollection'
stopwordsPath = '/home/joseph/Documents/AI/Machine Learning/databases/smsspamcollection/stopwords'
target_path = path+'Clean'

stopwords = []
LIMIT = 20
c = 0

with open(stopwordsPath) as fs:
    print(fs.read().splitlines())
fn = open(target_path, 'w')
with open(path) as f:
    for line in f:
        c += 1
        # #If you want case sensitive remove .lower() below
        new_line = line.translate(str.maketrans('', '', string.punctuation+'0123456789‘')).lower()
        new_line = new_line.split()
        result = [word for word in new_line if word not in stopwords]
        fn.write(' '.join(result)+'\n')
        # #Limit the amount of lines read
        # if c > LIMIT:
        #     break
f.close
fn.close
fs.close









