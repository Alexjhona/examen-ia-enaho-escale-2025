from pathlib import Path
import json,numpy as np,pandas as pd,joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import roc_curve,precision_recall_curve,confusion_matrix
from sklearn.calibration import calibration_curve
import shap,xgboost as xgb
from scipy.special import expit
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT
FIG=OUT/'resultados/figuras/articulo';FIG.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'Times New Roman','font.size':8,'axes.titlesize':8,'axes.labelsize':8,'xtick.labelsize':7,'ytick.labelsize':7,'legend.fontsize':7,'savefig.dpi':350})
d=pd.read_csv(OUT/'data/processed/dataset_enaho_escale_2025.csv',dtype='string',encoding='utf-8-sig')
cat=['P207_25','P300A_25','P1121_25','P1144_25','POBREZA_25','DOMINIO_25'];num=['INGHOG2D_25','GASHOG2D_25','ratio_docente_ps','proporcion_publicos','locales_escolares']
X=d[cat+num].copy();y=d['REZAGO_ESCOLAR'].astype(int);groups=d['CONGLOME_25']
for c in num:X[c]=pd.to_numeric(X[c],errors='coerce')
for c in cat:X[c]=X[c].astype(object).where(X[c].notna(),np.nan)
a,b=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(X,y,groups=groups))
model=joblib.load(OUT/'resultados/modelos/xgboost_balanceado_final.joblib')
p=model.predict_proba(X.iloc[b])[:,1];pred=model.predict(X.iloc[b]);yt=y.iloc[b]

f,axs=plt.subplots(2,1,figsize=(3.45,3.5));rocx,rocy,_=roc_curve(yt,p);pr,re,_=precision_recall_curve(yt,p)
axs[0].plot(rocx,rocy,label='XGBoost  AUC 0.6250',color='#1f4e79');axs[0].plot([0,1],[0,1],'--',color='.6');axs[0].set(xlabel='Tasa de falsos positivos',ylabel='Sensibilidad');axs[0].legend(loc='lower right');axs[0].set_title('(a) Curva ROC')
axs[1].plot(re,pr,color='#1f4e79',label='AP 0.0921; PR-AUC 0.0898');axs[1].axhline(yt.mean(),ls='--',c='.6');axs[1].set(xlabel='Recall de rezago',ylabel='Precisión',ylim=(0,1));axs[1].legend();axs[1].set_title('(b) Curva Precision–Recall')
for ax in axs:ax.grid(alpha=.2)
f.tight_layout();f.savefig(FIG/'roc_pr.png');plt.close(f)
f,axs=plt.subplots(2,1,figsize=(3.45,3.7));m=confusion_matrix(yt,pred,labels=[0,1]);axs[0].imshow(m,cmap='Blues')
for i in range(2):
 for j in range(2):axs[0].text(j,i,str(m[i,j]),ha='center',va='center',color='white' if m[i,j]>m.max()/2 else 'black',fontsize=10)
axs[0].set(xticks=[0,1],yticks=[0,1],xticklabels=['Sin rezago','Con rezago'],yticklabels=['Sin rezago','Con rezago'],xlabel='Clase predicha',ylabel='Clase real');axs[0].set_title('(a) Matriz de confusión')
frac,mean=calibration_curve(yt,p,n_bins=10,strategy='quantile');axs[1].plot(mean,frac,'o-',c='#1f4e79');axs[1].plot([0,1],[0,1],'--',c='.6');axs[1].set(xlabel='Probabilidad media predicha',ylabel='Frecuencia observada',xlim=(0,1),ylim=(0,1));axs[1].set_title('(b) Calibración  Brier 0.1890');axs[1].grid(alpha=.2)
f.tight_layout();f.savefig(FIG/'errores_calibracion.png');plt.close(f)

eda=pd.read_csv(OUT/'resultados/tablas/eda_pobreza_rezago.csv');f,ax=plt.subplots(figsize=(3.45,1.9));ax.bar(['Extrema','No extrema','No pobre'],eda['Tasa_rezago'],color=['#4f5d75','#829ab1','#b8c7d1']);ax.set(xlabel='Condición de pobreza',ylabel='Rezago en entrenamiento (%)');ax.grid(axis='y',alpha=.2);f.tight_layout();f.savefig(FIG/'eda_pobreza.png');plt.close(f)

sample=np.random.default_rng(42).choice(len(a),size=300,replace=False);xs=X.iloc[a].iloc[sample]
prep=model.named_steps['preprocesamiento'];xm=prep.transform(xs);names=list(prep.get_feature_names_out());contr=model.named_steps['clasificador'].get_booster().predict(xgb.DMatrix(xm),pred_contribs=True)
vals=xm.toarray() if hasattr(xm,'toarray') else np.asarray(xm)
aliases={'numericas__ratio_docente_ps':'Alumnos/docente','numericas__proporcion_publicos':'Proporción pública','numericas__GASHOG2D_25':'Gasto del hogar','numericas__INGHOG2D_25':'Ingreso del hogar','numericas__locales_escolares':'Locales escolares','categoricas__POBREZA_25_3':'No pobre','categoricas__DOMINIO_25_6':'Sierra sur','categoricas__DOMINIO_25_5':'Sierra centro','categoricas__P207_25_1':'Sexo masculino','categoricas__P300A_25_4':'Castellano'}
labels=[aliases.get(s,s.replace('categoricas__','').replace('numericas__','')) for s in names]
ex=shap.Explanation(values=contr[:,:-1],base_values=contr[:,-1],data=vals,feature_names=labels)
shap.plots.beeswarm(ex,max_display=11,show=False,plot_size=(3.45,3.3),s=6)
for ax in plt.gcf().axes:
 ax.tick_params(labelsize=7);ax.xaxis.label.set_size(8);ax.yaxis.label.set_size(8)
plt.gca().set_xlabel('Contribución SHAP  log-odds',fontsize=8);plt.gcf().subplots_adjust(left=.40,right=.92,bottom=.15,top=.98);plt.savefig(FIG/'shap_global.png',bbox_inches='tight');plt.close('all')
ix=[names.index('numericas__ratio_docente_ps'),names.index('numericas__proporcion_publicos')]
f,axs=plt.subplots(2,1,figsize=(3.45,3.25))
for ax,j,k,lab in [(axs[0],ix[0],ix[1],'Alumnos por docente'),(axs[1],ix[1],ix[0],'Proporción de servicios públicos')]:
 field=num[j];colorfield=num[k]
 pts=ax.scatter(pd.to_numeric(xs[field]),contr[:,j],c=pd.to_numeric(xs[colorfield]),s=8,cmap='coolwarm',alpha=.7)
 ax.set(xlabel=lab,ylabel='SHAP  log-odds');ax.axhline(0,color='.5',ls='--',lw=.6);ax.grid(alpha=.15)
 cb=f.colorbar(pts,ax=ax,pad=.02);cb.ax.tick_params(labelsize=6);cb.set_label('Pública' if k==ix[1] else 'Alumnos/docente',fontsize=7)
f.tight_layout();f.savefig(FIG/'shap_dependencias.png');plt.close(f)
real=yt.to_numpy();tp=np.flatnonzero((real==1)&(pred==1));tn=np.flatnonzero((real==0)&(pred==0));cases=[tp[np.argmax(p[tp])],tn[np.argmin(p[tn])]]
xcase=prep.transform(X.iloc[b].iloc[cases]);cc=model.named_steps['clasificador'].get_booster().predict(xgb.DMatrix(xcase),pred_contribs=True);vcase=xcase.toarray() if hasattr(xcase,'toarray') else np.asarray(xcase)
for i,label in enumerate(['positivo','negativo']):
 e=shap.Explanation(values=cc[i,:-1],base_values=cc[i,-1],data=vcase[i],feature_names=labels)
 shap.plots.waterfall(e,max_display=6,show=False)
 f=plt.gcf();f.set_size_inches(3.45,2.3)
 for ax in f.axes:
  ax.tick_params(labelsize=6.5)
  for t in ax.texts:t.set_fontsize(7)
  for t in ax.get_yticklabels()+ax.get_xticklabels():t.set_fontsize(7)
 plt.title(('Verdadero positivo' if i==0 else 'Verdadero negativo')+f'  p = {p[cases[i]]:.4f}',fontsize=8)
 f.tight_layout();f.savefig(FIG/f'waterfall_{label}.png',bbox_inches='tight');plt.close('all')
print('FIGURAS_ARTICULO',FIG,flush=True)

# Regenerar también el panel de clustering con ejes legibles.
import runpy
runpy.run_path(str(ROOT / "src/figura_clustering.py"),run_name="__main__")
