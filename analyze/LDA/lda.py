import pyLDAvis.gensim_models
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim import corpora, models

if __name__ == '__main__':
    words_ls = []
    with open('outdemowei.txt', 'r', encoding='UTF-8') as f:
        data = f.readlines()
        for line in data:
            words_ls.append(line.split(' '))
    f.close()
    # 构造词典，将每个唯一的词语映射到一个唯一的整数ID
    dictionary = corpora.Dictionary(words_ls)
    # 基于词典，使【词】→【稀疏向量】，并将向量放入列表，形成【稀疏向量集】（即语料库）
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    # tf-idf编码
    tfidf = models.TfidfModel(corpus)
    # 将语料库转换为tf-idf编码形式
    corpus_lda = tfidf[corpus]
    # lda模型，num_topics设置主题的个数
    lda = LdaModel(corpus=corpus_lda, id2word=dictionary, num_topics=4, random_state=100, iterations=50)

    for topic in lda.print_topics(num_words=10):
        print(topic)
    # 用pyLDAvis可视化
    plot = pyLDAvis.gensim_models.prepare(lda, corpus_lda, dictionary)
    pyLDAvis.save_html(plot, 'ldaweibo.html')
