#Created by Shoko Sano at 2018/08
#航空宇宙システムpython
#単語リンク度ランキングプログラム-Point分配ver.-

# coding: utf-8
import codecs
import numpy as np

def wordic():
    f1=codecs.open('words.txt','r')
    w=0 #入力単語の数カウント
    #page番号と対応するwordを辞書に
    pages={}
    for line in f1:
        w+=1
        page,word=line.strip().split('\t')
        pages.update({int(page):word})
    return pages,w

#==========pageのリンク度を確率ではなく数値の大小として評価==================================================================================================================================

def links():
    f2=codecs.open('links.txt','r')
    link={}
    k=0
    for line in f2:
        i,j=map(int,line.strip().split('\t')) #iはcurrentpage番号, jはnextpage番号
        if i in link.keys():
            link[i].append(j)
        else:
            link.update({int(i):[j]})
    return link  #[{0:[3,5,4]},{2:[4,6,7,8]},{3:[1,5,7]},,,,,,]辞書のkeyがcurrentpage,valueがlinkもつnextpages

def calculate_connects(links,wordic,point):
    #次のリンク先へのポイントを渡す割合：changeable
    rate=0.6
    word=len(wordic)
    steps=20#リンク度を計算する回数：changeable
    for k in range(steps):
        n_point={}
        #Initiarize n_point:
        for i in wordic.keys():
            n_point.update({i:0})
        #Distibute points
        for i in wordic.keys():
            if i in links.keys():#linkをもつ場合
                for each in wordic.keys():
                    n_point[each]+=(1-rate)*point[i]/word#(1-rate)%はそのpage自身も含めて全部のpageにリンク度を分配
                for j in links[i]:
                    n_point[j]+=rate*point[i]/len(links[i])#rate＊point[i]をリンクあるpageのみに平等に分配
            else:#リンクをもたない場合
                for each in wordic.keys():
                    n_point[each]+=point[i]/word
        point=n_point
        #print(sum(point.values()))
    return point
#===============================================================

def main():
    linked=links()
    #リンク度ランキングしらべたい単語のfile, read 'words.txt'
    pages,w=wordic()
    point={}  #point{key:page/value:point depending on the links}
    #Initialpoint=1 for all pages
    for i in pages.keys():
        point.update({i:1})
    pagerank=calculate_connects(linked,pages,point)

#pagerank＿top5output
    print('==linksrank.TOP5==')
    ranklist = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
    i=1
    for num in range(5):
        print(str(i)+'位',pages[ranklist[num][0]],':'+str(round(ranklist[num][1],3)))
        i+=1

if __name__=='__main__':
    main()


