{
  makes_inputs,
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    inherit (nixpkgs."${python_version}".pkgs) buildPythonPackage;
    inherit (nixpkgs.python3Packages) fetchPypi;
  };

  utils = makes_inputs.pythonOverrideUtils;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;

  layer_1 = python_pkgs:
    python_pkgs
    // {
      arch-lint = let
        result = import ./arch_lint.nix {
          inherit lib makes_inputs nixpkgs python_pkgs python_version;
        };
      in
        result.pkg;
      types-psycopg2 = import ./psycopg2/stubs.nix lib;
    };
  layer_2 = python_pkgs:
    python_pkgs
    // {
      fa-purity = let
        result = import ./fa_purity.nix {
          inherit lib makes_inputs nixpkgs python_pkgs python_version;
        };
      in
        result.pkg;
    };

  python_pkgs = utils.compose [layer_2 layer_1] nixpkgs."${python_version}Packages";
in {
  inherit lib python_pkgs;
}
