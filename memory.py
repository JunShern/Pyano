
def readMemory(inst_mem, base_mem, vol_mem, vel_mem):
    with open("memory.txt") as f:
        lines = [line.strip() for line in f]
    for num in lines[0].split(' '):
        inst_mem.append(int(num))
    for num in lines[1].split(' '):
        base_mem.append(int(num))
    for num in lines[2].split(' '):
        vol_mem.append(int(num))
    for num in lines[3].split(' '):
        vel_mem.append(int(num))

def writeMemory(inst_mem, base_mem, vol_mem, vel_mem):
    with open("memory.txt", 'w') as f:
        for i in inst_mem:
            f.write("%i " %i)
        f.write("\n")
        for b in base_mem:
            f.write("%i " %b)
        f.write("\n")
        for v in vol_mem:
            f.write("%i " %v)
        f.write("\n")
        for s in vel_mem:
            f.write("%i " %s)
        f.write("\n")
