#!/usr/bin/env python3

import numpy as np
import os
from os import path
from ctypes import c_longlong, c_double, c_float, c_int, cast, pointer, POINTER
from numpy.testing import assert_array_max_ulp
from numpy._core._multiarray_umath import __cpu_features__
def convert(s, datatype="np.float32"):
    i = int(s, 16)                   # convert from hex to a Python int
    if (datatype == "np.float64"):
        cp = pointer(c_longlong(i))           # make this into a c long long integer
        fp = cast(cp, POINTER(c_double))  # cast the int pointer to a double pointer
    else:
        cp = pointer(c_int(i))           # make this into a c integer
        fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer

    return fp.contents.value         # dereference the pointer, get the float

str_to_float = np.vectorize(convert)

def test_validate_transcendentals():
    with np.errstate(all='ignore'):
        data_dir = path.join(path.dirname(__file__), 'data')
        files = os.listdir(data_dir)
        files = list(filter(lambda f: f.endswith('.csv'), files))
        for filename in files:
            filepath = path.join(data_dir, filename)
            with open(filepath) as fid:
                print(filepath)
                file_without_comments = (
                    r for r in fid if r[0] not in ('$', '#')
                )
                data = np.genfromtxt(file_without_comments,
                                     dtype=('|S39', '|S39', '|S39', int),
                                     names=('type', 'input', 'output', 'ulperr'),
                                     delimiter=',',
                                     skip_header=1)
                npname = path.splitext(filename)[0].split('-')[3]
                npfunc = getattr(np, npname)
                for i, datatype in enumerate(np.unique(data['type'])):
                    data_subset = data[data['type'] == datatype]
                    inval = np.array(str_to_float(data_subset['input'].astype(str), data_subset['type'].astype(str)), dtype=eval(datatype))
                    outval = np.array(str_to_float(data_subset['output'].astype(str), data_subset['type'].astype(str)), dtype=eval(datatype))
                    perm = np.random.permutation(len(inval))
                    inval = inval[perm]
                    outval = outval[perm]
                    maxulperr = data_subset['ulperr'].max()
                    print(f"datatype {i} with maxulperr={maxulperr}")
                    try:
                        assert_array_max_ulp(npfunc(inval), outval, maxulperr)
                    except AssertionError as e:
                        print(npfunc(inval)[:10])
                        print(outval[:10])
                        print(e)

if __name__ == "__main__":
    np.set_printoptions(floatmode="unique")
    test_validate_transcendentals()
