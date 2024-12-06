import util

import nlmod


def test_dcs_structured():
    ds = util.get_ds_structured()
    line = [(0, 0), (1000, 1000)]
    dcs = nlmod.plot.DatasetCrossSection(ds, line)
    dcs.plot_layers()
    dcs.label_layers()
    dcs.plot_array(ds["kh"], alpha=0.5)
    dcs.plot_grid()


def test_dcs_vertex():
    ds = util.get_ds_vertex()
    line = [(0, 0), (1000, 1000)]
    dcs = nlmod.plot.DatasetCrossSection(ds, line)
    dcs.plot_layers()
    dcs.label_layers()
    dcs.plot_array(ds["kh"], alpha=0.5)
    dcs.plot_grid(vertical=False)
