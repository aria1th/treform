import os

from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
import pickle
import treform as ptm
from tqdm import tqdm
import matplotlib.ticker as mtick

f = [f.name for f in fm.fontManager.ttflist]
plt.rc('font', family='Malgun Gothic')
# get directory of treform library
directory = ptm.__path__[0]
# get relative directory of stopwords
stopwords = os.path.join(directory, 'stopwords', 'stopwordsKor.txt')


# Define functions here
# function that pickles the result with given name
def pickle_result(result, name=None):
    # if name is not given, extract name attribute from result
    if name is None:
        name = result.__name__
    pickle.dump(result, open(name, 'wb'))


def process_noun_corpus(corpus):
    # create pipeline
    pipeline = ptm.Pipeline(ptm.splitter.KoSentSplitter(), ptm.tokenizer.Komoran(),
                            ptm.helper.POSFilter('NN*'),
                            ptm.helper.SelectWordOnly(),
                            ptm.helper.StopwordFilter(file=stopwords))

    # we implemented progressbar attribute in Pipeline class so that we can see the progress of processing
    # print that we are processing noun corpus
    print("processing noun corpus")
    # now we have processed noun corpus. we can use this corpus to calculate Zipf's law
    # but we wrap corpus with tqdm so that we can see the progress of processing
    noun_result = pipeline.processCorpus(tqdm(corpus))
    # now pickle noun result
    pickle_result(noun_result, 'noun_result')
    # print that we finished processing noun corpus
    print("finished processing noun corpus")
    return noun_result


def process_verbs_corpus(corpus):
    # now we will process verb corpus
    # we will use same pipeline but we will change POSFilter to 'VV*'
    pipeline = ptm.Pipeline(ptm.splitter.KoSentSplitter(), ptm.tokenizer.Komoran(),
                            ptm.helper.POSFilter('VV*'),
                            ptm.helper.SelectWordOnly(),
                            ptm.helper.StopwordFilter(file=stopwords))
    # print that we are processing verb corpus
    print(" processing verb corpus")
    # now we have processed verb corpus. we can use this corpus to calculate Zipf's law
    verb_result = pipeline.processCorpus(tqdm(corpus))
    # now pickle verb result
    pickle_result(verb_result, 'verb_result')
    # print that we finished processing verb corpus
    print("finished processing verb corpus")
    return verb_result


def process_all_corpus(corpus):
    # now we will process all corpus even stopwords
    pipeline = ptm.Pipeline(ptm.splitter.KoSentSplitter(),
                            ptm.tokenizer.Word())
    # print that we are processing all corpus
    print(" processing all corpus")
    # now we have processed all corpus. we can use this corpus to calculate Zipf's law
    all_result = pipeline.processCorpus(tqdm(corpus))
    # now pickle all result
    pickle_result(all_result, 'all_result')
    # print that we finished processing all corpus
    print("finished processing all corpus")
    return all_result


def process_ngram_corpus(corpus, ngram=2):
    # now we will process all corpus even stopwords
    pipeline = ptm.Pipeline(ptm.splitter.KoSentSplitter(),
                            ptm.tokenizer.Word(),
                            ptm.helper.StopwordFilter(file=stopwords),  # filters stopwords
                            ptm.ngram.NGramTokenizer(ngram))
    # print that we are processing all corpus
    print(" processing {}-gram corpus".format(ngram))
    # now we have processed all corpus. we can use this corpus to calculate Zipf's law
    ngram_result = pipeline.processCorpus(tqdm(corpus))
    # now pickle all result
    # we will use different name for different ngram, from dictionary
    predefined_dict_name = {2: 'bigram_result', 3: 'trigram_result'}
    pickle_result(ngram_result, predefined_dict_name[ngram])
    return ngram_result


# read file from news_articles_201701_201812.csv
# prune lines to 5000 lines
# skip if you already have pruned file
if not os.path.exists('news_articles_201701_201812_pruned.csv'):
    line_prune = 5000
    # check if file exists
    if not os.path.exists('news_articles_201701_201812.csv'):
        raise FileNotFoundError('news_articles_201701_201812.csv does not exist')
    with open('news_articles_201701_201812.csv', 'r', encoding='utf-8') as f:
        # read lines
        lines = f.readlines()
        # prune lines
        lines = lines[:line_prune]
        # write lines to new file
        with open('news_articles_201701_201812_pruned.csv', 'w', encoding='utf-8') as f:
            f.writelines(lines)

# create corpus from pruned file
# we will use 4th column as text
corpus = ptm.CorpusFromCSVFile('news_articles_201701_201812_pruned.csv', 4)

# check if we have noun_result, verb_result, all_result, 2gram_result, 3gram_result already as pickle file.
# if we have, we will load it. if not, we will process it.
# by option, we remove existing pickle to process again.
remove_pickle = False
if remove_pickle:
    for file in ['noun_result', 'verb_result', 'all_result', 'bigram_result', 'trigram_result']:
        if os.path.exists(file):
            os.remove(file)
# check if we have noun_result already as pickle file.
if os.path.exists('noun_result'):
    # if we have, we will load it.
    with open('noun_result', 'rb') as f:
        noun_result = pickle.load(f)
else:
    # if not, we will process it.
    noun_result = process_noun_corpus(corpus)

# check if we have verb_result already as pickle file.
if os.path.exists('verb_result'):
    # if we have, we will load it.
    with open('verb_result', 'rb') as f:
        verb_result = pickle.load(f)
else:
    # if not, we will process it.
    verb_result = process_verbs_corpus(corpus)

# check if we have all_result already as pickle file.
if os.path.exists('all_result'):
    # if we have, we will load it.
    with open('all_result', 'rb') as f:
        all_result = pickle.load(f)
else:
    # if not, we will process it.
    all_result = process_all_corpus(corpus)

# check if we have 2gram_result already as pickle file.
if os.path.exists('bigram_result'):
    # if we have, we will load it.
    with open('bigram_result', 'rb') as f:
        bigram_result = pickle.load(f)
else:
    # if not, we will process it.
    bigram_result = process_ngram_corpus(corpus, 2)

# check if we have 3gram_result already as pickle file.
if os.path.exists('trigram_result'):
    # if we have, we will load it.
    with open('trigram_result', 'rb') as f:
        trigram_result = pickle.load(f)
else:
    # if not, we will process it.
    trigram_result = process_ngram_corpus(corpus, 3)


# now we have noun_result, verb_result, all_result, 2gram_result, 3gram_result
# input is double nested list such as [[word1, word2], [word3, word4],...]
# thus we need function to create flat list and count frequency of each word

def flatten_nested_list_genexpr(nested_list):
    for element in nested_list:
        if not isinstance(element, str):
            yield from flatten_nested_list_genexpr(element)
        else:
            yield element


def count_total_string(nested_list):
    return sum(1 for _ in flatten_nested_list_genexpr(nested_list))


def count_frequency(nested_list):
    # create flat list, recursively until we get non-nested list
    flat_genexpr = flatten_nested_list_genexpr(nested_list)
    # count frequency of each word
    # create empty dictionary that will hold frequency of each word
    frequency = {}
    # iterate over flat list
    for word in flat_genexpr:
        # if word is not in frequency dictionary
        if word not in frequency:
            # add word to frequency dictionary
            frequency[word] = 1
        # if word is in frequency dictionary
        else:
            # increase frequency of word by 1
            frequency[word] += 1
    # return frequency
    return frequency


# processed dictionary may contain non-words, remove it
def word_only_fdist(fdist):
    # only leave letters and underscore for n-gram words
    import re
    word_only_keys = [k for k in fdist.keys() if re.search(r'^[가-힣a-zA-Z_]+$',
                                                           k)]
    return {key: fdist[key] for key in word_only_keys}


# now we have function to calculate frequency of each word
# lets create function to calculate Zipf's law, simply by dividing counted frequency by total number of words

def calculate_zipf(result_list: list):
    # calculate frequency of each word
    frequency = count_frequency(result_list)
    # remove non-words
    frequency = word_only_fdist(frequency)
    # calculate total number of words
    total_words = sum(frequency.values())
    # divide frequency by total number of words
    zipf = {k: v / total_words for k, v in frequency.items()}
    # return zipf
    return zipf


# define function that automatically calculate zipf's law and plot it
def plot_zipf(result_list: list, title: str, prune: int = 5, save: bool = True) -> list:
    result_zipf: dict = calculate_zipf(result_list)
    # lets record unique words
    unique_words = len(result_zipf)
    # sort zipf's law by value
    result_zipf: list = sorted(result_zipf.items(), key=lambda x: x[1], reverse=True)
    # get top 100 words
    result_zipf: list = result_zipf[:prune]
    # get x and y axis
    x, y = zip(*result_zipf)
    # set figure size to fit long words
    plt.figure(figsize=(20, 10))
    # plot by bar, y is percentage, x is words
    plt.bar(x, y)
    # show actual percentage on bar, just above word
    for i, v in enumerate(y):
        plt.text(x[i], v, str(round(v * 100, 2)) + '%', ha='center',
                 va='bottom')
    # use percentage for y
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    # set x and y axis label
    # for xlabel, show total number of words
    plt.xlabel('Words (Total: ' + str(count_total_string(result_list)) + ')')
    plt.ylabel('Frequency')
    # annotate total number of words
    # for word, we will rotate vertical, and use adjust to fit long words
    plt.xticks(rotation=90, ha='right')
    # expand plot to fit long words
    # set title
    plt.title(title)
    plt.tight_layout()
    # save as png file
    if save:
        plt.savefig(title + '.png')
    # clear plot
    print('------------------------')
    print(title)
    print('Top ' + str(prune) + ' words and its frequency:')
    # result_zipf is dictionary that contains {word: frequency}. lets print it prettier
    for word, frequency in result_zipf:
        # use percentage for frequency, and round it to 4 decimal places
        print(word + ': ' + str(round(frequency * 100, 4)) + '%')
    print('Total number of words: ' + str(count_total_string(result_list)))
    print('Total number of unique words: ' + str(unique_words))
    plt.clf()
    return result_zipf


# 1. 품사가 명사인 단어로 Zipf's 법칙 계산해서 그래프 만들기
noun_zipf = plot_zipf(noun_result, 'Noun Zipf')
# 2. 품사가 동사인 단어로 Zipf's 법칙 계산해서 그래프 만들기
verb_zipf = plot_zipf(verb_result, 'Verb Zipf')
# 3. 품사 구분없이 모든 단어로 Zipf's 법칙 계산해서 그래프 만들기
all_zipf = plot_zipf(all_result, 'All Zipf')
# 4. 품사 구분없이, 불용어 제거 후, bi-gram과 tri-gram만 가지고 Zipf's 법칙 계산해서 그래프 만들기
bigram_zipf = plot_zipf(bigram_result, 'Bigram Zipf')
trigram_zipf = plot_zipf(trigram_result, 'Trigram Zipf')

# now lets process with top 100 words, but not save it as png file
# we overwrite previous result, just with different parameter
# 1. 품사가 명사인 단어로 Zipf's 법칙 계산해서 그래프 만들기
noun_zipf = plot_zipf(noun_result, 'Noun Zipf', prune=100, save=False)
# 2. 품사가 동사인 단어로 Zipf's 법칙 계산해서 그래프 만들기
verb_zipf = plot_zipf(verb_result, 'Verb Zipf', prune=100, save=False)
# 3. 품사 구분없이 모든 단어로 Zipf's 법칙 계산해서 그래프 만들기
all_zipf = plot_zipf(all_result, 'All Zipf', prune=100, save=False)
# 4. 품사 구분없이, 불용어 제거 후, bi-gram과 tri-gram만 가지고 Zipf's 법칙 계산해서 그래프 만들기
bigram_zipf = plot_zipf(bigram_result, 'Bigram Zipf', prune=100, save=False)
trigram_zipf = plot_zipf(trigram_result, 'Trigram Zipf', prune=100, save=False)

# now we have list of top <prune> words and its frequency. Lets plot as line plot in single graph, to see how it looks
# lets create figure then plot each line
plt.figure(figsize=(20, 10))
# for each result, instead of using word as x axis, we will use index
# lets create index for each word
# create empty list
x = []
# iterate over each result
for i, result in enumerate([noun_zipf, verb_zipf, all_zipf, bigram_zipf, trigram_zipf]):
    # append index to x
    x.append([i for i in range(len(result))])
# get y axis
y = [list(zip(*result))[1] for result in [noun_zipf, verb_zipf, all_zipf, bigram_zipf, trigram_zipf]]
# plot each line using loop
for i, result in enumerate([noun_zipf, verb_zipf, all_zipf, bigram_zipf, trigram_zipf]):
    # plot line. for label, use 'noun', 'verb', 'all', 'bigram', 'trigram' respectively instead of words
    plt.plot(x[i], y[i], label=['noun', 'verb', 'all', 'bigram', 'trigram'][i])

# set x and y axis label
# for xlabel, show index instead of word
plt.xlabel('Index')
plt.ylabel('Frequency')
# use percentage for y

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
# set title
plt.title('Zipf\'s Law')
# set legend
plt.legend()
# save as png file
plt.savefig('Zipf\'s Law.png')
