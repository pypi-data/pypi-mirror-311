# Lutz POC FLux

LutzPOCFlux is a Python library for calculating POC export flux as detailed in [Lutz et al. 2007](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2006JC003706).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install LutzPOCFlux.

```bash
pip install lutzpocflux
```

Numpy is the only dependency. Other parts of the process, such as reading HDF files and plotting results are expected to be done with other packages.

## Usage

There is a convenience class for calculating Flux given a list of annual npp arrays and a `ze` array (or float value).

This handles

* Creation of the SVI array
* Creation of the total average array
* Calculation of the p ratio_ze
* Application of the ratio to the total average array

```python
from lutzpocflux import MakeFlux
mf = MakeFlux(ze=ze, annual_npp=npp_list)
flux = mf.get_flux()
```

Alternatively the calculated flux ratio can be used against another npp array provided seperately.

```python
from lutzpocflux import MakeFlux
mf = MakeFlux(ze=4000.0, annual_npp=npp_list, npp=some_other_npp)
flux = mf.get_flux()
```

Or the equations can be used on their own.

```python
from lutzpocflux.equations import (
    prd_f,
    rld_f,
    prr_f,
    pratioze_f,
)

# Assuming you already have an average npp and SVI layer, you can
# calculate individual parameters
rld = rld_f(svi)
prd = prd_f(svi)
prr = prr_f(svi)

# ze can be a 2D array of the same shape as the npp input arrays or a float value
pratio = pratioze_f(prd,ze,rld,prr)

# Now use the pratio to calculate your export npp given your choice of npp array:
npp_flux = npp * pratio
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Acknowledgments
Results were tested agains the R package [here](https://rdrr.io/github/chihlinwei/OceanData/src/R/lutz_p_flux.R)

## License

[MIT](https://choosealicense.com/licenses/mit/)