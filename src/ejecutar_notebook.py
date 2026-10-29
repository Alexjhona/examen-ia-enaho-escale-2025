"""Ejecuta todo el notebook en un kernel nuevo del Python que invoca este script."""
from pathlib import Path
from tempfile import TemporaryDirectory
import argparse,json,os,sys,time,traceback
import nbformat
from nbclient import NotebookClient

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeout',type=int,default=600,help='Segundos máximos por celda')
    args=parser.parse_args()
    raiz=Path(__file__).resolve().parents[1]
    salida=raiz/'resultados/reproducido';salida.mkdir(parents=True,exist_ok=True)
    nb=nbformat.read(raiz/'notebooks/AnalisisExamen_Final.ipynb',as_version=4)
    nbformat.validate(nb)
    # Se descartan las salidas previas antes de ejecutar; no hay estado residual.
    for c in nb.cells:
        if c.cell_type=='code':c.outputs=[];c.execution_count=None
    inicio=time.time();eventos=[]
    estado={'success':False,'python':sys.version,'cells':len(nb.cells),'started':time.strftime('%Y-%m-%dT%H:%M:%S')}
    def registrar(cell,cell_index,**kwargs):
        if cell.cell_type=='code':
            eventos.append({'celda':cell_index+1,'ejecucion':cell.execution_count})
            print('Celda',cell_index+1,'completada',flush=True)
    try:
        with TemporaryDirectory(prefix='ia_kernel_') as temporal:
            base=Path(temporal);kernel=base/'kernels/ia_entrega';kernel.mkdir(parents=True)
            (kernel/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'IA Entrega','language':'python'}),encoding='utf-8')
            os.environ['JUPYTER_PATH']=str(base)+os.pathsep+os.environ.get('JUPYTER_PATH','')
            os.environ['IA_PROJECT_ROOT']=str(raiz)
            os.environ.setdefault('OMP_NUM_THREADS','4');os.environ.setdefault('MKL_NUM_THREADS','4')
            NotebookClient(nb,timeout=args.timeout,kernel_name='ia_entrega',resources={'metadata':{'path':str(raiz)}},on_cell_executed=registrar,allow_errors=False).execute()
        estado['success']=True
    except Exception as error:
        estado['error']=str(error);traceback.print_exc()
    finally:
        estado['elapsed_seconds']=round(time.time()-inicio,2);estado['eventos']=eventos
        nbformat.write(nb,salida/'AnalisisExamen_Ejecutado.ipynb')
        (salida/'registro_ejecucion.json').write_text(json.dumps(estado,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Ejecución completa:',estado['success'],'segundos:',estado['elapsed_seconds'])
    return 0 if estado['success'] else 1

if __name__=='__main__':sys.exit(main())
