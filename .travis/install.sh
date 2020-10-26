#!/bin/sh

echo "TRAVIS_OS_NAME = $TRAVIS_OS_NAME"
echo "TRAVIS_PYTHON_VERSION = $TRAVIS_PYTHON_VERSION"
echo "TOXENV = $TOXENV"

if [ $TRAVIS_OS_NAME = 'osx' ]; then

  # Install wget using brew if necessary
  if hash wget 2>/dev/null; then
    brew install wget
  else
    echo "wget already installed"
  fi

  # Install miniconda on macOS
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O ~/miniconda.sh
  bash ~/miniconda.sh -b -p $HOME/miniconda
  . "$HOME/miniconda/etc/profile.d/conda.sh"
  hash -r
  conda config --set always_yes yes --set changeps1 no
  conda update -q conda

  # Useful for debugging any issues with conda
  conda info -a

else

  # Install miniconda on Linux
  sudo apt-get update
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
  bash miniconda.sh -b -p $HOME/miniconda
  . "$HOME/miniconda/etc/profile.d/conda.sh"
  hash -r
  conda config --set always_yes yes --set changeps1 no
  conda update -q conda

  # Useful for debugging any issues with conda
  conda info -a
fi

case "${TOXENV}" in
py37)
  # Install Mac Python3.7 environment
  conda env create -f environment-37.yml
  ;;
py38)
  # Install some custom Python 3.8 requirements on macOS
  conda env create -f environment.yml
  ;;
esac