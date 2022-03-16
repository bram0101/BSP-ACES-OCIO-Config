import math

LUT_SIZE = 65
BOUNDS_MIN = 0.0
BOUNDS_MAX = 1.0
BOUNDS_SIZE = BOUNDS_MAX - BOUNDS_MIN

sLin = 1.0
oLin = 0.001
sLog = 0.18
oLog = 0.54

def shaper(val):
    return math.log(val * sLin + oLin, 10.0) * sLog + oLog

def invShaper(val):
    return (math.pow(10.0, (val - oLog) / sLog) - oLin) / sLin

def lutFunc(R, G, B):
    R = invShaper(R)
    G = invShaper(G)
    B = invShaper(B)
    
	# Corresponds to the V in HSV
    Cmax = max(R, max(G, B))
    
    if Cmax > 0:
		# Normalise the values to the range 0.0 - 1.0
        R /= Cmax
        G /= Cmax
        B /= Cmax
        
		# Inverse it
        R = 1.0 - R
        G = 1.0 - G
        B = 1.0 - B
        
		# We can now calculate the saturation.
		# We do clip it to a maximum of 1, because
		# of some imprecision due to LUTs.
        S = min(max(R, max(G, B)),1.0)
        
		# Boost the saturation.
		# The 1.4 specifies by how much to boost the saturation.
		# Higher values saturate more.
        newS = 1.0 - math.pow(1.0 - S, 1.4)
        if S > 0.0:
            Sfactor = newS / S
            R *= Sfactor
            G *= Sfactor
            B *= Sfactor
        
		# Desaturate based on luminance
		# The 7.0 power can be changed to determine
		# how quickly it desaturates. A lower number
		# desaturates slower
        desat_factor = Cmax * (-0.25 / 128.0) + 1.0
        if desat_factor < 0.0:
            desat_factor = 0.0
        desat_factor = math.pow(desat_factor, 7.0)
        
        R *= desat_factor
        G *= desat_factor
        B *= desat_factor
        
		# Invert the values again
        R = 1.0 - R
        G = 1.0 - G
        B = 1.0 - B
        
		# Undo the normalisation
        R *= Cmax
        G *= Cmax
        B *= Cmax
        
		# Boost the exposure for very saturated colours
        exposure_boost = (math.pow(10.0, -Cmax) + math.pow(10.0, -10.0 * Cmax)) * 0.18 + 0.25
        saturation_attenuation = math.pow(newS, 2.0)
        saturation_exposure_boost = exposure_boost * saturation_attenuation + 1.0
        R *= saturation_exposure_boost
        G *= saturation_exposure_boost
        B *= saturation_exposure_boost
    
    R = shaper(R)
    G = shaper(G)
    B = shaper(B)
	
	# Clip values to 0.
	# This is needed due to limited precision,
	# because of LUTs and the use of floating point.
    if R < 0.000000001:
        R = 0
    if G < 0.000000001:
        G = 0
    if B < 0.000000001:
        B = 0
    return [R, G, B]

with open("luts/look_bsp.cube", "w") as fLut:
    fLut.write("TITLE \"look_bsp\"\n")
    fLut.write("LUT_3D_SIZE " + str(LUT_SIZE) + "\n")
    fLut.write("DOMAIN_MIN " + str(BOUNDS_MIN) + " " + str(BOUNDS_MIN) + " " + str(BOUNDS_MIN) + "\n")
    fLut.write("DOMAIN_MAX " + str(BOUNDS_MAX) + " " + str(BOUNDS_MAX) + " " + str(BOUNDS_MAX) + "\n")
    for iB in range(LUT_SIZE):
        for iG in range(LUT_SIZE):
            for iR in range(LUT_SIZE):
                R = float(iR) / float(LUT_SIZE - 1) * BOUNDS_SIZE + BOUNDS_MIN
                G = float(iG) / float(LUT_SIZE - 1) * BOUNDS_SIZE + BOUNDS_MIN
                B = float(iB) / float(LUT_SIZE - 1) * BOUNDS_SIZE + BOUNDS_MIN
                value = lutFunc(R, G, B)
                fLut.write(str(value[0]) + " " + str(value[1]) + " " + str(value[2]) + "\n")