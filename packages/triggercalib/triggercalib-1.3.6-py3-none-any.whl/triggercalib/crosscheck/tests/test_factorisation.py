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

import ROOT as R
from .utils import example_files_factorisable, example_files_non_factorisable
from triggercalib.hlteff.tests.utils import roofit_model, zfit_model

R.gROOT.SetBatch(True)


def test_factorisable_factorisation_roofit(example_files_factorisable):
    from triggercalib.crosscheck import Factorisation

    R.EnableImplicitMT(8)

    tree, signal_path, background_path = example_files_factorisable
    _, discrim_var, pdf = roofit_model()

    kt = Factorisation(
        discrim_var,
        "observ1",
        [f"{signal_path}:{tree}", f"{background_path}:{tree}"],
        pdf,
        threads=8,
    )

    assert kt.factorisable


def test_non_factorisable_factorisation_roofit(example_files_non_factorisable):
    from triggercalib.crosscheck import Factorisation

    R.EnableImplicitMT(8)

    tree, signal_path, background_path = example_files_non_factorisable
    _, discrim_var, pdf = roofit_model()

    kt = Factorisation(
        discrim_var,
        "observ1",
        [f"{signal_path}:{tree}", f"{background_path}:{tree}"],
        pdf,
        threads=8,
    )

    assert not kt.factorisable


def test_factorisable_factorisation_fit(example_files_factorisable):
    from triggercalib.crosscheck import Factorisation

    R.EnableImplicitMT(8)

    tree, signal_path, background_path = example_files_factorisable
    discrim_var, pdf = zfit_model()

    kt = Factorisation(
        discrim_var,
        "observ1",
        [f"{signal_path}:{tree}", f"{background_path}:{tree}"],
        pdf,
    )

    assert kt.factorisable


def test_non_factorisable_factorisation_zfit(example_files_non_factorisable):
    from triggercalib.crosscheck import Factorisation

    R.EnableImplicitMT(8)

    tree, signal_path, background_path = example_files_non_factorisable
    discrim_var, pdf = zfit_model()

    kt = Factorisation(
        discrim_var,
        "observ1",
        [f"{signal_path}:{tree}", f"{background_path}:{tree}"],
        pdf,
    )

    assert not kt.factorisable
