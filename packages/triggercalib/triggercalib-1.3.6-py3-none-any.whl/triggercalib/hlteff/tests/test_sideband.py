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

from ROOT import gROOT
from .utils import example_file, check_result

gROOT.SetBatch(True)


def test_sideband_1D(example_file):
    from triggercalib import HltEff

    tree, path = example_file
    sideband = {
        "discrim": {
            "range": [5000, 5400],
            "sideband": [5100, 5300],
        }
    }

    hlteff = HltEff(
        "test_sideband",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        output_path="results/sideband_1D/",
        sideband=sideband,
    )
    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [6, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts()
    hlteff.efficiencies()
    hlteff.write("results/output_test_sideband_1D.root")

    hist = hlteff["efficiencies"][
        "trig_total_efficiency_observ1"
    ]  # Test 'manual' result extraction
    val = hist.GetPointY(0)
    err_low = hist.GetErrorYlow(0)
    err_high = hist.GetErrorYhigh(0)

    assert check_result(
        val,
        (err_low, err_high),
        cut="discrim > 5000 && discrim < 5400 && observ1 > 0 && observ1 < 8",
    )


def test_sideband_2D(example_file):
    from triggercalib import HltEff

    tree, path = example_file
    sideband = {
        "discrim": {
            "range": [5000, 5400],
            "sideband": [5100, 5300],
        },
    }

    hlteff = HltEff(
        "test_sideband",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        output_path="results/sideband_2D/",
        sideband=sideband,
    )
    hlteff.set_binning(
        {
            "observ1": {"label": "Observable 1", "bins": [4, 0, 8]},
            "observ2": {"label": "Observable 2", "bins": [4, -18, 12]},
        },
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts()
    hlteff.efficiencies()
    hlteff.write("results/output_test_sideband_2D.root")

    hist = hlteff.get_eff("trig_total_efficiency_observ1_observ2")
    val = hist.GetZ()[0]
    err_low = hist.GetErrorZlow(0)
    err_high = hist.GetErrorZhigh(0)

    assert check_result(
        val,
        (err_low, err_high),
        cut="discrim > 5000 && discrim < 5400 && observ1 > 0 && observ1 < 8 && observ2 > -18 && observ2 < 12",
    )
