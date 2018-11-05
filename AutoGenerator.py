# -*- coding: UTF-8 -*-

import re
import os
import pandas as pd

SourceDir = r'.\v6.3.11_20180109_tradeapi64_windows'
HMDFile = 'ThostFtdcMdApi.h'
HTDFile = 'ThostFtdcTraderApi.h'
HDTFile = 'ThostFtdcUserApiDataType.h'
HSFile = 'ThostFtdcUserApiStruct.h'

def GenerateDataTypeDF(kfile):
    k = 0
    j = 0
    klist = list()
    with open(kfile, 'r', encoding='gb18030') as kf:
        for kline in kf:
            if k > 11:
                kline = kline.strip()
                if re.match(r'\/+$',kline):
                    j=(j+1)%2
                    continue
                if j==1:
                    aexp=re.sub(r'/','', kline)
                    continue
                if re.match(r'///', kline):
                    bexp=re.sub(r'/','',kline)
                elif re.match(r'typedef', kline):
                    ksp = re.sub(r';','',kline).split(' ')
                    klist.append([
                        'typedef',
                        ksp[1],
                        ksp[2].split('[')[0],
                        1 if len(ksp[2].split('['))==1 else int(re.sub(r']','',ksp[2].split('[')[1])),
                        aexp,
                        '',
                    ])
                elif re.match(r'#define', kline):
                    ksp = kline.split(' ')
                    klist.append([
                        'define',
                        'char' if len(ksp[2])==3 else 'string',
                        ksp[1],
                        str(ksp[2]),
                        aexp,
                        bexp,
                    ])
            k+=1
    return pd.DataFrame(klist)


def GenerateStructDF(kfile):
    klist=list()
    k=0
    j=0
    with open(kfile, 'r', encoding='gb18030') as kf:
        for kline in kf:
            if k > 17:
                kline = kline.strip('\r\n\t ')
                if re.match(r'{|}', kline):
                    j=(j+1)%2
                    continue
                if re.match(r'///', kline):
                    if j==0:
                        aexp=re.sub(r'/', '', kline)
                        continue
                    else:
                        bexp=re.sub(r'/', '', kline)
                        continue
                elif re.match(r'struct', kline):
                    cstruct=kline.split(' ')[1]
                elif re.match(r'[a-zA-Z]', kline):
                    ksp = re.sub(r'\t', ' ', re.sub(r';', '', kline)).split(' ')
                    klist.append([
                        cstruct,
                        ksp[0],
                        ksp[1],
                        aexp,
                        bexp,
                    ])
            k+=1
    return pd.DataFrame(klist)



