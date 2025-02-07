1. [Install nix](https://nixos.org/download/)
2. Ensure `/etc/nix/nix.conf` lists your user as a "trusted user". e.g. add `trusted-users = root YOURUSERNAME` as a line
3. `nix --option experimental-features "nix-command flakes" --option substituters "https://nix.pleunetowne.com/" --option extra-trusted-public-keys git-runner1:uBsNvsIl85z2ApqcH88hIhc4F0uGl5vFmt5ohr3NZDA=` develop github:pleune/numpy_nix_test_validate_transcenden_fail
Now you are in an environment with python3.12 and numpy, where the tests fail. To see the tests fail in the nix build, clone this repo... First clone and comment out the overlay line in flake.nix and re-run the develop command. Then rerun the develop command but with `.` instead of the github url.
4. `./fail.py`


```python
self = <test_umath_accuracy.TestAccuracy object at 0x7fff65e5b3b0>

    @platform_skip
    def test_validate_transcendentals(self):
        with np.errstate(all='ignore'):
            data_dir = path.join(path.dirname(__file__), 'data')
            files = os.listdir(data_dir)
            files = list(filter(lambda f: f.endswith('.csv'), files))
            for filename in files:
                filepath = path.join(data_dir, filename)
                with open(filepath) as fid:
                    file_without_comments = (
                        r for r in fid if r[0] not in ('$', '#')
                    )
                    data = np.genfromtxt(file_without_comments,
                                         dtype=('|S39','|S39','|S39',int),
                                         names=('type','input','output','ulperr'),
                                         delimiter=',',
                                         skip_header=1)
                    npname = path.splitext(filename)[0].split('-')[3]
                    npfunc = getattr(np, npname)
                    for datatype in np.unique(data['type']):
                        data_subset = data[data['type'] == datatype]
                        inval  = np.array(str_to_float(data_subset['input'].astype(str), data_subset['type'].astype(str)), dtype=eval(datatype))
                        outval = np.array(str_to_float(data_subset['output'].astype(str), data_subset['type'].astype(str)), dtype=eval(datatype))
                        perm = np.random.permutation(len(inval))
                        inval = inval[perm]
                        outval = outval[perm]
                        maxulperr = data_subset['ulperr'].max()
>                       assert_array_max_ulp(npfunc(inval), outval, maxulperr)
E                       AssertionError: Arrays are not almost equal up to 2 ULP (max difference is 3 ULP)

lib/python3.12/site-packages/numpy/_core/tests/test_umath_accuracy.py:74: AssertionError
```
