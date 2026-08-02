#!/usr/bin/env python3
from __future__ import annotations
import http.client, os, sqlite3, subprocess, sys, tempfile, time
from pathlib import Path

BASE = Path(__file__).resolve().parent

def request(path, cookie=None):
    conn=http.client.HTTPConnection('127.0.0.1', 8765, timeout=5)
    headers={'Cookie':cookie} if cookie else {}
    conn.request('GET', path, headers=headers)
    r=conn.getresponse(); body=r.read().decode('utf-8','replace'); headers=dict(r.getheaders()); conn.close()
    return r.status, headers, body

def main():
    with tempfile.TemporaryDirectory() as tmp:
        env=os.environ.copy(); env.update({'HOST':'127.0.0.1','PORT':'8765','DATABASE_PATH':str(Path(tmp)/'nav.sqlite3')})
        p=subprocess.Popen([sys.executable, str(BASE/'server.py')], cwd=BASE, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        try:
            for _ in range(50):
                try:
                    if request('/health')[0]==200: break
                except OSError: time.sleep(.1)
            else: raise RuntimeError('server did not start')
            checks=[('/',200),('/connexion',200),('/inscription',200),('/administration',200),('/tableau-de-bord',303),('/espace-apprenant',401),('/espace-apprenant/sequence-1',303),('/route-inconnue',404)]
            for path, expected in checks:
                status, headers, body=request(path)
                assert status==expected, (path,status,expected)
                if path=='/espace-apprenant/sequence-1':
                    assert headers.get('Location')=='/espace-apprenant/sequence-1/accueil'
            print('Navigation check: OK')
        finally:
            p.terminate(); p.wait(timeout=5)
if __name__=='__main__': main()
