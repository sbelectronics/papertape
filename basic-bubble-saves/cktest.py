import sys

b = open(sys.argv[1],"rb").read()

b = b[32:]

b = [ord(x) for x in b]

cksum = (b[7] << 8) | b[6]

b=b[8:]
v = 0
for x in b:
    v = v + x

v = v & (0xFFFF)

print("chksum is %04x" % cksum)

if v==cksum:
    print("good")
else:
    print("%04X should be %04X" % (v,cksum))
