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
