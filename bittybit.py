import argparse
import base64
import re
import os
import mimetypes

parser = argparse.ArgumentParser(prog='Bittybit',description='Extracting content from .bit file used in the Bitty Engine.')
parser.add_argument('filename',nargs='?',default='data.bit',help='.bit file')
parser.add_argument('destination',nargs='?',default='.',help='destination of extracted file')
args = parser.parse_args()

# mode [h]ead [d]ata
mode = 'h'
fileMode = 'w'
isBase64 = False

def isHeader(str):
    try:
        if str[-2] == ';':
            return 1
        else:
            return 0
    except:
        return 0

with open(args.filename,mode='r') as file:
    buff = file.readline()
    while buff != '':
        buff = file.readline()
        if isHeader(buff):
            buff = buff.split(';')
            buff.remove('\n')
            if 'base64' in buff:
                isBase64 = True
                buff.remove('base64')
            else: isBase64 = False
            arg = dict(map(lambda x: re.split(r':|=',x),buff))
            os.makedirs(os.path.dirname('./output/'), exist_ok=True)
            arg['path'] = arg['path'].split('/')[-1]
            print(arg)
            
            if isBase64:
                fileMode = 'wb'
            else:
                fileMode = 'w'
                
            with open('./output/'+arg["path"],mode=fileMode) as savedfile:
                    mode = 'd'
                    basebuff = file.read(int(arg["count"]))
                    if isBase64:
                        basebuff = base64.b64decode(basebuff)
                    savedfile.write(basebuff)
                    
                    savedfile.close()
