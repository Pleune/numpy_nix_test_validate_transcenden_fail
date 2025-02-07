1. [Install nix](https://nixos.org/download/)
2. Ensure `/etc/nix/nix.conf` lists your user as a "trusted user". e.g. add `trusted-users = root YOURUSERNAME` as a line
3. `nix develop github:pleune/numpy_nix_test_validate_transcenden_fail --option substituters "https://nix.pleunetowne.com/" --option extra-trusted-public-keys git-runner1:uBsNvsIl85z2ApqcH88hIhc4F0uGl5vFmt5ohr3NZDA=`

Now you are in an environment with python3.12 and numpy, where the tests fail. To see the tests fail in the nix build, clone this repo... First clone and comment out the overlay line in flake.nix and re-run the develop command. Then rerun the develop command but with `.` instead of the github url.
