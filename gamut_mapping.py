# BSD 2-Clause License
# 
# Copyright (c) 2022, Bram Stout Productions
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import math

LUT_SIZE = 61
BOUNDS_MIN = 0.0
BOUNDS_MAX = 1.0
BOUNDS_SIZE = BOUNDS_MAX - BOUNDS_MIN

SHAPER_LUT_SIZE = 1001
SHAPER_BOUNDS_MIN = -0.5
SHAPER_BOUNDS_MAX = 1.5
SHAPER_BOUNDS_SIZE = SHAPER_BOUNDS_MAX - SHAPER_BOUNDS_MIN

def shaper(val):
    if val > 0:
        return (math.pow(val, 1.0 / 3.0) * 0.65) + 0.25
    else:
        return (math.pow(-val, 1.0 / 3.0) / -3.174802104) + 0.25

def invShaper(val):
    if val > 0.25:
        return math.pow((val - 0.25) / 0.65, 3.0)
    else:
        return -math.pow((val - 0.25) * -3.174802104, 3.0)

def toHSV(R, G, B):
    M = max(max(R, G), B)
    m = min(min(R, G), B)
    C = M - m
    H = 0.0
    if C == 0:
        pass
    elif M == R:
        H = ((G - B) / C) % 6.0
    elif M == G:
        H = (B - R) / C + 2.0
    elif M == B:
        H = (R - G) / C + 4.0
    if H < 0:
        H += 6.0
    H *= 60.0
    S = C / M
    return [H, S, M]

def toRGB(H, S, V):
    C = V * S
    H /= 60.0
    X = C * (1.0 - abs(H % 2.0 - 1.0))
    R = 0
    G = 0
    B = 0
    if H < 0.0:
        pass
    elif H < 1.0:
        R = C
        G = X
    elif H < 2.0:
        R = X
        G = C
    elif H < 3.0:
        G = C
        B = X
    elif H < 4.0:
        G = X
        B = C
    elif H < 5.0:
        R = X
        B = C
    elif H < 6.0:
        R = C
        B = X
    m = V - C
    R += m
    G += m
    B += m
    return [R, G, B]

def luminance(R, G, B):
    return 0.2126 * R + 0.7152 * G + 0.0722 * B
        
def lutFunc(R, G, B):
    R = invShaper(R)
    G = invShaper(G)
    B = invShaper(B)

    Lo = luminance(R, G, B)

    # Make sure that at least one of the values is above 0.0
    # Those values would be pure black anyways, and this math
    # doesn't like all negative values that much
    if R <= 0.0 and G <= 0.0 and B <= 0.0:
        return [0.0, 0.0, 0.0]

    # Convert to HSV
    hsv = toHSV(R, G, B)
    H = hsv[0]
    S = hsv[1]
    V = hsv[2]
    
    # saturation mapping
    if S > 0.98:
        S = (S - 0.98) / 0.02
        S = S / (S + 1.0)
        S = S * (0.02 / 0.91) + 0.98
        S = min(S, 1.0)
    
    # Fix the hue in order to make the reds and blues
    # show in a more predictable manner.
    if H >= 354.0 and (B < 0.00001 or G < 0.00001):
        H = 0.0
    if H >= 240.0 and R < 0.00001:
        H = 240.0
    
    # Convert back to RGB
    rgb = toRGB(H, S, V)
    R = rgb[0]
    G = rgb[1]
    B = rgb[2]
    
    # Make sure that the luminance is still the same
    L = luminance(R, G, B)
    Lscale = Lo / L
    R *= Lscale
    G *= Lscale
    B *= Lscale
    
    # If one of the RGB values is still above 1.0,
    # then scale all of the values so that the values
    # do stay within 0.0 and 1.0.
    maxC = max(max(R, G), B)
    if maxC > 1.0:
        R /= maxC
        G /= maxC
        B /= maxC

    R = shaper(R)
    G = shaper(G)
    B = shaper(B)
    
    return [R, G, B]


with open("luts/gamut_mapping_shaper.cube", "w") as fLut:
    fLut.write("TITLE \"gamut mapping shaper\"\n")
    fLut.write("LUT_1D_SIZE " + str(SHAPER_LUT_SIZE) + "\n")
    fLut.write("DOMAIN_MIN " + str(SHAPER_BOUNDS_MIN) + " " + str(SHAPER_BOUNDS_MIN) + " " + str(SHAPER_BOUNDS_MIN) + "\n")
    fLut.write("DOMAIN_MAX " + str(SHAPER_BOUNDS_MAX) + " " + str(SHAPER_BOUNDS_MAX) + " " + str(SHAPER_BOUNDS_MAX) + "\n")
    for i in range(SHAPER_LUT_SIZE):
        val = float(i) / float(SHAPER_LUT_SIZE - 1) * SHAPER_BOUNDS_SIZE + SHAPER_BOUNDS_MIN
        value = shaper(val)
        fLut.write(str(value) + " " + str(value) + " " + str(value) + "\n")

with open("luts/gamut_mapping.cube", "w") as fLut:
    fLut.write("TITLE \"gamut mapping\"\n")
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