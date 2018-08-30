"""
MIT License

Copyright (c) 2018 TOSKT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import math,sys
from janome.tokenizer import Tokenizer
import tkinter as tk
import tkinter.filedialog as tf

class BayesianFilter:
    def __init__(self):
        self.words = set()
        self.word_dic={}
        self.category_dic={}

    def split(self,text):
        result = []
        t = Tokenizer()
        tokens = t.tokenize(text)
        for token in tokens:
            sf = token.surface
            result.append(sf)
        return result

    def wordplus(self,word,category):
        self.word_dic.setdefault(category,{})
        self.word_dic[category].setdefault(word,0)
        self.word_dic[category][word] += 1
        self.words.add(word)

    def categoryplus(self,category):
        self.category_dic.setdefault(category,0)
        self.category_dic[category] += 1

    def train(self,text,category):
        word_list = self.split(text)
        for word in word_list:
            self.wordplus(word,category)
        self.categoryplus(category)

    def sc(self,words,category):
        sc = math.log(self.category_prb(category))
        for word in words:
            sc += math.log(self.word_prb(word,category))
            return sc

    def incat_get_count(self,word,category):
        if word in self.word_dic[category]:
            return self.word_dic[category][word]
        else:
            return 0

    def category_prb(self,category):
        return self.category_dic[category] / sum(self.category_dic.values())

    def word_prb(self,word,category):
        return self.incat_get_count(word,category) + 1 / sum(self.word_dic[category].values()) + len(self.words)

    def categorize(self,text):
        best_category = None
        max_sc =  -sys.maxsize
        words = self.split(text)
        for category in self.category_dic.keys():
            sc = self.sc(words,category)
            if sc > max_sc:
                max_sc = sc
                best_category = category
        return best_category

    def learn(self):  
        text = entry.get()
        self.train('スポーツ選手にインタビュー','スポーツ')
        self.train('スポーツ選手たちにインタビュー','スポーツ')
        self.train('インタビューを受けた○○選手','スポーツ')
        self.train('スポーツ選手である○○さんの登場','スポーツ')
        self.train('スポーツ選手たちが参加','スポーツ')
        self.train('こちらは新商品の○○です。','商品')
        self.train('新しいおすすめ商品の紹介','商品')
        self.train('あなたへのおすすめ商品','商品')
        self.train('○○商品が発売開始','商品')
        self.train('新商品はこちら','商品')
        self.train('新しくメニューに加わった料理','料理')
        self.train('野菜を使った料理','料理')
        self.train('料理の基本','料理')
        self.train('看板メニュー','料理')
        self.train('こちらのお店で楽しめる料理','料理')
        result = self.categorize(text)
        label.configure(text='「'+text+'」' + '\ncategory:'+ result)
        tex = '・「'+text+'」' + 'category:'+ result
        if result == 'スポーツ':
            with open('cate_sport.txt','a',encoding='utf-8') as a:
                a.writelines(tex+'\n')
        elif result == '商品':
            with open('cate_product.txt','a',encoding='utf-8') as a:
                a.writelines(tex+'\n')
        elif result == '料理':
            with open('cate_food.txt','a',encoding='utf-8') as a:
                a.writelines(tex+'\n')
        else:
            label.configure(text='分類できるカテゴリーがありません')

bf = BayesianFilter()

root = tk.Tk()
root.title('categorize tool')
root.geometry('850x560')
font=('メイリオ',12)

label = tk.Label(
        root,
        width = 80,
        height = 20,
        bg = 'white',
        font = font
        )
label.place(x=20,y=25)

frame = tk.Frame(root)

entry = tk.Entry(
        frame,
        width = 70,
        font = font   
    )
entry.pack(side = tk.LEFT)
entry.focus_set()

button = tk.Button(
        frame,
        width=15,
        text = 'push',
        command = bf.learn
    )
button.pack(side=tk.LEFT)
frame.place(x=30,y=520)

root.mainloop()