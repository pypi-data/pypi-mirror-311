# -*- coding: utf-8 -*-
# :Project:   metapensiero.tool.tinject — Development shell
# :Created:   mer 29 giu 2022, 10:40:08
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022, 2023, 2024 Lele Gaifax
#

{
  description = "metapensiero.tool.tinject";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    gitignore = {
      url = "github:hercules-ci/gitignore.nix";
      # Use the same nixpkgs
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, gitignore }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (builtins) fromTOML readFile;
        inherit (gitignore.lib) gitignoreFilterWith;

        pinfo = (fromTOML (readFile ./pyproject.toml)).project;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        pkgs = import nixpkgs { inherit system; };

        bump-my-version = pkgs.python3Packages.buildPythonPackage rec {
          pname = "bump-my-version";
          version = "0.28.1";
          src = pkgs.python3Packages.fetchPypi {
            pname = "bump_my_version";
            inherit version;
            hash = "sha256-5gje9Rkbr1BbbN6IvWeaCpX8TP6s5CR622CsD4p+V+4=";
          };
          pyproject = true;
          build-system = [ pkgs.python3Packages.hatchling ];
          dependencies = with pkgs.python3Packages; [
            click
            pydantic
            pydantic-settings
            questionary
            rich
            rich-click
            tomlkit
            wcmatch
          ];
        };

        pkg = pkgs.python3Packages.buildPythonPackage {
          pname = pinfo.name;
          version = pinfo.version;
          src = getSource "tinject" ./.;
          pyproject = true;
          build-system = with pkgs.python3Packages; [
            pdm-backend
          ];
          doCheck = false;
          dependencies = with pkgs.python3Packages; [
            jinja2
            jinja2-time
            questionary
            ruamel-yaml
          ];
        };
        app = pkgs.python3Packages.toPythonApplication pkg;

        pydevenv = pkgs.python3.withPackages (ps: [
          bump-my-version
          pkg
          ps.build
          ps.twine
        ]);
      in {
        packages = {
          tinject = pkg;
        };

        apps = rec {
          tinject = {
            type = "app";
            program = "${app}/bin/tinject";
          };
          default = tinject;
        };

        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = with pkgs; [
              just
              pydevenv
              twine
            ];

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';
          };
        };
      });
}
