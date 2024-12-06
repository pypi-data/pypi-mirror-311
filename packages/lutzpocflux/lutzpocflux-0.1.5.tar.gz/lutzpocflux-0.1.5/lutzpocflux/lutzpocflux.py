import numpy as np

from lutzpocflux.equations import pratioze_f, prd_f, prr_f, rld_f


class MakeFlux:

    def __init__(
        self,
        ze: np.ndarray | float,
        annual_npp: list[np.ndarray],
        npp: np.ndarray | None = None,
    ):
        """
        Convenience class for calculating export flux

        Args:
            ze (np.ndarray | float):    Array or float of export depth
                                        (depth z minus export zone depth)
            annual_npp (list[np.ndarray]): List of arrays for annual net primary production.
            npp (np.ndarray | None, optional):  Alternative npp layer to calculate the
                                                final export flux. If not provided then
                                                the average of all the annual_npp
                                                arrays is used. Defaults to None.

        Raises:
            ValueError: More than one npp layer should be provided in order to calculate
            SVI.
        """
        self.ze = ze
        annual_npp = np.array(annual_npp)
        self.npp = npp

        if annual_npp.shape[0] == 1:
            raise ValueError("Cannot calculate SVI or average from one annual layer.")

        self.all_years_average = np.nanmean(annual_npp, axis=0)
        self.all_years_std = np.nanstd(annual_npp, axis=0)
        self.svi = self.all_years_std / self.all_years_average

    def get_flux(self) -> np.ndarray:
        """
        Calculating the flux given the provided npp and ze arrays.

        Returns:
            np.ndarray: The export flux at the given export depth ze.
        """

        prdl = prd_f(self.svi)
        rldl = rld_f(self.svi)
        prrl = prr_f(self.svi)

        pratioze_res = pratioze_f(prdl, self.ze, rldl, prrl)

        if self.npp is None:
            return self.all_years_average * pratioze_res
        else:
            return self.npp * pratioze_res
