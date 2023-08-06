# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""Module containing the Base Harvester class"""
from datetime import datetime
from pathlib import Path

from data_harvesting import get_config
from data_harvesting import get_config_path


class Harvester:
    """Basic harvester class template to be implemented for a given pipeline

    Required in a method called run.
    This class may be extended in the future with maybe functions to parse
    and process data
    """
    outpath: Path
    config: dict
    sources: dict
    last_run: datetime

    def __init__(self, outpath=Path('.'), config_path=get_config_path()):
        """Initialize the Harvester

        Outpath: where data will be stored
        config_path: Path to the config files to read sources
        """
        self.outpath = outpath
        self.set_config(config_path=config_path)

    def set_config(self, config_path=get_config_path()):
        """Set sources and harvester specific config from a given config"""
        full_config = get_config(config_path)

        # This is the harvester specific part in the config
        self.config = full_config.get(self.__class__.__name__, {})
        self.sources = self.config.get('sources', {})
        last_run = self.config.get('last_run', None)

        if last_run is None:
            all_harvester_conf = full_config.get('AllHarvesters', {})
            last_run = all_harvester_conf.get('last_run', None)

        self.last_run = last_run

    def get_sources(self) -> dict:
        """Return sources"""
        return self.sources

    def get_config(self) -> dict:
        """Return harvester specific config"""
        return self.config

    def run(self, **kwargs) -> None:
        """Run the harvester

        This method is required to be implemented for every harvester
        """
        raise NotImplementedError
