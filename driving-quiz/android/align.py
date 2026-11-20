import zipfile,struct,sys
src=zipfile.ZipFile(sys.argv[1]); out=zipfile.ZipFile(sys.argv[2],'w')
for zi in src.infolist():
    n=zipfile.ZipInfo(zi.filename,(1981,1,1,1,1,2)); n.compress_type=zi.compress_type; n.external_attr=zi.external_attr
    if zi.compress_type==zipfile.ZIP_STORED:
        pad=(-(out.fp.tell()+30+len(zi.filename.encode())))%4
        if pad: n.extra=struct.pack('<HH',0xD935,pad)+b'\0'*pad
    out.writestr(n,src.read(zi.filename))
out.close()
