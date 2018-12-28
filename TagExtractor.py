from sklearn.externals import joblib
from gensim.models import word2vec
from pyhanlp import *
from Category import *
import numpy as np

class TagExtractor:
    kmeans_model = joblib.load('kmeans.pkl')
    w2v_model = word2vec.Word2Vec.load('model_30w.model')

    print('loading complete..')

    def deperal_principle(self, word):
        """
        word: HanLP.word
        描述标签中可能出现的规则:
        主谓关系(n, n)(n, a)(n, d)(v, a)
        动宾关系(a, a)(n, n), 状中关系(d, d), 
        定中关系(n, n)(v, v)(a, a)(n, e), 动补结构(m, m)
        定中关系通常会组成名词性短语,需继续寻找修饰词
        主谓关系 动宾关系组成的(n, v ,a) 可以考虑寻找, 较复杂
        """
        if word.DEPREL == '主谓关系':
            # print('主谓关系', word.HEAD)
            if word.CPOSTAG == 'n':
                if word.HEAD.CPOSTAG == 'n' or word.HEAD.CPOSTAG == 'a' or word.HEAD.CPOSTAG == 'd':
                    return word.LEMMA + '+' + word.HEAD.LEMMA
            elif word.CPOSTAG == 'v' and word.HEAD.CPOSTAG == 'a':
                return word.LEMMA + '+' + word.HEAD.LEMMA

        elif word.DEPREL == '动宾关系':
            if word.CPOSTAG == 'a' and word.HEAD.CPOSTAG == 'a':
                return word.HEAD.LEMMA + '+' + word.LEMMA
            elif word.CPOSTAG == 'n' and word.HEAD.CPOSTAG == 'n':
                return word.LEMMA + '+' + word.HEAD.LEMMA

        elif word.DEPREL == '状中关系':
            if word.CPOSTAG == 'd' and word.HEAD.CPOSTAG == 'd':
                return word.LEMMA + '+' + word.HEAD.LEMMA

        elif word.DEPREL == '定中关系':
            if word.CPOSTAG == 'n' and word.HEAD.CPOSTAG == 'n':
                # 查看下一层是否为修饰词
                t = self.deperal_principle(word.HEAD)    
                return word.LEMMA + '+' + word.HEAD.LEMMA + ((t[t.rfind('+'):]) if t else '')
            elif word.CPOSTAG == 'n' and word.HEAD.CPOSTAG == 'e':
                return word.LEMMA + '+' + word.HEAD.LEMMA
            elif word.CPOSTAG == 'v' and word.HEAD.CPOSTAG == 'v':
                return word.LEMMA + '+' + word.HEAD.LEMMA
            elif word.CPOSTAG == 'a' and word.HEAD.CPOSTAG == 'a':
                return word.LEMMA + '+' + word.HEAD.LEMMA
            
        elif word.DEPREL == '动补结构':
            if word.CPOSTAG == 'm' and word.HEAD.CPOSTAG == 'm':
                return word.LEMMA + '+' + word.HEAD.LEMMA

        else:
            return None

    # 对标签中的词语进行向量相加得到词组向量
    def get_vec_of_tag(self, tag):
        """通过词向量相加获取标签词组向量"""
        if not tag:
            return [0 for i in range(100)] 
        word_list = tag.split('+')
        
        i = 0
        t = []
        for word in word_list:    
            try:
                t.append(self.w2v_model.wv.word_vec(word)) 
            except:
                # 词典外的不参与匹配
                return [0 for i in range(100)]
            finally:
                i += 1
        return np.sum(t, axis=0)

    def extract_tag(self, sentence):
        """
        从评论语句中抽取标签
        return: list
        """
        s = HanLP.parseDependency(sentence) # 词法依存分析 
        word_array = s.getWordArray()
        tags = []
        
        for word in word_array:
            tag = self.deperal_principle(word)
            # print("tag:", tag)
            if tag:
                # 利用kmeans模型预测其处在的类别
                cat = self.kmeans_model.predict([self.get_vec_of_tag(tag)])[0]
                # print("category:", cat)
                if cat in unknown_tag:
                    continue
                else:
                    find = False
                    for k_tag, tag_list in known_tag.items():
                        if cat in tag_list:
                            tags.append(k_tag)
                            find = True
                            break
                    if find:
                        continue
                    for k_tag, tag_list in accurate_tag.items():
                        if cat in tag_list:
                            tags.append(k_tag)
                            find = True
                            break
        return tags

t = TagExtractor()
# print(t.extract_tag('iphoneX 的运行速度很快，外观很好看'))