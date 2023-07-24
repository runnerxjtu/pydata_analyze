import jieba  # 分词

def stopwordslist():
    stopwords = [line.strip() for line in open('停用词.txt', encoding='UTF-8').readlines()]
    return stopwords

def seg_depart(sentence):
    jieba.load_userdict('自定义词.txt')  # 自定义词典不被分割
    sentence_depart = jieba.cut(sentence.strip(), cut_all=False, HMM=True)
    stopwords = stopwordslist()
    outstr = ''
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t' and len(word) != 1:
                outstr += word
                outstr += " "
    return outstr

if __name__=='__main__':
    filename = "content.txt"
    outfilename = "outdemowei.txt"
    inputs = open(filename, 'r', encoding='UTF-8')
    outputs = open(outfilename, 'w', encoding='UTF-8')
    for line in inputs:
        a = line.split()
        line_seg = seg_depart(line)
        outputs.write(line_seg + '\n')
    outputs.close()
    inputs.close()
    print("删除停用词和分词成功！！！")