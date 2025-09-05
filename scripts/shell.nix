{
  pkgs ? import <nixpkgs> { },
}:
(pkgs.buildFHSEnv {
  name = "rb3dx-build-env";
  targetPkgs =
    pkgs: with pkgs; [
      gmp
      icu
      python3
      ninja
      fish
      zlib
    ];
  runScript = "fish";
}).env