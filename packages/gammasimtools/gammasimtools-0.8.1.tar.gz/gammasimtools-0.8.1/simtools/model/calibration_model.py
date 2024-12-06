"""Definition and modeling of a calibration device."""

import logging

from simtools.model.model_parameter import ModelParameter

__all__ = ["CalibrationModel"]


class CalibrationModel(ModelParameter):
    """
    CalibrationModel represents the MC model of an individual calibration device.

    It provides functionality to read the required parameters from the DB.

    Parameters
    ----------
    site: str
        Site name (e.g., South or North).
    calibration_device_model_name: str
        Calibration device model name (ex. ILLS-01, ILLN-01, ...).
    mongo_db_config: dict
        MongoDB configuration.
    model_version: str
        Model version.
    label: str
        Instance label. Important for output file naming.
    """

    def __init__(
        self,
        site,
        calibration_device_model_name,
        mongo_db_config,
        model_version,
        label=None,
    ):
        """Initialize CalibrationModel."""
        self._logger = logging.getLogger(__name__)
        self._logger.debug("Init CalibrationModel %s %s", site, calibration_device_model_name)
        ModelParameter.__init__(
            self,
            site=site,
            array_element_name=calibration_device_model_name,
            collection="calibration_devices",
            mongo_db_config=mongo_db_config,
            model_version=model_version,
            db=None,
            label=label,
        )
