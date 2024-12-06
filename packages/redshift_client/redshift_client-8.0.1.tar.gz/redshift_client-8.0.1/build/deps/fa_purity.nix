{
  lib,
  makes_inputs,
  nixpkgs,
  python_pkgs,
  python_version,
}: let
  make_bundle = commit: sha256: let
    raw_src = builtins.fetchTarball {
      inherit sha256;
      url = "https://gitlab.com/dmurciaatfluid/purity/-/archive/${commit}/purity-${commit}.tar";
    };
    src = import "${raw_src}/build/filter.nix" nixpkgs.nix-filter raw_src;
  in
    import "${raw_src}/build" {
      makesLib = makes_inputs;
      inherit nixpkgs python_version src;
    };
  bundle =
    make_bundle "6b2f5f029171665070df306ea9db883a2ce82a31"
    "1ijsa1f2x74rqb742yrcw4r103w7zf03mplbr3hs6js6nfs69sdm"; # v2.0.0
in
  bundle.build_bundle (
    default: required_deps: builder:
      builder lib
      (required_deps (python_pkgs // {inherit (default.python_pkgs) types-simplejson;}))
  )
