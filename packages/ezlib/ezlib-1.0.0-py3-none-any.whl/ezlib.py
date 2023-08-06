import zlib, sys, os

def enough_args():
    if len(sys.argv) < 2:
        sys.stderr.write("Too few arguments. Usage: ezip/unezip/ezcat file...\n")
        sys.exit(1)
def ezip():
    enough_args()
    for file in sys.argv[1:]:
        try:
            with open(file, "rb") as fin:
                with open(file+".ez", "wb") as fout:
                    fout.write(zlib.compress(fin.read()))
            os.unlink(file)
            sys.stderr.write("Compression of "+file+" succeeded.\n")
        except:
            sys.stderr.write("Compression of "+file+" failed.\n")

def unezip():
    enough_args()
    for file in sys.argv[1:]:
        try:
            with open(file, "rb") as fin:
                with open(file[:-3], "wb") as fout:
                    fout.write(zlib.decompress(fin.read()))
            os.unlink(file)
            sys.stderr.write("Decompression of "+file+" succeeded.\n")
        except:
            sys.stderr.write("Decompression of "+file+" failed.\n")

def ezcat():
    enough_args()
    for file in sys.argv[1:]:
        try:
            with open(file, "rb") as fin:
               print(str(zlib.decompress(fin.read()), encoding='utf-8'))
        except:
            sys.stderr.write("Decompression of "+file+" failed.\n")
