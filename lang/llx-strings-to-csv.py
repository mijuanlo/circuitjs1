#!/usr/bin/env python3

import os
import subprocess

GET_STRINGS_BIN='./getstrings.py'
TR_DIR='../src/com/lushprojects/circuitjs1/public'
LOCALES=['en','es','ca']
SPACER='¬'
STR_BOUND_CHR='"'
CSV_FILE=f'{TR_DIR}/circuitjs.csv'

keys=subprocess.check_output(f'python {GET_STRINGS_BIN}',shell=True).decode('utf8').split('\n')
all_strings={k:{'es':'','ca':''} for k in map(lambda x: str.strip(x,'"'),keys)}

def fn_filter(x):
    if not x:
        return False
    if x == '=':
        return False
    return True

for lang in ['es','ca']:
    lang_file=f'{TR_DIR}/locale_{lang}.txt'
    if os.path.isfile(lang_file):
        with open(lang_file,'r') as fp:
            for line in fp.readlines():
                en,l=filter(fn_filter,line.strip().split('"'))
                try:
                    all_strings[en][lang]=l
                except:
                    pass

if os.path.isfile(CSV_FILE):
    with open(CSV_FILE,'r') as fp:
        for line in fp.readlines():
            if 'TRANSLATION_EN' in line:
                continue
            en,es,ca=map(lambda x: str.strip(x,'"'),line.strip().split('¬'))
            if en not in all_strings:
                continue
            if es:
                all_strings[en]['es']=es
            if ca:
                all_strings[en]['ca']=ca


print(f'{STR_BOUND_CHR}TRANSLATION_EN{STR_BOUND_CHR}{SPACER}{STR_BOUND_CHR}TRANSLATION_ES{STR_BOUND_CHR}{SPACER}{STR_BOUND_CHR}TRANSLATION_CA{STR_BOUND_CHR}')
for en in sorted(all_strings.keys()):
    if not en:
        continue
    es=all_strings[en]['es']
    ca=all_strings[en]['ca']
    if es and es[0] == ' ' and en[0] != ' ':
        es=es.lstrip()
    if es and es[-1] == ' ' and en[-1] != ' ':
        es=es.rstrip()
    if ca and ca[0] == ' ' and en[0] != ' ':
        ca=ca.lstrip()
    if ca and ca[-1] == ' ' and en[-1] != ' ':
        ca=ca.rstrip()
    print(f'{STR_BOUND_CHR}{en}{STR_BOUND_CHR}{SPACER}{STR_BOUND_CHR}{es}{STR_BOUND_CHR}{SPACER}{STR_BOUND_CHR}{ca}{STR_BOUND_CHR}')
