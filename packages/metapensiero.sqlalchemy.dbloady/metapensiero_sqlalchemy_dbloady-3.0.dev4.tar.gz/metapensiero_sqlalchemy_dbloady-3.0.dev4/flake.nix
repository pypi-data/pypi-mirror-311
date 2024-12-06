# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady — Development environment
# :Created:   gio 30 giu 2022, 8:29:40
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022, 2023, 2024 Lele Gaifax
#

{
  description = "metapensiero.sqlalchemy.dbloady";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
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
        inherit (builtins) fromTOML getAttr listToAttrs map readFile replaceStrings splitVersion;
        pkgs = import nixpkgs { inherit system; };
        inherit (pkgs.lib) cartesianProduct flip;
        inherit (gitignore.lib) gitignoreFilterWith;

        getSource = name: path: pkgs.lib.cleanSourceWith {
          name = name;
          src = path;
          filter = gitignoreFilterWith { basePath = path; };
        };

        # Python versions to test against, see also Makefile
        pyVersions = [
          "python311"
          "python312"
        ];

        # SQLAlchemy versions to try out
        saVersions = [
          { version = "1.4.54";
            hash = "sha256-RHD77QiMNdwgt4o5qvSuVP6BeQx4OzJkhyoCJPQ3wxo="; }
          { version = "2.0.36";
            hash = "sha256-fydnaAttI5iupwguRad0srB2e1yNj/uci2gwiOqbKcU="; }
        ];

        py-sa-pairs = cartesianProduct { pyv = pyVersions; sav = saVersions; };

        mkBMVPkg = python:
          python.pkgs.buildPythonApplication rec {
            pname = "bump-my-version";
            version = "0.28.1";
            src = pkgs.python3Packages.fetchPypi {
              pname = "bump_my_version";
              inherit version;
              hash = "sha256-5gje9Rkbr1BbbN6IvWeaCpX8TP6s5CR622CsD4p+V+4=";
            };
            pyproject = true;
            build-system = [ python.pkgs.hatchling ];
            dependencies = with python.pkgs; [
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

        mkSAPkg = python: saVersion:
          python.pkgs.buildPythonPackage rec {
            pname = "sqlalchemy";
            version = saVersion.version;
            src = python.pkgs.fetchPypi {
              inherit pname version;
              hash = saVersion.hash;
            };
            doCheck = false;
            nativeBuildInputs = [ python.pkgs.cython ];
            propagatedBuildInputs = [
              python.pkgs.greenlet
              python.pkgs.typing-extensions
            ];
          };

        mkPkg = pyVersion: saVersion:
          let
            py = getAttr pyVersion pkgs;
            sqlalchemy' = mkSAPkg py saVersion;
            pinfo = (fromTOML (readFile ./pyproject.toml)).project;
          in
            py.pkgs.buildPythonPackage {
              pname = pinfo.name;
              version = pinfo.version;

              src = getSource "dbloady" ./.;
              format = "pyproject";

              nativeBuildInputs = with py.pkgs; [
                pdm-backend
              ];

              propagatedBuildInputs = with py.pkgs; [
                progressbar2
                ruamel-yaml
                sqlalchemy'
              ];
            };

        # Concatenate just the major and minor version parts: "1.2.3" -> "12"
        mamiVersion = v:
          let
            inherit (builtins) splitVersion;
            inherit (pkgs.lib.lists) take;
            inherit (pkgs.lib.strings) concatStrings;
          in
            concatStrings (take 2 (splitVersion v));

        dbloadyPkgs = flip map py-sa-pairs
          (pair: {
            name = "dbloady-${mamiVersion pair.pyv}-sqlalchemy${mamiVersion pair.sav.version}";
            value = mkPkg pair.pyv pair.sav;
          });

        mkTestShell = pyVersion: saVersion:
         let
           py = getAttr pyVersion pkgs;
           pkg = mkPkg pyVersion saVersion;
           env = py.buildEnv.override {
             extraLibs = [
               pkg
               py.pkgs.psycopg2
             ];
           };
         in pkgs.mkShell {
           name = "Test Python ${py.version} SA ${saVersion.version}";
           packages = with pkgs; [
             (mkBMVPkg py)
             env
             just
             postgresql_16
             sqlite
           ];

           shellHook = ''
             TOP_DIR=$(pwd)
             export PYTHONPATH="$TOP_DIR/src''${PYTHONPATH:+:}$PYTHONPATH"
             trap "$TOP_DIR/tests/postgresql stop" EXIT
           '';
         };

        testShells = flip map py-sa-pairs
          (pair: {
            name = "test-${mamiVersion pair.pyv}-sqlalchemy${mamiVersion pair.sav.version}";
            value = mkTestShell pair.pyv pair.sav;
          });
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = (with pkgs; [
              (mkBMVPkg python3)
              just
              python3
              twine
            ]) ++ (with pkgs.python3Packages; [
              build
            ]);

            shellHook = ''
               TOP_DIR=$(pwd)
               export PYTHONPATH="$TOP_DIR/src''${PYTHONPATH:+:}$PYTHONPATH"
               trap "$TOP_DIR/tests/postgresql stop" EXIT
             '';
          };
        } // (listToAttrs testShells);

        packages = listToAttrs dbloadyPkgs;
      });
}
