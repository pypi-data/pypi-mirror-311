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

from ROOT import (
    RooMsgService,
    gROOT,
    RDataFrame,
    RooArgSet,
    RooDataSetHelper,
    RooFit,
    std,
)

from .utils import example_file, roofit_model, zfit_model, check_result

RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)
gROOT.SetBatch(True)


def test_fit_count_simple_roofit(example_file):
    from triggercalib import HltEff

    tree, path = example_file
    _, obs, pdf = roofit_model()

    hlteff = HltEff(
        "test_fit_count_simple_roofit",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        observable=obs,
        pdf=pdf,
        output_path="results/fit_count_simple_roofit/",
        threads=8,
    )
    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [3, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts()
    hlteff.efficiencies()
    hlteff.write("output_test_fit_count_simple_roofit.root")

    hist = hlteff.get_eff("trig_total_efficiency_observ1")
    val = hist.GetPointY(0)
    err_low = hist.GetErrorYlow(0)
    err_high = hist.GetErrorYhigh(0)

    assert check_result(
        val,
        (err_low, err_high),
        cut="discrim > 4800 && discrim < 5600 && observ1 > 0 && observ1 < 8",
    )


def test_fit_count_simple_zfit(example_file):
    from triggercalib import HltEff

    tree, path = example_file
    obs, pdf = zfit_model()

    hlteff = HltEff(
        "test_fit_count_simple_zfit",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        observable=obs,
        pdf=pdf,
        output_path="results/fit_count_simple_zfit/",
        threads=8,
        expert_mode=True,
    )
    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [3, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts()
    hlteff.efficiencies()
    hlteff.write("output_test_fit_count_simple_zfit.root")

    hist = hlteff.get_eff("trig_total_efficiency_observ1")
    val = hist.GetPointY(0)
    err_low = hist.GetErrorYlow(0)
    err_high = hist.GetErrorYhigh(0)

    assert check_result(
        val,
        (err_low, err_high),
        cut="discrim > 4800 && discrim < 5600 && observ1 > 0 && observ1 < 8",
    )


def test_fit_count_with_prefit(example_file):
    from triggercalib import HltEff

    tree, path = example_file
    ws, obs, pdf = roofit_model()

    # Perform prefit #
    rdf = RDataFrame(*example_file)
    rdf = rdf.Filter("isSignal")
    data = rdf.Book(
        std.move(
            RooDataSetHelper(
                "data",
                "data",
                RooArgSet(
                    obs,
                ),
            )
        ),
        (obs.GetName(),),
    )

    pdf.pdfList()[0].fitTo(data.GetValue())

    ws.var("signal_mean").setConstant(True)
    ws.var("signal_width").setConstant(True)

    # Calculate counts and efficiencies #
    hlteff = HltEff(
        "test_fit_count_with_prefit",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        observable=obs,
        pdf=pdf,
        output_path="results/fit_count_with_prefit/",
        threads=8,
    )
    hlteff.set_binning(
        {"observ1": {"label": "Observable 1", "bins": [3, 0, 8]}},
        compute_bins=True,
        bin_cut="discrim > 5100 && discrim < 5300 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    hlteff.counts()
    hlteff.efficiencies()
    hlteff.write("results/fit_count_with_prefit/output_test_fit_count_with_prefit.root")

    hist = hlteff.get_eff("trig_total_efficiency_observ1")
    val = hist.GetPointY(0)
    err_low = hist.GetErrorYlow(0)
    err_high = hist.GetErrorYhigh(0)

    assert check_result(
        val,
        (err_low, err_high),
        cut="discrim > 4800 && discrim < 5600 && observ1 > 0 && observ1 < 8",
    )
