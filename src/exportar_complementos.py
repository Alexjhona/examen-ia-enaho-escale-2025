"""Exporta los complementos ya definidos en el notebook sin reentrenar modelos."""
from pathlib import Path
from zipfile import ZipFile
import nbformat
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

def ejecutar():
    raiz=Path(__file__).resolve().parents[1]
    inter=raiz/'data/interim';inter.mkdir(exist_ok=True)
    for archivo in ['00_Padron.zip','00_Padlocal.zip']:
        with ZipFile(raiz/'data/raw'/archivo) as z:
            for info in z.infolist():
                if info.filename.lower().endswith('.dbf'):
                    destino=inter/Path(info.filename).name
                    if not destino.exists():
                        with z.open(info) as entrada,destino.open('xb') as salida:
                            import shutil
                            shutil.copyfileobj(entrada,salida)
    df=pd.read_csv(raiz/'data/processed/dataset_enaho_escale_2025.csv',dtype='string',encoding='utf-8-sig')
    train,_=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=42).split(df,groups=df['CONGLOME_25']))
    scope={'raiz':raiz,'df_modelo':df,'train_idx':train,'display':lambda *args:None}
    nb=nbformat.read(raiz/'notebooks/AnalisisExamen_Final.ipynb',as_version=4)
    for marker in ['DESCRIPCIÓN COMPLEMENTARIA CON FACTOR ANUAL DE PERSONAS','ESCALE COMPLEMENTARIO POR DISTRITO Y ÁREA URBANA/RURAL']:
        cells=[c for c in nb.cells if c.cell_type=='code' and marker in c.source]
        assert len(cells)==1,marker
        exec(compile(cells[0].source,'<complemento notebook>','exec'),scope)
    out=raiz/'resultados/complementarios';out.mkdir(exist_ok=True)
    for variable,nombre in [('resumen_factor','control_factor_personas'),('tabla_descriptiva_ponderada','descripcion_facpob07'),('tabla_cobertura_area','cobertura_escale_area'),('escale_distrito_area_complementario','escale_distrito_area')]:
        scope[variable].to_csv(out/(nombre+'.csv'),index=False,encoding='utf-8-sig')
    scope['modelo_area_complementario'].to_csv(raiz/'data/processed/dataset_enaho_escale_2025_area.csv',index=False,encoding='utf-8-sig')
    assert len(scope['modelo_area_complementario'])==19490
    assert scope['modelo_area_complementario']['_cruce_escale_area'].eq('left_only').sum()==377
    print('Complementos exportados. No se modificó el dataset ni el modelo de referencia.')

if __name__=='__main__':ejecutar()
