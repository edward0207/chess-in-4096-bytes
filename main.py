# alpha-beta+quiescence, fixed nodes, no clock/random. 0=a8..63=h1, UPPERCASE moves,
# each ply mirrors (i^56)+swapcase. Perft-verified to d5.
import json,os,urllib.request as U
E=os.environ.get("MAKEFUN_ENV_URL")
V=dict(P=100,N=305,B=333,R=500,Q=950,K=60000)
NM=(-17,-15,-10,-6,6,10,15,17)
KM=(-9,-8,-7,-1,1,7,8,9)
SL=dict(B=(-9,-7,7,9),R=(-8,-1,1,8),Q=KM)
NB=80000
n=0
D={}
def mir(s):return''.join(s[j-8:j]for j in range(64,0,-8)).swapcase()
def att(b,s):
 for D,c,g in((NM,'n',3),(KM,'k',2),((-9,-7),'p',2)):
  for d in D:
   t=s+d
   if 0<=t<64 and abs(t%8-s%8)<g and b[t]==c:return 1
 for c in'br':
  for d in SL[c.upper()]:
   t=s
   while 1:
    u=t+d
    if not 0<=u<64 or abs(u%8-t%8)>1:break
    t=u;x=b[t]
    if x!='.':
     if x==c or x=='q':return 1
     break
 return 0
def pm(i,t):return[(i,t,q)for q in'QRBN']if t<8 else[(i,t,0)]
def gen(p):
 b,c,o,ep=p
 for i,f in enumerate(b):
  if not f.isupper():continue
  if f=='P':
   t=i-8
   if t>=0 and b[t]=='.':
    yield from pm(i,t)
    if i>47 and b[i-16]=='.':yield(i,i-16,0)
   for d in(-9,-7):
    t=i+d
    if 0<=t<64 and abs(t%8-i%8)<2 and(b[t].islower()or t==ep):yield from pm(i,t)
  elif f in'NK':
   D,g=(NM,3)if f=='N'else(KM,2)
   for d in D:
    t=i+d
    if 0<=t<64 and abs(t%8-i%8)<g and not b[t].isupper():yield(i,t,0)
   if f=='K':
    if c[0]and b[61]==b[62]=='.'and not(att(b,60)or att(b,61)or att(b,62)):yield(60,62,0)
    if c[1]and b[57]==b[58]==b[59]=='.'and not(att(b,60)or att(b,59)or att(b,58)):yield(60,58,0)
  else:
   for d in SL[f]:
    t=i
    while 1:
     u=t+d
     if not 0<=u<64 or abs(u%8-t%8)>1:break
     t=u
     if b[t].isupper():break
     yield(i,t,0)
     if b[t].islower():break
def mk(p,m):
 b,c,o,ep=p;i,t,q=m;f=b[i];l=list(b);l[t]=q or f;l[i]='.';e=-1
 if f=='P':
  if t==ep:l[t+8]='.'
  if i-t==16:e=(i-8)^56
 elif f=='K':
  c=(0,0)
  if t-i==2:l[63]='.';l[61]='R'
  elif i-t==2:l[56]='.';l[59]='R'
 s=''.join(l)
 if att(s,s.index('K')):return None
 if i==63:c=(0,c[1])
 if i==56:c=(c[0],0)
 if t==7:o=(0,o[1])
 if t==0:o=(o[0],0)
 return(mir(s),o,c,e)
def ev(b):
 s=0
 for i,f in enumerate(b):
  if f=='.':continue
  u=f.upper();v=V[u];r=i//8
  if f.islower():r=7-r
  if u=='P':v+=(6-r)*7
  elif u in'NB':v+=3*(14-abs(i%8*2-7)-abs(r*2-7))
  elif u=='R'and r==1:v+=14
  elif u=='K'and r>5:v+=12
  s+=v if f.isupper()else-v
 return s
def od(b,m):return V.get(b[m[1]].upper(),0)*10-V[b[m[0]]]+900*(m[2]!=0)
def qs(p,a,B):
 global n
 n+=1;s=ev(p[0])
 if s>=B:return B
 if n>NB*2:return s
 if s>a:a=s
 for m in sorted([m for m in gen(p)if p[0][m[1]]!='.'or m[2]],key=lambda m:od(p[0],m),reverse=True):
  q=mk(p,m)
  if not q:continue
  s=-qs(q,-B,-a)
  if s>=B:return B
  if s>a:a=s
 return a
def sr(p,d,a,B):
 global n
 n+=1
 if d<1:return qs(p,a,B)
 if n>NB:return ev(p[0])
 y=0
 for m in sorted(gen(p),key=lambda m:od(p[0],m),reverse=True):
  q=mk(p,m)
  if not q:continue
  y=1;s=-sr(q,d-1,-B,-a)
  if s>=B:return B
  if s>a:a=s
 if y:return a
 b=p[0];return-99000+d if att(b,b.index('K'))else 0
def sq(s):return ord(s[0])-97+(56-ord(s[1]))*8
def fen(F):
 x=F.split();b=''
 for r in x[0].split('/'):
  for ch in r:b+='.'*int(ch)if ch.isdigit()else ch
 a=x[2];w=('K'in a,'Q'in a);k=('k'in a,'q'in a)
 ep=sq(x[3])if x[3]!='-'else-1
 if x[1]=='w':return(b,w,k,ep)
 return(mir(b),k,w,ep^56 if ep>=0 else-1)
def best(F,L):
 global n
 fl=F.split()[1]=='b';p=fen(F);n=0;L=[u for u in L if u!=D.get(p[0])]or L;bm=L[0]
 for d in range(1,7):
  cs=-10**9;cb=None
  for u in L:
   i=sq(u[:2]);t=sq(u[2:4])
   if fl:i^=56;t^=56
   q=mk(p,(i,t,u[4:].upper()or 0))
   if not q:continue
   s=-sr(q,d-1,-10**9,-cs)
   if s>cs:cs=s;cb=u
  if n>NB:break
  if cb:bm=cb
 D[p[0]]=bm
 return bm
def post(P,B):
 r=U.Request(E+P,data=json.dumps(B).encode(),headers={"content-type":"application/json"})
 with U.urlopen(r)as s:return json.load(s)
if E:
 while 1:
  g=post("/game",{})
  if g["status"]=="done":break
  D.clear()
  while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":best(g["fen"],g["legal_moves"])})
