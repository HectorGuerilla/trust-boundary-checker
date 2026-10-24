#!/usr/bin/env python3
import re, sys, pathlib
CHECKS=[('Audience/job',[r'for developers',r'use case',r'problem',r'helps ',r'built for'],'Say who it is for and what job it does.'),('Trust boundary',[r'local',r'cloud',r'permission',r'token',r'credential',r'read-only',r'write access'],'Name local vs remote execution and required permissions.'),('Data handling',[r'data',r'privacy',r'log',r'retain',r'store',r'delete',r'telemetry'],'Say what is read, sent, stored, logged, retained, and deleted.'),('Setup/proof',[r'install',r'quickstart',r'example',r'screenshot',r'demo',r'expected output'],'Show a fast path to verified success.'),('Limits/failure',[r'limit',r'risk',r'fail',r'unsupported',r'false positive',r'false negative'],'List when users should not trust it.'),('Next action',[r'try',r'sign up',r'docs',r'pricing',r'issue',r'get started'],'Make the next useful action obvious.')]
def score(t):
 t=t.lower(); total=0; out=[]
 for name,pats,fix in CHECKS:
  hits=sum(1 for p in pats if re.search(p,t)); s=min(10,round(hits/max(2,min(5,len(pats)))*10)); total+=s; out.append((name,s,hits,fix))
 return round(total/(10*len(CHECKS))*100),out
if len(sys.argv)!=2:
 print('usage: python3 trust_boundary_checker.py README.md   # or - for stdin'); sys.exit(2)
text=sys.stdin.read() if sys.argv[1]=='-' else pathlib.Path(sys.argv[1]).read_text(errors='replace')
pct,rows=score(text[:30000]); print(f'Score: {pct}/100')
for name,s,h,fix in rows: print(f'- {name}: {s}/10 ({h} hits) — {fix}')
