"""Streamflow indicator definitions."""

from __future__ import annotations

from xclim.core.cfchecks import check_valid
from xclim.core.indicator import ResamplingIndicator
from xclim.core.units import declare_units
from xclim.indices import (
    base_flow_index,
    generic,
    rb_flashiness_index,
    standardized_groundwater_index,
    standardized_streamflow_index,
)

__all__ = [
    "base_flow_index",
    "doy_qmax",
    "doy_qmin",
    "rb_flashiness_index",
    "standardized_groundwater_index",
    "standardized_streamflow_index",
]


class Streamflow(ResamplingIndicator):
    """Streamflow class."""

    context = "hydro"
    src_freq = "D"
    keywords = "streamflow hydrology"

    # TODO: TJS: The signature of this method seems wrong. Should it be `def cfcheck(cls, q):` or something else? Is it a static method?
    @staticmethod
    def cfcheck(q):
        check_valid(q, "standard_name", "water_volume_transport_in_river_channel")


class StandardizedStreamflowIndexes(ResamplingIndicator):
    """Resampling but flexible inputs indicators."""

    src_freq = ["D", "MS"]
    context = "hydro"


base_flow_index = Streamflow(
    title="Base flow index",
    identifier="base_flow_index",
    units="",
    long_name="Base flow index",
    description="Minimum of the 7-day moving average flow divided by the mean flow.",
    abstract="Minimum of the 7-day moving average flow divided by the mean flow.",
    compute=base_flow_index,
)


rb_flashiness_index = Streamflow(
    title="Richards-Baker Flashiness Index",
    identifier="rb_flashiness_index",
    units="",
    var_name="rbi",
    long_name="Richards-Baker Flashiness Index",
    description="{freq} of Richards-Baker Index, an index measuring the flashiness of flow.",
    abstract="Measurement of flow oscillations relative to average flow, "
    "quantifying the frequency and speed of flow changes.",
    compute=rb_flashiness_index,
)


doy_qmax = Streamflow(
    title="Day of year of the maximum streamflow",
    identifier="doy_qmax",
    var_name="q{indexer}_doy_qmax",
    long_name="Day of the year of the maximum streamflow over {indexer}",
    description="Day of the year of the maximum streamflow over {indexer}.",
    units="",
    compute=declare_units(da="[discharge]")(generic.select_resample_op),
    parameters={"op": generic.doymax, "out_units": None},
)


doy_qmin = Streamflow(
    title="Day of year of the minimum streamflow",
    identifier="doy_qmin",
    var_name="q{indexer}_doy_qmin",
    long_name="Day of the year of the minimum streamflow over {indexer}",
    description="Day of the year of the minimum streamflow over {indexer}.",
    units="",
    compute=declare_units(da="[discharge]")(generic.select_resample_op),
    parameters={"op": generic.doymin, "out_units": None},
)


standardized_streamflow_index = StandardizedStreamflowIndexes(
    title="Standardized Streamflow Index (SSI)",
    identifier="ssi",
    units="",
    standard_name="ssi",
    long_name="Standardized Streamflow Index (SSI)",
    description="Streamflow over a moving {window}-X window, normalized such that SSI averages to 0 for "
    "calibration data. The window unit `X` is the minimal time period defined by resampling frequency {freq}.",
    abstract="Streamflow over a moving window, normalized such that SSI averages to 0 for the calibration data. "
    "The window unit `X` is the minimal time period defined by the resampling frequency.",
    cell_methods="",
    keywords="streamflow",
    compute=standardized_streamflow_index,
)


standardized_groundwater_index = StandardizedStreamflowIndexes(
    title="Standardized Groundwater Index (SGI)",
    identifier="sgi",
    units="",
    standard_name="sgi",
    long_name="Standardized Groundwater Index (SGI)",
    description="Groundwater over a moving {window}-X window, normalized such that SGI averages to 0 for "
    "calibration data. The window unit `X` is the minimal time period defined by resampling frequency {freq}.",
    abstract="Groundwater over a moving window, normalized such that SGI averages to 0 for the calibration data. "
    "The window unit `X` is the minimal time period defined by the resampling frequency.",
    cell_methods="",
    keywords="groundwater",
    compute=standardized_groundwater_index,
)
