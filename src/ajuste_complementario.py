"""Sensibilidad acotada de hiperparámetros sobre entrenamiento, sin consultar prueba."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, GroupKFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import f1_score, roc_auc_score
from xgboost import XGBClassifier

def ejecutar(raiz=None):
    raiz=Path(raiz) if raiz else Path(__file__).resolve().parents[1]
    datos=pd.read_csv(raiz/'data/processed/dataset_enaho_escale_2025.csv',encoding='utf-8-sig',dtype='string')
    cat=['P207_25','P300A_25','P1121_25','P1144_25','POBREZA_25','DOMINIO_25']
    num=['INGHOG2D_25','GASHOG2D_25','ratio_docente_ps','proporcion_publicos','locales_escolares']
    X=datos[cat+num].copy();y=datos['REZAGO_ESCOLAR'].astype(int)
    for c in num:X[c]=pd.to_numeric(X[c],errors='coerce')
    for c in cat:
        X[c]=X[c].str.strip().replace('',pd.NA).astype(object)
        X[c]=X[c].where(pd.notna(X[c]),np.nan)
    grupos=datos['CONGLOME_25'].astype(str)
    ent,_=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(X,y,groups=grupos))
    X=X.iloc[ent].copy();y=y.iloc[ent].copy();grupos=grupos.iloc[ent]
    folds=list(GroupKFold(n_splits=3).split(X,y,groups=grupos))
    filas=[]
    for profundidad in [3,4]:
        for arboles in [100,150]:
            f1=[];roc=[]
            for a,b in folds:
                assert set(grupos.iloc[a]).isdisjoint(set(grupos.iloc[b]))
                prep=ColumnTransformer([
                    ('numericas',Pipeline([('imputador',SimpleImputer(strategy='median')),('escalador',StandardScaler())]),num),
                    ('categoricas',Pipeline([('imputador',SimpleImputer(strategy='most_frequent')),('codificador',OneHotEncoder(handle_unknown='ignore'))]),cat)])
                peso=float(y.iloc[a].eq(0).sum()/y.iloc[a].eq(1).sum())
                modelo=Pipeline([('preprocesamiento',prep),('clasificador',XGBClassifier(
                    n_estimators=arboles,max_depth=profundidad,learning_rate=.05,subsample=.8,
                    colsample_bytree=.8,scale_pos_weight=peso,objective='binary:logistic',
                    eval_metric='logloss',tree_method='hist',random_state=42,n_jobs=4))])
                modelo.fit(X.iloc[a],y.iloc[a])
                f1.append(f1_score(y.iloc[b],modelo.predict(X.iloc[b]),zero_division=0))
                roc.append(roc_auc_score(y.iloc[b],modelo.predict_proba(X.iloc[b])[:,1]))
            filas.append({'max_depth':profundidad,'n_estimators':arboles,'F1_rezago_CV':np.mean(f1),
                          'DE_F1_rezago_CV':np.std(f1,ddof=1),'ROC_AUC_CV':np.mean(roc)})
    tabla=pd.DataFrame(filas)
    destino=raiz/'resultados/complementarios';destino.mkdir(exist_ok=True)
    tabla.to_csv(destino/'ajuste_hiperparametros.csv',index=False,encoding='utf-8-sig')
    return tabla

if __name__=='__main__':
    print(ejecutar().round(6).to_string(index=False))
