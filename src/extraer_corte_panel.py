"""Regenera extractos de 2025 desde los cuatro CSV panel completos, sin sobrescribir.

Uso: python src/extraer_corte_panel.py --origen RUTA_ENAHO --destino CARPETA_NUEVA
La carpeta de origen debe contener los archivos panel o sus subcarpetas.
La codificación comprobada en estos CSV es UTF-8-SIG; se admite otra por argumento.
"""
from pathlib import Path
import argparse
import pandas as pd

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--origen',required=True,type=Path)
    p.add_argument('--destino',required=True,type=Path)
    p.add_argument('--encoding',default='utf-8-sig')
    a=p.parse_args();raiz=Path(__file__).resolve().parents[1]
    a.destino.mkdir(parents=True,exist_ok=True)
    specs=[('enaho01-2021-2025-100-panel.csv','enaho_vivienda_2025.csv','data/processed'),('enaho01-2021-2025-200-panel.csv','enaho_personas_2025.csv','data/processed'),('enaho01a-2021-2025-300-panel.csv','enaho_educacion_2025.csv','data/processed'),('sumaria-2021-2025-panel.csv','enaho_sumaria_2025.csv','data/processed'),('enaho01-2021-2025-200-panel.csv','factores_personas_2025.csv','data/raw'),('enaho01a-2021-2025-300-panel.csv','grados_educativos_2025.csv','data/raw')]
    for patron,nombre,carpeta in specs:
        archivos=list(a.origen.rglob(patron))
        if len(archivos)!=1:raise ValueError(f'Se esperaba una fuente para {patron}; encontradas {len(archivos)}')
        columnas=pd.read_csv(raiz/carpeta/nombre,nrows=0,encoding='utf-8-sig').columns.tolist()
        destino=a.destino/nombre
        if destino.exists():raise FileExistsError(destino)
        total=0;cabecera=True
        with destino.open('x',encoding='utf-8-sig',newline='') as f:
            for bloque in pd.read_csv(archivos[0],encoding=a.encoding,dtype='string',usecols=lambda c:c.strip().upper() in columnas,chunksize=25000):
                bloque.columns=bloque.columns.str.strip().str.upper()
                corte=bloque.loc[bloque['AÑO_25'].str.strip().eq('2025').fillna(False),columnas]
                corte.to_csv(f,index=False,header=cabecera);cabecera=False;total+=len(corte)
        print(nombre,total,'filas')

if __name__=='__main__':main()
