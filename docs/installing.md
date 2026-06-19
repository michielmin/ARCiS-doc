# Installation

Before installing ARCiS, you need:
- A Fortran compiler: This can be either gfortran or ifort (any other might work but is not tested).
- cfitsio library: This is needed for Fortran to read and write binary fits files.
- MultiNest: This allows ARCiS to perform Bayesian retrievals.

## On a Mac
The easiest way to install cfitsio is through HomeBrew:

```bash
brew install cfitsio
```
Next, fetch MultiNest:
```
git clone https://github.com/JohannesBuchner/MultiNest.git
cd MultiNest/build
cmake ..
make
sudo make install
```

## Installing from git

Create the ARCiS main directory:
```
cd ~ ; mkdir ARCiS ; cd ARCiS
```
Create the ARCiS Data directory. This has to be placed in this exact location in your home directory:
```
cd ~/ARCiS ; mkdir Data
```
Clone the source code:
```
git clone http://github.com/michielmin/ARCiS ./src
cd src
```
Compile the code
```
make gfort=true multi=true
```
This creates the ARCiS binary, which you can put in any path accessible (e.g., /usr/bin).
