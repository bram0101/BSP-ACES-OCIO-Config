import math

LUT_SIZE = 4096
BOUNDS_MIN = 0.0
BOUNDS_MAX = 4.0
BOUNDS_SIZE = BOUNDS_MAX - BOUNDS_MIN


def lutFunc(val):
    
    if val < 1.0:
        return val

    return 1.0


with open("luts/saturation_mapping.cube", "w") as fLut:
    fLut.write("TITLE \"saturation mapping\"\n")
    fLut.write("LUT_1D_SIZE " + str(LUT_SIZE) + "\n")
    fLut.write("DOMAIN_MIN " + str(BOUNDS_MIN) + " " + str(BOUNDS_MIN) + " " + str(BOUNDS_MIN) + "\n")
    fLut.write("DOMAIN_MAX " + str(BOUNDS_MAX) + " " + str(BOUNDS_MAX) + " " + str(BOUNDS_MAX * 100.0) + "\n")
    for i in range(LUT_SIZE):
        val = float(i) / float(LUT_SIZE - 1) * BOUNDS_SIZE + BOUNDS_MIN
        value = lutFunc(val)
        fLut.write(str(val) + " " + str(value) + " " + str(val * 100.0) + "\n")
