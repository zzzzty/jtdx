from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import codecs
import jieba
from collections import Counter
from .settings import BASE_DIR
from tevaluation.models import Comment
#文件目录
d = path.dirname('__file__')
#print(BASE_DIR)


#停用词
def stopwordslist(stopwords_path):
    stopwords = [line.strip() for line in open(stopwords_path).readlines()]
    return stopwords

#教师，学年，cl
def get_words(txt,stopwords_path):
    seg_list = jieba.cut(txt)
    c = Counter()
    stopwords = stopwordslist(stopwords_path)
    for x in seg_list:
        if len(x)>1 and x != '\r\n' and x not in stopwords:
            c[x] += 1
    return dict(c)
    #return dict(c.most_common(200))#返回前200个

def save_plt_image(teacher,semester):
    text = "我听不懂你在说什么"

    alice_coloring = imread(path.join(BASE_DIR,'static/wordcloud/alice_color.png'))
    fontpath = path.join(BASE_DIR,'static/wordcloud/10016.ttf')
    wc = WordCloud(background_color="white",mask=alice_coloring,font_path=fontpath, \
        max_font_size=400,random_state=42)

    texts = Comment.objects.filter(teacher=teacher,semester=semester)
    for t in texts:
        text += t.text
    stopwords_path = path.join(BASE_DIR,'static/wordcloud/stopword.txt')
    txt_freq = get_words(text,stopwords_path)
    #print(text)
    wc.generate_from_frequencies(txt_freq)
    image_colors = ImageColorGenerator(alice_coloring)
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(BASE_DIR+"/static/wordcloud/cloud/"+teacher.teacher.username+"-"+str(semester)+".png")