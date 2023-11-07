

def split_colon(alist):
    returnlist = []
    block = []
    for item in alist:
        if item == ':':
            returnlist.append(block)
            block = []
        else:
            block.append(item)
    if returnlist:
        returnlist.append(block)
    else:
        returnlist = block
    return returnlist

mpiargs = ['-n', '2', 'python', 'my_script.py', '-n', '800', ':', '-n', '1', 'python', 'my_script.py']

print(mpiargs)
split = split_colon(mpiargs)
print(split)
total = 0
for block in split:
    for ii, item in enumerate(block):
        if item in ['-n', '-np', '-ppn']:
            total += int(block[ii + 1])
            break
print(total)
