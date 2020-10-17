{ pkgs ? import <nixpkgs> {} }:
pkgs.poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  # see https://github.com/nix-community/poetry2nix/blob/master/overrides.nix for examples
  # overrides = poetry2nix.overrides.withDefaults (self: super: {
  #   foo = foo.overridePythonAttrs(oldAttrs: {});
  # });
}
