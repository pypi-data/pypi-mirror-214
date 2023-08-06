# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""
Module containing the Data model for linked data close to the unhide project, which wraps the original data stores
metadata and provenance data together with derived data for the actual graph
"""
import json
from pathlib import Path
from typing import Optional
from typing import Tuple

from pyshacl import validate as shacl_validate
from rdflib import Graph

from data_harvesting.util.external_schemas import load_external_schema

SCHEMA_ORG_SHAPE = load_external_schema('schema_org_shacl')


class LinkedDataObject():
    """
    Representation of a json-ld file with Original data, derived data, and metadata including provenance

    {
    metadata: {}
    original: {}
    derived: {}
    patch_stack: []
    }
    Each LinkedDataObject usually has a representative file on disk or data object in an object store
    The derived data will make it into the Unhide graph.

    # Provenance might/should be tract somewhere externally, like through AiiDA

    # Once might also use this or write a base class which can abstract from the actual storage,
    # like if it is stored in disk, or in an objectstore or some other database
    """
    def __init__(self, orgi_data: dict, metadata: dict = None, validate=True):
        """
        Initialize an LinkedDataObject instance

        :param orgi_data: jsonld dict of the original data instance
        :param metadata: dict which contains further metadata to be stored
        :param validate: Bool, default true. if the original data object and the UnhideData instance
            should be validated with shacl and co.
        """
        data = {'original': orgi_data}

        if metadata is None:
            metadata = derive_metadata(data)
        # store original and derived as graphs

        patch_stack, derived = derive_data(data)
        self.patch_stack = patch_stack
        data = {'original': orgi_data, 'metadata': metadata, 'derived': derived}
        self.data = data
        if validate:
            self.validate()

    def pack_jsonlddata(self, data: dict, metadata: dict):
        """
        Take the given data and pack it with metadata together.
        Also derive some new data to be used
        """
        packed_data: dict = {}

        return packed_data

    def unpack_jsonlddata(self, data: dict):
        """
        return the original data within a given packed json data object
        """
        return data.get('original')

    def get_meta(self):
        """
        return the metadata only
        """
        return self.data['metadata']

    def set_derived(self, derived: dict):
        """
        set the derived data
        """
        self.data['derived'] = derived

    def validate(self, shape_graph: Optional[Graph] = None, original_only: bool = False):
        """
        Do a shacl validation on the original data and derived

        todo get the default shape graph
        =SCHEMA_ORG_SHAPE
        """
        shape_graph = shape_graph or SCHEMA_ORG_SHAPE
        val_org = shacl_validate(self.data['original'], shacl_graph=shape_graph)
        conforms, results_graph, results_text = val_org
        if not original_only:
            val = shacl_validate(self.data['derived'], shacl_graph=shape_graph)
            conforms_de, results_graph, results_text = val
            conforms = conforms and conforms_de

        return conforms

    def serialize(self, destination: Path, graph_format='json-ld'):
        """
        Serialize the file to a json document, while the graph data is stored in a specific format
        """
        total_json = {
            'metadata': self.get_meta(),
            'original': self.data['original'],
            'derived': self.data['derived'],
            'patch_stack': [patch.to_string() for patch in self.patch_stack],
            #RDF_patch_stack_ids: []
        }

        with open(destination, 'w', encoding='utf-8') as fileo:
            json.dump(total_json, fileo)


def derive_metadata(data: dict) -> dict:
    """Derive metadata from the data and complete it
    """
    return data


def derive_data(data: dict) -> Tuple[list, dict]:
    """Derive ata from the data and complete it

    # steps to do:
    # 1. Complete ids
    # 2. Apply shacl rule list and infer triples
    # 3. store prov metadata on it in metadata
    """

    patch_stack: list = []
    return patch_stack, data
