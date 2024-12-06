###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

# A special thanks is given to Hans Dembinski for his help and input on the sWeight checks.   #
# In particular, KendallTau is heavily influenced by Hans' notebook on sWeight factorisation: #
# - https://github.com/sweights/sweights/blob/main/doc/notebooks/factorization_test.ipynb     #

# Another special thanks is given to Maxim Lysenko, on whose work the implementation of the   #
# factorisation tests (particularly in zFit) is based                                         #

from typing import Annotated, List, Union

import numpy as np
import ROOT as R
from scipy.stats import chi2
import zfit

from ..utils import create_zfit_dataset, split_paths, zfit_fit


class Factorisation:
    def __init__(
        self,
        discriminating_obs: Union[R.RooAbsReal, zfit.Space],
        control_var: str,
        sample: Union[List[str], str],
        pdf: Union[R.RooAddPdf, zfit.pdf.BasePDF],
        cut: Union[List[str], str] = "",
        threshold: float = 0.05,
        threads: int = 8,
    ):
        self.discriminating_obs = discriminating_obs
        self.control_var = control_var

        self.threshold = threshold

        self.threads = threads

        if isinstance(discriminating_obs, R.RooAbsReal) and isinstance(
            pdf, R.RooAddPdf
        ):
            self.backend = "roofit"
            _range = f"{discriminating_obs.GetName()} > {discriminating_obs.getMin()} && {discriminating_obs.GetName()} < {discriminating_obs.getMax()}"
        elif isinstance(discriminating_obs, zfit.Space) and isinstance(
            pdf, zfit.pdf.BasePDF
        ):
            self.backend = "zfit"
            _range = " && ".join(
                f"({name} > {lower[0]} && {name} < {upper[0]})"
                for name, lower, upper in zip(
                    discriminating_obs.obs,
                    discriminating_obs.lower,
                    discriminating_obs.upper,
                )
            )
        else:
            raise ValueError(
                "Unsupported combination of 'discriminating_obs' and 'pdf' arguments. These must be either both RooFit objects or both zFit objects."
            )

        self.rdf = R.RDataFrame(*split_paths(sample))
        self.rdf = self.rdf.Filter(_range)
        if cut:
            self.rdf = self.rdf.Filter(",".join(cut))

        low_data, high_data = self._create_datasets()

        self.split_fit = self._fit((low_data, high_data), pdf, simultaneous=False)
        self.simultaneous_fit = self._fit((low_data, high_data), pdf, simultaneous=True)

        # Compare likelihoods
        if self.backend == "roofit":
            self.split_nll = self.split_fit.minNll()
            self.split_nparams = self.split_fit.floatParsFinal().getSize()

            self.simultaneous_nll = self.simultaneous_fit.minNll()
            self.simultaneous_nparams = self.simultaneous_fit.floatParsFinal().getSize()

        elif self.backend == "zfit":
            self.split_nll = self.split_fit.fmin
            self.split_nparams = len(self.split_fit.params)

            self.simultaneous_nll = self.simultaneous_fit.fmin
            self.simultaneous_nparams = len(self.simultaneous_fit.params)

        self.ndof = self.split_nparams - self.simultaneous_nparams
        self.q_statistic = self.simultaneous_nll - self.split_nll
        self.p_value = chi2(self.ndof).sf(self.q_statistic)

        self.factorisable = self.p_value > self.threshold

        return

    def _create_datasets(self):

        # First event loop to get cut value
        var_array = self.rdf.AsNumpy((self.control_var,))
        median = np.median(var_array[self.control_var])

        _observables = (
            self.discriminating_obs.obs
            if self.backend == "zfit"
            else [self.discriminating_obs.GetName()]
        )

        low_data = self.rdf.Filter(f"{self.control_var} < {median}").AsNumpy(
            _observables
        )
        high_data = self.rdf.Filter(f"{self.control_var} >= {median}").AsNumpy(
            _observables
        )

        if self.backend == "roofit":
            low_data = R.RooDataSet.from_numpy(low_data, [self.discriminating_obs])
            high_data = R.RooDataSet.from_numpy(high_data, [self.discriminating_obs])
        elif self.backend == "zfit":
            low_data = create_zfit_dataset(low_data, self.discriminating_obs)
            high_data = create_zfit_dataset(high_data, self.discriminating_obs)

        return low_data, high_data

    def _fit(
        self,
        datasets: Annotated[List[Union[R.RooDataSet, zfit.Data]], 2],
        pdf: Union[R.RooAddPdf, zfit.pdf.BasePDF],
        simultaneous: bool = False,
    ):

        if self.backend == "roofit":
            category = R.RooCategory("category", "category")
            category.defineType("low")
            category.defineType("high")

            low_dataset, high_dataset = datasets
            data = R.RooDataSet(
                "data",
                "data",
                {self.discriminating_obs},
                Index=category,
                Import={"low": low_dataset, "high": high_dataset},
            )

            ws = R.RooWorkspace(f"{pdf.GetName()}_ws")
            ws.Import(data)
            ws.Import(pdf)

            split_params = list({y.GetName() for y in pdf.coefList()})
            if not simultaneous:
                split_params += [
                    "signal_mean",
                    "signal_width",
                    "combinatorial_exponent",
                ]
            sim_pdf = ws.factory(
                f"SIMCLONE::sim_{pdf.GetName()}({pdf.GetName()}, $SplitParam({{{','.join(split_params)}}},category))"
            )

            fit_kwargs = {
                "Extended": True,
                "EvalBackend": "cpu",
                "EvalErrorWall": False,
                "Minimizer": ("Minuit2", "minimize"),
                "NumCPU": self.threads,
                "Optimize": True,
                "Save": True,
                "Strategy": 2,
                "SumW2Error": True,
            }
            return sim_pdf.fitTo(data, **fit_kwargs)

        elif self.backend == "zfit":

            low_pdfs = []
            high_pdfs = []
            for _pdf in pdf.pdfs:
                _yield = _pdf.get_yield()

                _name = _yield.name
                _value = _yield.value()
                _lower = _yield.lower
                _upper = _yield.upper

                if simultaneous:
                    _low_params = list(_pdf.get_params(is_yield=False)) + [_pdf.obs]
                    _high_params = list(_pdf.get_params(is_yield=False)) + [_pdf.obs]
                else:
                    _low_params = []
                    _high_params = []
                    for _param in _pdf.get_params(is_yield=False):
                        _low_params.append(
                            zfit.Parameter(
                                f"low_{_param.name}",
                                _param.value(),
                                _param.lower,
                                _param.upper,
                            )
                        )
                        _high_params.append(
                            zfit.Parameter(
                                f"high_{_param.name}",
                                _param.value(),
                                _param.lower,
                                _param.upper,
                            )
                        )
                    _low_params.append(_pdf.obs)
                    _high_params.append(_pdf.obs)

                _low_pdf = type(_pdf)(*_low_params, **{"norm": _pdf.norm})
                _low_yield = zfit.Parameter(f"low_{_name}", _value, _lower, _upper)
                low_pdfs.append(_low_pdf.create_extended(_low_yield))

                _high_pdf = type(_pdf)(*_high_params, **{"norm": _pdf.norm})
                _high_yield = zfit.Parameter(f"high_{_name}", _value, _lower, _upper)
                high_pdfs.append(_high_pdf.create_extended(_high_yield))

            low_pdf = zfit.pdf.SumPDF(low_pdfs)
            low_nll = zfit.loss.ExtendedUnbinnedNLL(model=low_pdf, data=datasets[0])

            high_pdf = zfit.pdf.SumPDF(high_pdfs)
            high_nll = zfit.loss.ExtendedUnbinnedNLL(model=high_pdf, data=datasets[1])

            nll = low_nll + high_nll
            fit_result, _ = zfit_fit(nll)
            return fit_result

        return ValueError(f"Backend '{self.backend}' not recognised")
