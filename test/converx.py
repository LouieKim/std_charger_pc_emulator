aa = 'ff'
bb = '11'

#dd = int(aa, 16)
#aa_b = bytes.fromhex(aa)
#bb_b = bytes.fromhex(bb)
#cc = format(aa_b, '04x')

an_integer = int(aa, 16)
bb_integer = int(bb, 16)
cc = an_integer << 8 | bb_integer

#hex_value = hex(an_integer)
print(cc)

dd = aa << 8 | bb
print(dd)

#aa_x = aa_b.hex()
#bb_x = bb_b.hex()

#aa_x = hex(aa_b)
#bb_x = hex(bb_b)

#xx = int(zz, 16)
#cc = aa.encode("utf-8").encode("hex")

#cc = aa_x << 8 | bb_x
#print(cc)