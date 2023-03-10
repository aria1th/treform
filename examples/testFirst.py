import shutil
import time
import treform as ptm
import os

path = os.path.dirname(ptm.__file__)
force_refresh = False  # Flag for refreshing sample data folder.


def download_samples():
    base_repo = r'https://github.com/MinSong2/treform'
    target_relative_path = r'/sample_data'
    target_folder = os.path.join(path, 'sample_data')
    print(os.path.abspath(target_folder))
    tmp_path = '/tmp/clone'
    if os.path.exists(tmp_path):
        #  Somehow its being used by other process?
        tmp_path = f'/tmp/clone/{time.strftime("%H%M%S")}'
    if force_refresh:
        shutil.rmtree(target_folder)
    try:
        import git
    except (ModuleNotFoundError, ImportError):
        import pip
        print('Installing pygithub to download sample datas')
        pip.main(['install', 'pygithub'])
    import git
    try:
        print(f'Created temporary path {os.path.abspath(tmp_path)}')
        repo = git.Repo.clone_from(base_repo, tmp_path)
        shutil.copytree(os.path.abspath(tmp_path + target_relative_path), target_folder)
    finally:
        del repo
        shutil.rmtree(tmp_path, ignore_errors=True)
        print(f'Removed temporary path {os.path.abspath(tmp_path)}')


if os.path.exists(os.path.join(path, 'sample_data')) and not force_refresh:
    print('Sample data folder already exists, set flag force_refresh = True to re-download')
else:
    download_samples()

# 다음은 분석에 사용할 corpus를 불러오는 일입니다. sampleEng.txt 파일을 준비해두었으니, 이를 읽어와봅시다.
# ptm의 CorpusFromFile이라는 클래스를 통해 문헌집합을 가져올 수 있습니다. 이 경우 파일 내의 한 라인이 문헌 하나가 됩니다.
#corpus = ptm.CorpusFromFieldDelimitedFile('../sample_data/donald.txt',2)
#corpus = ptm.CorpusFromDirectory('./tmp', True)
#corpus, pair_map = ptm.CorpusFromFieldDelimitedFileWithYear('./data/donald.txt')
corpus = ptm.CorpusFromFile(os.path.join(path, 'sample_data', 'sampleEng.txt'))

import nltk
nltk.download('punkt')

#pipeline = ptm.Pipeline(ptm.splitter.NLTK(),
#                        ptm.tokenizer.Komoran(),
#                        ptm.helper.POSFilter('NN*'),
#                        ptm.helper.SelectWordOnly(),
#                        ptm.ngram.NGramTokenizer(3),
#                        ptm.helper.StopwordFilter(file='../stopwords/stopwordsKor.txt')
#                        )

pipeline = ptm.Pipeline(ptm.splitter.NLTK(),
                        ptm.tokenizer.Word())

#pipeline = ptm.Pipeline(ptm.splitter.NLTK(),
#                        ptm.segmentation.SegmentationKorean('../model/korean_segmentation_model.crfsuite'),
#                        ptm.ngram.NGramTokenizer(3),
#                        ptm.helper.StopwordFilter(file='../stopwords/stopwordsKor.txt')
#                        )

result = pipeline.processCorpus(corpus)

with open("demofile.csv", 'w', encoding='utf8') as f:
    for doc in result:
        for sent in doc:
            f.write('\t'.join(sent) + "\n")

print('== 문장 분리 + 형태소 분석 + 명사만 추출 + 단어만 보여주기 + 구 추출 ==')
print(result)
print()
