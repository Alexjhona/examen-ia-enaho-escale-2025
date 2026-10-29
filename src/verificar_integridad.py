"""Verifica los tamaños y SHA-256 del manifiesto final, sin ejecutar modelos."""
from pathlib import Path
import hashlib,json,sys

def main():
    raiz=Path(__file__).resolve().parents[1]
    items=json.loads((raiz/'auditoria/manifest_sha256.json').read_text(encoding='utf-8'))
    errores=[]
    for nombre,info in items.items():
        p=raiz/nombre
        if not p.is_file():errores.append(nombre+': ausente');continue
        h=hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
        if p.stat().st_size!=info['bytes'] or h!=info['sha256']:errores.append(nombre+': cambió')
    print('Archivos comprobados:',len(items))
    print('\n'.join(errores) if errores else 'Integridad correcta')
    return 1 if errores else 0

if __name__=='__main__':sys.exit(main())
