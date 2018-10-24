#Created by Shoko Sano at 2018/08
#航空宇宙システムpython
#単語リンク度ランキングプログラム-確率行列ver.-

# coding: utf-8
import codecs
import numpy as np


def wordic():
    w=0 #入力単語の数カウント
    f1=codecs.open('words.txt','r')
    pages={}#ページ番号と単語のリンクを辞書に
    page_list=[]#単語が格納される順のリスト
    for line in f1:
        w+=1
        page,word=line.strip().split('\t')
        pages.update({int(page):word})
        page_list.append(int(page))
    return pages,w,page_list

def link_matrix(P,pages):
    f2=codecs.open('links.txt','r')
    for link in f2:
        i,j=map(int,link.strip().split('\t'))
        if i in pages.keys():
            P[j][i]=1  #page間のリンクを隣接行列に   #i→jへ移動する確率
            n=len(P)
    for i in range(n):
        if sum(P[:,i])>0: #link exists? →yes probability=(1/the number of links)
            for j in range(n):
                if P[j][i]==1:
                    P[j][i]=1/sum(P[:,i])
    return P


#page間のリンクを確率隣接行列Mを用いて求める
def calculate_pagerank(P,n):
    rate=0.95
    A=np.ones((n,n))
    A=(1-rate)*(1/n)*A
    M=rate*P+A
    M.tolist()
    #X=MXとなるX
    X=np.ones((n,1))  #rink度初期設定
    #Xn+1=MXn
    steps=10 #times for calcilation:changeable
    k=0
    while k in range(steps):
        X_next=np.dot(M, X)
        X=X_next
        k+=1
    return X_next


def main():
    #{page:word}対応の辞書,wordの数,fileのpage順を保存するリスト(最後のランキングの際にpagerankとwordを適合させるため)
    pages,w,page_list=wordic()
    #行列サイズは単語のサイズw
    matrixP=np.zeros((w,w),dtype=float)
    #確率行列X生成
    nP=link_matrix(matrixP,pages)
    X=calculate_pagerank(nP,w)
    X=X.tolist()

    #pagerank＿top5 output
    print('==linksrank.TOP5==')
    pagerank={}#各単語とそのlink度を辞書に
    for data in range(len(X)):
        #Xにはpage_listに格納された順に単語のリンク度が計算されているので、それらを結びつける
        word,ranknum=pages[page_list[data]],X[data] #ranknumはlink度をを数値として計算した結果
        pagerank.update({word:0})
        pagerank[word]=ranknum
    pagerank = sorted(pagerank.items(), key=lambda x: x[1],reverse=True)#ranknumでsort
    pagerank=list(pagerank)
    i=1
    for num in range(5):#ranking表示数は変えられる
        print(str(i)+'位',pagerank[num][0],':'+str(round(pagerank[num][1][0],5)))
        i+=1

if __name__=='__main__':
    main()








