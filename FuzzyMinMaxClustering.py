def f(x,v):
    if x*v>1:return 1
    elif 0<=x*v<=1: return x*v
    else: return 0
def HMF(Ah,h):
    mh=[]#-1
    if len(h)!=0:
        for j in range(len(h)):
            Vj=h[j][0]
            Wj=h[j][1]
            v=1   #Sensitivity Parameter
            n=len(Ah)
            op=0
            for i in range(n):
                op=op+1-f(Ah[i]-Wj[i],v)-f(Vj[i]-Ah[i],v)
            a=op*1/float(n)
            mh.append([a,j])
        mh=sorted(mh,key=lambda x: (x[0],x[1]),reverse=True)
    return mh
####### Data input ############
import numpy as np
x=np.genfromtxt('irisNormal.csv',delimiter=',')
d=x[:,-1].tolist()
x=x[:,:-1].tolist()
th=0.20  #theta for putthing bounds on hyperboxes
n=len(x[0])
fir=1
############ Training Starts ##############
for i in x:
    if fir==1:#true if first input
        H=[[i,i]]
        fir=0
    else:
        hii=HMF(i,H)
        if hii!=[]:
            var=0
            for hx in hii:
                hi=hx[1]
                he=H[hi]
                s=0
###########          Expansion        ################                
                for k in range(n):
                    s=s+max(he[1][k],i[k])-min(he[0][k],i[k])
                if n*th >= s:
                    var=1
                    p=[]
                    q=[]
                    for k in range(n):
                        p.append(min(H[hi][0][k],i[k]))
                        q.append(max(H[hi][1][k],i[k]))
                    H[hi][0]=p
                    H[hi][1]=q
    #############         Overlap        ###############
                    for z in range(len(H)):
                        h=H[z]
                        shu=0
                        for dim in range(n):
                            ##### Case1 #####
                            Vji=p[dim]
                            Vki=h[0][dim]
                            Wji=q[dim]
                            Wki=h[1][dim]
                            if Vji<Vki<Wji<Wki:
                                shu=shu+1
                            elif Vki<Vji<Wki<Wji:
                                shu=shu+1
                            elif Vji<Vki<=Wki<Wji:
                                shu=shu+1
                            elif Vki<Vji<=Wji<Wki:
                                shu=shu+1
                        if shu==n:
     #############         Contraction      ##############
                            for delta in range(n):
                                Vji=p[delta]
                                Vki=h[0][delta]
                                Wji=q[delta]
                                Wki=h[1][delta]
                                gf=0
                                if Vji<Vki<Wji<Wki:
                                    Vki=Wji=(Vki+Wji)/2
                                    gf=1
                                elif Vki<Vji<Wki<Wji:
                                    gf=1
                                    Vji=Wki=(Vji+Wki)/2
                                elif Vji<Vki<=Wki<Wji:
                                    gf=1
                                    if((Wki-Vji)>(Wji-Vki)):
                                        Wji=Vki
                                    elif((Wki-Vji)<(Wji-Vki)):
                                        Vji=Wki
                                elif Vki<Vji<=Wji<Wki:
                                    gf=1
                                    if((Wji-Vki)>(Wki-Vji)):
                                        Wki=Vji
                                    elif((Wji-Vki)<(Wki-Vji)):
                                        Vki=Wji
                                H[hi][0][delta]=Vji
                                H[z][0][delta]=Vki
                                H[hi][1][delta]=Wji
                                H[z][1][delta]=Wki
                    break;
            if var==0:
                H.append([i,i])
        else:
            H.append([i,i])
print("\nHyperBoxes:-")
print(H)
print("\nTotal number of Hyperboxes: "+str(len(H)))
cla=[[0,0,0] for i in range(len(H))] 
for i in range(len(x)):
    hii=HMF(x[i],H)
    cc=hii[0][1]
#    if hii[0][0]==1:
    cla[cc][int(d[i])-1]=cla[cc][int(d[i])-1]+1
#print(cla)
H_labels=[]
for i in cla:
    maxi=0
    for j in range(len(i)):
        if i[maxi]<i[j]:
            maxi=j
    H_labels.append(maxi+1)
#print(H_labels)
confusion_matrix=[[0,0,0],[0,0,0],[0,0,0]]
for i in range(1,4):
    for j in range(len(H_labels)):
        if i==H_labels[j]:
            confusion_matrix[i-1]=[(r+e) for r,e in zip(confusion_matrix[i-1],cla[:][j])]
    confusion_matrix[i-1]=[e*2 for e in confusion_matrix[i-1]]
confusion_matrix=np.array(confusion_matrix).T.tolist()
print("\nConfusion Matrix")
print(confusion_matrix)           
            


