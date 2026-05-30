import os,glob,re
ROOT="."
CITYMAP={"bradenton":"Bradenton","sarasota":"Sarasota","lakewood-ranch":"Lakewood Ranch",
"palmetto":"Palmetto","parrish":"Parrish","venice":"Venice","tampa":"Tampa","st-petersburg":"St. Petersburg"}
MULTI=["st-petersburg","lakewood-ranch","bradenton","sarasota","palmetto","parrish","venice","tampa"]

AGG=', "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "6", "bestRating": "5"}'

def detect_city(rel):
    parts=rel.replace("\\","/").lower().split("/")
    for p in parts:
        if p in CITYMAP: return p
    folder=parts[-2] if parts[-1]=="index.html" and len(parts)>=2 else parts[-1].replace(".html","")
    for s in MULTI:
        if folder.endswith(s) or folder.endswith(s+"-2026"): return s
    return None

stats={"geo":0,"vis13":0,"visSix":0,"vis6home":0,"aggRemoved":0,"homeSchema":0,"files":0}
log=[]
for f in glob.glob("**/*.html",recursive=True):
    rel=os.path.relpath(f,ROOT)
    s=open(f,encoding="utf-8").read()
    o=s; ch=[]
    # 1) visible review text -> 20
    n=s.count("13 verified Google reviews");  s=s.replace("13 verified Google reviews","20 verified Google reviews");  stats["vis13"]+=n;  ch+=["vis13:%d"%n] if n else []
    n=s.count("Six verified Google reviews"); s=s.replace("Six verified Google reviews","20 verified Google reviews"); stats["visSix"]+=n; ch+=["visSix:%d"%n] if n else []
    n=s.count("· 6 Google Reviews");      s=s.replace("· 6 Google Reviews","· 20 Google Reviews");        stats["vis6home"]+=n; ch+=["vis6home:%d"%n] if n else []
    # 2) homepage schema 13->20 ; other pages remove agg block
    if rel.replace("\\","/")=="index.html":
        n=s.count('"reviewCount":"13"'); s=s.replace('"reviewCount":"13"','"reviewCount":"20"'); stats["homeSchema"]+=n; ch+=["homeSchema:%d"%n] if n else []
    else:
        n=s.count(AGG); s=s.replace(AGG,""); stats["aggRemoved"]+=n; ch+=["aggRem:%d"%n] if n else []
    # 3) geo.placename per city
    city=detect_city(rel)
    if city and CITYMAP[city]!="Palmetto":
        target='geo.placename" content="%s, Florida"'%CITYMAP[city]
        cur='geo.placename" content="Palmetto, Florida"'
        if cur in s:
            s=s.replace(cur,target); stats["geo"]+=1; ch+=["geo->%s"%CITYMAP[city]]
    if s!=o:
        open(f,"w",encoding="utf-8").write(s); stats["files"]+=1
        log.append("%-58s %s"%(rel,", ".join(ch)))

print("STATS:",stats)
print("\n--- amostra de mudancas (primeiras 25) ---")
for l in log[:25]: print(l)
# leftovers check
import subprocess
