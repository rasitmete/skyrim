import datetime
from pathlib import Path
import xarray as xr

from earth2mip import registry
from earth2mip.initial_conditions import cds
import earth2mip.networks.fcnv2_sm as fcnv2_sm
from .base import GlobalModel, GlobalPrediction
from .utils import run_basic_inference


class FourcastnetV2Model(GlobalModel):
    def __init__(self, model_name: str = "fourcastnet_v2"):
        super().__init__(model_name)

    def build_model(self):
        return fcnv2_sm.load(registry.get_model("e2mip://fcnv2_sm"))

    def build_datasource(self):
        return cds.DataSource(self.model.in_channel_names)

    @property
    def time_step(self):
        return self.model.time_step

    @property
    def in_channel_names(self):
        return self.model.in_channel_names

    @property
    def out_channel_names(self):
        return self.model.out_channel_names

    def predict_one_step(
        self,
        start_time: datetime.datetime,
        initial_condition: str | Path | None = None,
    ) -> xr.DataArray | xr.Dataset:
        return run_basic_inference(
            model=self.model,
            n=1,
            data_source=self.data_source,
            time=start_time,
            x=initial_condition,
        )


class FourcastnetV2Prediction(GlobalPrediction):
    def __init__(self, source):
        super().__init__(source)
        self.model_name = "fourcastnet_v2"
