#!/usr/bin/env python3

import os
import sys
import shutil

TR_DIR='../src/com/lushprojects/circuitjs1/public'
LOCALE_FIELDS=['en','es','ca']
SPACER='¬'
STR_BOUND_CHR='"'
CSV_FILE=f'{TR_DIR}/circuitjs.csv'

argsize=len(sys.argv)
LOCALE_GEN=[]
for i in range(argsize):
    if sys.argv[i].lower() == "-l" and i+1<argsize:
        if sys.argv[i+1].lower() in LOCALE_FIELDS:
            LOCALE_GEN.append(sys.argv[i+1].lower())

def help():
    print('llx-gen-locale.py -l [es|ca] -l [es|ca]')
    sys.exit(0)

LOCALE_GEN=['es','ca']
if not LOCALE_GEN:
    help()

if not os.path.isfile(CSV_FILE):
    print(f'{CSV_FILE} not exists!')
    sys.exit(1)

locales={}
with open(CSV_FILE,'r') as fp:
    data=fp.readlines()
    idx_en=LOCALE_FIELDS.index('en')
    for line in data:
        if 'TRANSLATION_EN' in line:
            continue
        fields=line.split(SPACER)
        for lang in LOCALE_GEN:
            idx=LOCALE_FIELDS.index(lang)
            locales.setdefault(lang,{})
            if len(fields) > idx:
                tr_en=fields[idx_en].strip()
                tr_lang=fields[idx].strip()
                if not tr_en or not tr_lang:
                    continue
                if tr_en[0] != STR_BOUND_CHR:
                    tr_en=f'{STR_BOUND_CHR}{tr_en}'
                if tr_en[-1] != STR_BOUND_CHR:
                    tr_en=f'{tr_en}{STR_BOUND_CHR}'
                if tr_lang[0] != STR_BOUND_CHR:
                    tr_lang=f'{STR_BOUND_CHR}{tr_lang}'
                if tr_lang[-1] != STR_BOUND_CHR:
                    tr_lang=f'{tr_lang}{STR_BOUND_CHR}'
                locales[lang].setdefault(tr_en,tr_lang)
for lang in LOCALE_GEN:
    if not locales.get(lang):
        continue
    tr_file=f'{TR_DIR}/locale_{lang}.txt'
    bkp_tr_file=f'{TR_DIR}/backup-locale_{lang}.txt'
    if os.path.isfile(tr_file):
        if not os.path.isfile(bkp_tr_file):
            shutil.copy(tr_file,bkp_tr_file)
    with open(tr_file,'w') as fp:
        for k in sorted(locales[lang]):
            tr=locales[lang][k]
            fp.write(f'{k}={tr}\n')

