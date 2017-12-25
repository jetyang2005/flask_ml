#!/usr/bin/env python
#coding:utf-8
import os
import os.path
import subprocess

def retrieving_obpg(filelist,outpath):
    '''Download data'''
    f = open(filelist,'r')
    log= open(os.path.splitext(filelist)[0]+'_log.txt','w')
    os.chdir(outpath)
    print(os.curdir)
    for i in f:
        try:
            each_item = str(i.strip())
            cmd = 'wget http://oceandata.sci.gsfc.nasa.gov/cgi/getfile/'+each_item
            print(cmd)
            if not os.path.exists(outpath+each_item):
                status = subprocess.call(cmd)
                if status !=0:
                    log.write('\nFailed:'+each_item)
                    continue
                log.write('\nSuccess:'+each_item)
            log.flush()
        except:
            log.write('\nFailed:'+each_item)
            continue
    f.close()
    log.close()


if __name__  =='__main__':
        import glob
        outpath = 'F:\\卫星数据\\MODIS\\'
        for filelist in glob.glob(r'F:\卫星数据\MODIS\filelists\*m2s.txt'):
            retrieving_obpg(filelist,outpath)
        print('END')