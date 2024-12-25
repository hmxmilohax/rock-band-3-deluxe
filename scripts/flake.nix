{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  };

  outputs =
    { self, nixpkgs }:
    {
      devShells.x86_64-linux.default =
        let
          pkgs = import nixpkgs { system = "x86_64-linux"; };
        in
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
        }).env;
    };
}