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

from array import array
import numpy as np
import os
import pytest
import ROOT as R
from typing import Annotated, List
import zfit


@pytest.fixture
def example_file(N_events=1_000_000):

    R.EnableImplicitMT(8)

    tree = "Hlt2Test/DecayTree"
    path = "example_file.root"

    one_signal_efficiencies = {"trig": 0.8, "tos": 0.7, "tis": 0.2}
    two_signal_efficiencies = {"trig": 0.7, "tos": 0.65, "tis": 0.1}

    one_background_efficiencies = {"trig": 0.2, "tos": 0.18, "tis": 0.3}
    two_background_efficiencies = {"trig": 0.05, "tos": 0.04, "tis": 0.2}

    purity = 4 / (
        one_signal_efficiencies["trig"] / one_background_efficiencies["trig"]
    )  # p = S / B
    background_yield = N_events / (1 + purity)
    signal_yield = purity * background_yield

    ws = R.RooWorkspace("ws")

    discrim_var = ws.factory("discrim[5000, 4800, 5800]")
    observ1_var = ws.factory("observ1[0, -10, 10]")
    observ2_var = ws.factory("observ2[0, -50, 50]")

    ws.factory(
        "BreitWigner::signal_discrim_pdf(discrim, signal_discrim_mean[5200], signal_discrim_width[16])"
    )
    ws.factory(
        "BreitWigner::signal_observ1_pdf(observ1, signal_observ1_mean[4], signal_observ1_width[1])"
    )
    ws.factory(
        "Gaussian::signal_observ2_pdf(observ2, signal_observ2_mean[-1], signal_observ2_width[4])"
    )
    signal_pdf = ws.factory(
        "PROD::signal_pdf(signal_discrim_pdf, signal_observ1_pdf, signal_observ2_pdf)"
    )

    ws.factory(
        "Exponential::background_discrim_pdf(discrim, background_discrim_lambda[-0.001])"
    )
    ws.factory(
        "Gaussian::background_observ1_pdf(observ1, background_observ1_mean[-2], background_observ1_width[8])"
    )
    ws.factory("Uniform::background_observ2_pdf(observ2)")
    background_pdf = ws.factory(
        "PROD::background_pdf(background_discrim_pdf, background_observ1_pdf, background_observ2_pdf)"
    )

    tree_list = R.TList()

    signal_data = signal_pdf.generate(
        {discrim_var, observ1_var, observ2_var}, signal_yield
    )
    signal_data.convertToTreeStore()
    signal_tree = signal_data.tree()
    tree_list.Add(signal_tree)
    signal_n = signal_tree.GetEntries()

    signal_issignal = array("b", [0])
    signal_issignal_branch = signal_tree.Branch(
        "isSignal", signal_issignal, "isSignal/O"
    )

    for line, signal_efficiencies in zip(
        ("Hlt1DummyOne", "Hlt1DummyTwo"),
        (one_signal_efficiencies, two_signal_efficiencies),
    ):

        signal_dec = array("b", [0])
        signal_dec_branch = signal_tree.Branch(
            f"{line}Decision", signal_dec, f"{line}Decision/O"
        )

        signal_tis = array("b", [0])
        signal_tis_branch = signal_tree.Branch(
            f"P_{line}Decision_TIS", signal_tis, f"P_{line}Decision_TIS/O"
        )

        signal_tos = array("b", [0])
        signal_tos_branch = signal_tree.Branch(
            f"P_{line}Decision_TOS", signal_tos, f"P_{line}Decision_TOS/O"
        )

        for _ in range(signal_n):
            signal_issignal[0] = 1
            signal_dec[0] = np.random.uniform() < signal_efficiencies["trig"]
            signal_tis[0] = np.random.uniform() < signal_efficiencies["tis"]
            signal_tos[0] = np.random.uniform() < signal_efficiencies["tos"]

            signal_issignal_branch.Fill()
            signal_dec_branch.Fill()
            signal_tis_branch.Fill()
            signal_tos_branch.Fill()

    background_data = background_pdf.generate(
        {discrim_var, observ1_var, observ2_var}, background_yield
    )
    background_data.convertToTreeStore()
    background_tree = background_data.tree()
    tree_list.Add(background_tree)
    background_n = background_tree.GetEntries()

    for line, background_efficiencies in zip(
        ("Hlt1DummyOne", "Hlt1DummyTwo"),
        (one_background_efficiencies, two_background_efficiencies),
    ):
        background_issignal = array("b", [0])
        background_issignal_branch = background_tree.Branch(
            "isSignal", background_issignal, "isSignal/O"
        )

        background_dec = array("b", [0])
        background_dec_branch = background_tree.Branch(
            f"{line}Decision", background_dec, f"{line}Decision/O"
        )

        background_tis = array("b", [0])
        background_tis_branch = background_tree.Branch(
            f"P_{line}Decision_TIS", background_tis, f"P_{line}Decision_TIS/O"
        )

        background_tos = array("b", [0])
        background_tos_branch = background_tree.Branch(
            f"P_{line}Decision_TOS", background_tos, f"P_{line}Decision_TOS/O"
        )

        for _ in range(background_n):
            background_issignal[0] = 0
            background_dec[0] = np.random.uniform() < background_efficiencies["trig"]
            background_tis[0] = np.random.uniform() < background_efficiencies["tis"]
            background_tos[0] = np.random.uniform() < background_efficiencies["tos"]

            background_issignal_branch.Fill()
            background_dec_branch.Fill()
            background_tis_branch.Fill()
            background_tos_branch.Fill()

    output_tree = R.TTree.MergeTrees(tree_list)
    with R.TFile(path, "RECREATE") as outfile:
        tree_dir = outfile.mkdir("Hlt2Test")
        tree_dir.WriteObject(output_tree, tree.rsplit("/", 1)[1])

    return tree, path


distributions = {
    "breitwigner": "BreitWigner",
    "doublecrystalball": "CrystalBall",
    "exponential": "Exponential",
    "gauss": "Gaussian",
}


def build_component(ws, name, observable, component):
    distribution = distributions[component["model"]]
    expanded_vars = ", ".join(
        f"{name}_{variable}[{', '.join(str(value) for value in values)}]"
        for variable, values in component["variables"].items()
    )
    expanded_vars = f"{observable}, {expanded_vars}"

    ws.factory(f"{distribution}::{name}_pdf({expanded_vars})")

    return ws


def roofit_model():  # <- not decorated as pytest fixture due to PyROOT RooFit persistency issues

    description = {
        "signal": {
            "model": "breitwigner",
            "variables": {"mean": [5200, 5150, 5300], "width": [16, 0.01, 64]},
            "yield": [100_000, 0, 1_000_000],
        },
        "combinatorial": {
            "model": "exponential",
            "variables": {"exponent": [-0.001, -0.01, 0]},
            "yield": [10_000, 0, 1_000_000],
        },
    }

    ws = R.RooWorkspace("test_ws")
    obs = ws.factory("discrim[4800, 5600]")
    build_strings = []
    for name, component in description.items():
        build_component(ws, name, "discrim", component)
        build_strings += [
            f"{name}_yield[{','.join(str(y) for y in component['yield'])}]*{name}_pdf",
        ]
    pdf = ws.factory(f"SUM::test_pdf({','.join(build_strings)})")
    return ws, obs, pdf


def zfit_model():
    # zfit model with BasePDF objects
    observable = zfit.Space("discrim", limits=(4800, 5600))

    # signal-gaussian extended
    mu = zfit.Parameter("signal_mu", 5200, 5150, 5300)
    sigma = zfit.Parameter("signal_sigma", 32, 0.01, 64)
    signal_yield = zfit.Parameter("signal_yield", 100_000, 0, 1_000_000)

    signal_pdf = zfit.pdf.Cauchy(obs=observable, m=mu, gamma=sigma)
    extended_sig = signal_pdf.create_extended(signal_yield, name="Signal")

    # bkg-exponential extended
    lambda_bkg = zfit.Parameter("background_exponent", -0.001, -0.01, 0)
    background_yield = zfit.Parameter("background_yield", 100_000, 0, 1_000_000)
    background_pdf = zfit.pdf.Exponential(lambda_bkg, obs=observable)
    extended_bkg = background_pdf.create_extended(background_yield, "Background")

    # SumPDF combines the signal and background with their respective yields
    pdf = zfit.pdf.SumPDF([extended_sig, extended_bkg], name="PDF", label="PDF")

    # Ensure the pdf is indeed a zfit.BasePDF object
    assert isinstance(pdf, zfit.pdf.BasePDF), "The pdf must be a zfit.BasePDF instance"

    return observable, pdf


def check_result(
    value: float,
    error: Annotated[List[float], 2],
    sample: str = "example_file.root:Hlt2Test/DecayTree",
    cut: str = "",
    line: str = "Hlt1DummyOne",
    threshold: float = 10.0,
):
    sample_rdf = R.RDataFrame(*reversed(sample.split(":", 1)))
    sample_rdf = sample_rdf.Filter(cut)
    sample_rdf = sample_rdf.Filter("isSignal")
    denominator = sample_rdf.Count()
    numerator = sample_rdf.Filter(f"{line}Decision").Count()
    R.RDF.RunGraphs((numerator, denominator))

    true_efficiency = numerator.GetValue() / denominator.GetValue()

    result_okay = (
        true_efficiency > value - threshold * error[0]
        and true_efficiency < value + threshold * error[1]
    )
    if not result_okay:
        print(
            f"True efficiency '{true_efficiency:.4f}' does not lie within window [{value - threshold * error[0]:.4f} - {value + threshold * error[1]:.4f}] ({threshold:.1f} sigma threshold)"
        )

    return result_okay
