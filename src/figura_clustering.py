"""Figura compacta del K-Means refinado, conservando las semillas originales."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_samples

R=Path(__file__).resolve().parents[1]
d=pd.read_csv(R/'data/processed/dataset_enaho_escale_2025.csv',dtype='string',encoding='utf-8-sig')
a,_=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(d,groups=d['CONGLOME_25']))
cols=['INGHOG2D_25','GASHOG2D_25','ratio_docente_ps','proporcion_publicos','locales_escolares']
x=d.iloc[a][cols].apply(pd.to_numeric)
x['desfase_anios']=pd.to_numeric(d.iloc[a]['P208A_25'])-pd.to_numeric(d.iloc[a]['EDAD_NORMATIVA'])
for c in ['INGHOG2D_25','GASHOG2D_25','locales_escolares']:x[c]=np.log1p(x[c])
z=StandardScaler().fit_transform(x)
labels=KMeans(n_clusters=2,n_init=10,random_state=42).fit_predict(z)
assert np.array_equal(np.bincount(labels),[8310,7300])
pca=PCA(n_components=2,random_state=42);xy=pca.fit_transform(z)
sample=np.random.RandomState(42).choice(len(z),size=1200,replace=False)
s=silhouette_samples(z[sample],labels[sample]);assert round(s.mean(),4)==.2681
plt.rcParams.update({'font.family':'Times New Roman','font.size':8,'axes.labelsize':8,'axes.titlesize':8,'xtick.labelsize':7,'ytick.labelsize':7,'legend.fontsize':7})
fig,ax=plt.subplots(2,1,figsize=(3.45,3.8))
for k,color in [(0,'#355c7d'),(1,'#d49b3b')]:
    m=labels==k;ax[0].scatter(xy[m,0],xy[m,1],s=.8,alpha=.45,c=color,label=f'Grupo {k}')
ax[0].set(xlabel='Componente principal 1',ylabel='Componente principal 2',title='(a) PCA  varianza explicada 63,76 %')
ax[0].legend(markerscale=5,loc='upper right');ax[0].grid(alpha=.15)
lower=10
for k,color in [(0,'#355c7d'),(1,'#d49b3b')]:
    v=np.sort(s[labels[sample]==k]);upper=lower+len(v)
    ax[1].fill_betweenx(np.arange(lower,upper),0,v,color=color,alpha=.85,label=f'Grupo {k}')
    lower=upper+10
ax[1].axvline(s.mean(),c='black',ls='--',lw=.8,label='Media 0,2681')
ax[1].set(xlabel='Coeficiente de silueta',ylabel='Observaciones de la muestra',title='(b) Silueta en 1 200 observaciones')
ax[1].legend(loc='lower right');ax[1].grid(axis='x',alpha=.15)
fig.tight_layout(pad=.5,h_pad=.7)
dest=R/'resultados/figuras/articulo';dest.mkdir(exist_ok=True)
fig.savefig(dest/'clustering.png',dpi=350)
print('Clustering compacto verificado',s.mean(),pca.explained_variance_ratio_.sum())
