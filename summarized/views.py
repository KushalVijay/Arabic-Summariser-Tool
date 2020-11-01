from django.shortcuts import render

# Create your views here.

from .sumrized import Sumrized
from .helper import Helper
import gensim.models.keyedvectors as w2v
import pickle
from .similarity import TextSimilarity

def home(request):
    return render(request,'index.html')

def summarizer_tool(request):

    if request.method == 'POST':
        percent = int(request.POST.get('percent'))
        text = request.POST.get('text')
        lang = "ar"

        tools = "summarized/tools"
        # word2vecArPath = tools + "/wiki.ar.vec"
        # word2vecAr = w2v.KeyedVectors.load_word2vec_format(word2vecArPath,
        #                                                         binary=False,
        #                                                         unicode_errors='ignore',
        #                                                         limit=50000)

        docs = open("summarized/wordvec.pickle", "rb")
        word2vec = pickle.load(docs)
        docs.close()


        help = Helper(lang=lang)

        sentences = help.getArticleSentences(text)

        summarySize = percent  # [10, 100]
        limit = (summarySize * len(sentences)) / 100

        sumrized = Sumrized(lang, word2vec)
        summary = sumrized.summarize(text, limit)

        return render(request,'about.html',{'summary':summary})

    return render(request,'about.html')


def similarity_tool(request):
    if request.method=='POST':
        obj = TextSimilarity()
        text1 = request.POST.get('text1')
        text2 = request.POST.get('text2')
        result = float(obj.similarity(text1,text2)) * 100
        result = round(result,2)
        return render(request,'similarity.html',{'percent':result})

    return render(request,'similarity.html',{'percent':None})




