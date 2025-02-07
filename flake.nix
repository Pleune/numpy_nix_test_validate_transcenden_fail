{
  description = "Mitchell Pleunes Nix flake for mcs5713 workspace";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs =
    inputs@{
      self,
      flake-parts,
      ...
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
      ];
      perSystem =
        {
          system,
          pkgs,
          config,
          ...
        }:
        {
          _module.args.pkgs = import self.inputs.nixpkgs {
            localSystem = {
              inherit system;
              gcc.arch = "x86-64-v3";
              gcc.tune = "alderlake";
            };
            overlays = [
              (final: prev: {
                pythonPackagesExtensions = prev.pythonPackagesExtensions ++ [
                  (pyFinal: pyPrev: {
                    # numpy tests fail when optimized with gcc.arch
                    # https://github.com/NixOS/nixpkgs/issues/275626
                    # https://github.com/numpy/numpy/issues/27460
                    numpy = pyPrev.numpy.overridePythonAttrs (old: {
                      disabledTests = old.disabledTests ++ [
                        "test_validate_transcendentals"
                      ];
                    });
                  })
                ];
              })
            ];
          };

          devShells.default = pkgs.mkShell {
            packages = [
              (pkgs.python3.withPackages (ps: with ps; [ numpy ]))
            ];
          };
        };
    };
}
