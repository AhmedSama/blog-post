from __future__ import print_function
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster

NUM_CLUSTERS = 5


def colorized(rgba):
    newColors = []
    for i in rgba:
        if i < 50:
            i += 70
        elif i < 150 and i > 99:
            i += 30
        elif i >= 150 and i < 240:
            i += 10
        newColors.append(i)
    return newColors

def most_common_color(img):
    im = Image.open(img)
    im = im.resize((150, 150))      # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = np.histogram(vecs, len(codes))    # count occurrences

    index_max = np.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    peak = colorized(peak)
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    
    return "#"+colour
