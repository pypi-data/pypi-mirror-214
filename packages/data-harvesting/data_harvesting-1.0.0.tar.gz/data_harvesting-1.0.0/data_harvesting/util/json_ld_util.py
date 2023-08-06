# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""This module contains utility to process and handle, validate json-ld data """
import copy
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Callable
from typing import List
from typing import Optional
from typing import Union

from pyld import jsonld
from pyshacl import validate as shacl_validate
from rdflib import Graph
from rdflib import Literal
from rdflib.compare import graph_diff
from rdflib.plugins.sparql.results.csvresults import CSVResultSerializer

from data_harvesting.util.pid_util import generate_uuid
#from itertools import chain

# validating jsonlD is not so clear:
# there is framing https://www.w3.org/TR/json-ld-framing/ and for example in R this https://codemeta.github.io/codemetar/articles/validation-in-json-ld.html
# For rdf data there is shacl. where one can define shapes for validation, which are kind of
# schema graphs
# these might also be used to do some logic operation stuff like inference of new triples


def validate_jsonld_simple(jsonld_data: dict) -> bool:
    """
    Test if the integrety of the json-ld file is right,
    i.e we do not validate the content of an instance like the schema does

    Returns True if it validates
    returns False if not
    """

    context = jsonld_data.get('@context', None)
    if context is None:
        print('Missing context, so probably no or broken json-LD data given')
        return False

    instance = copy.deepcopy(jsonld_data)
    # perform some roundturn json-LD operation to see if they work
    # TODO check if they are proper
    # Check if URIs are resolvable...
    instance = jsonld.expand(instance)
    instance = jsonld.compact(instance, context)

    # maybe also flatten the jsonLD to get all keys in general

    # check if we end with the same
    diffk: set = set(instance.keys()) - set(jsonld_data.keys())
    if len(diffk) != 0:
        print(f'The following keys are not supported: {diffk}')
        return False

    return True


def valdiate_from_file(filepath: Path, file_format='json-ld', options: Optional[dict] = None):
    """validate a given file"""
    data_graph = Graph()
    data_graph.parse(filepath, format=file_format)
    return validate(data_graph, options=options)


def validate(graph: Graph, validate_against: Optional[Graph] = None, options: Optional[dict] = None):
    """Validate a given rdf graph with shacl"""

    if validate_against is None:
        validate_against = Graph()
        # default is unhide specific
        # if not they should be downloaded, also they should be read once somewhere else and used from
        # there..
        # /data_harvesting/external_schemas/*
        basepath = Path(__file__).parent.parent.resolve() / 'external_schemas'
        schema_org = basepath / 'schemaorg-current-https.jsonld'
        codemeta = basepath / 'schema-codemeta.jsonld'
        if schema_org.exists():
            validate_against.parse(schema_org, format='json-ld')
        if codemeta.exists():
            validate_against.parse(codemeta, format='json-ld')
        # add other unhide specific things, ... or use only certain terms if class is given or so
    if options is None:
        options = {}
    vali = shacl_validate(graph, shacl_graph=validate_against, **options)
    conforms, results_graph, results_text = vali

    return conforms, vali


def convert(
    filepath: Path,
    destfilepath: Optional[Path] = None,
    informat: str = 'json-ld',
    outformat: str = 'ttl',
    overwrite: bool = False
) -> None:
    """
    convert a given graph file to a different format using rdflib
    """
    name = filepath.name.rstrip(filepath.suffix)
    destfilepath = destfilepath or Path(f'./{name}.{outformat}').resolve()

    if not overwrite and destfilepath.exists():
        return

    graph = Graph()
    graph.parse(filepath, format=informat)
    if outformat == 'csv':
        convert_to_csv(graph, destination=destfilepath)
    else:
        graph.serialize(destination=destfilepath, format=outformat)
    return


def convert_to_csv(graph: Graph, query: str = None, destination: Union[Path, str] = 'converted.csv'):
    """Convert results of a sparql query of a given graph to to a csv file

    Default query results:
    link table. Source | link_type | Target
    """

    default_edge_query = """
    PREFIX schema: <http://schema.org/>
    SELECT DISTINCT ?Source ?Type ?Target
    WHERE {
      ?Source ?Type ?Target .
    }
    """
    # ?sType ?tType
    #  ?source a ?sType .
    #  ?target a ?tType .
    #  FILTER((?sType) IN (schema:Person, schema:Organization, schema:Dataset, schema:SoftwareSourceCode, schema:Document))
    #  FILTER((?tType) IN (schema:Person, schema:Organization, schema:Dataset, schema:SoftwareSourceCode, schema:Document))
    #}
    #"""

    query = query or default_edge_query
    results = graph.query(query)
    csv_s = CSVResultSerializer(results)
    with open(destination, 'wb') as fileo:
        csv_s.serialize(fileo)


# Add URIs and types
def add_missing_uris(data: dict, path_prefix: str, alternative_ids: Optional[List[str]] = None) -> dict:
    """
    Add for each for each entity an internal id corresponding to the given prefix
    and the internal jsonpath (since jsonpath is bad for urls we use the xpath syntax)

    if it has an @id then sameAs is added
    further rules, if there is a url contentUrl identifier or email present, this becomes the id
    instead and our custom id is put in sameAs

    """
    # To avoid mutable as default value, through this is not so nice...
    if alternative_ids is None:
        alternative_ids = ['identifier', 'contentUrl', 'url']

    # For now we do this rekursive, iterative might be safer
    id_path = path_prefix
    new_data = data.copy()
    same_as = new_data.get('sameAs', [])
    if '@id' in new_data:
        if id_path not in same_as:
            same_as.append(id_path)
            new_data['sameAs'] = same_as
    else:
        found = False
        for term in alternative_ids:
            if term in new_data:
                new_data['@id'] = new_data['term']
                found = True
                break  # Only use the first one, so there is an order we want to replace these
        if not found:
            new_data['@id'] = id_path

    for key, val in new_data.items():
        if key == 'sameAs':
            continue
        id_path = path_prefix + f'/{key}'
        if isinstance(val, dict):
            new_data[key] = add_missing_uris(val, id_path)  # rekursion
        elif isinstance(val, str):  # str is also list
            new_data[key] = val
        elif isinstance(val, list):
            new_entry: list = []
            for i, entry in enumerate(val):
                if isinstance(entry, str):
                    new_entry.append(entry)
                prefix = id_path + f'_{i}'
                new_entry.append(add_missing_uris(entry, prefix))  # rekursion
            new_data[key] = new_entry
        else:
            new_data[key] = val

    return new_data


def add_missing_types(data: dict, type_map: Optional[List[dict]] = None) -> dict:
    """
    Add @types to data where it can be known for sure.
    TODO: There should be a general solution for this on the
    semantic/reasoner level, i.e schema.org allows for some reasoning, other rules could be stated by us

    like schema.org author, creator and contributor get type @Person or @organization
    the affiliation key is only allowed for a Person

    example type_map = [{'type': 'Person', 'keys': ['author', 'creator', 'contributor'], 'if_present' : 'affiliation'}]
    """

    if type_map is None:
        type_map = [{'type': 'Person', 'keys': ['author', 'creator', 'contributor'], 'if_present': 'affiliation'}]
    # If 'affiliation' present, type is a person
    new_data = data.copy()

    def add_type(data_d: Union[dict, list, str], mapping: dict) -> Union[dict, list, str]:
        """Add type"""
        if not isinstance(data_d, dict):
            return data_d
        if not '@type' in data_d.keys():
            condition = mapping.get('if_present', '')  # empty string is false
            if condition:
                if condition in data_d.keys():
                    data_d['@type'] = mapping.get('type')
        return data_d

    for key, val in new_data.items():  # Currently Only first level, maybe we have to do rekursion
        for mapping in type_map:
            if key in mapping.get('keys', []):
                if isinstance(val, list):
                    new_data[key] = [add_type(entry, mapping) for entry in val]
                elif isinstance(val, dict):
                    new_data[key] = add_type(val, mapping)
                else:
                    new_data[key] = val

    return new_data


# complete affiliations and organizations
# organizations with the same name should become the same id
# there should be a list of HGF orgas with ROARs.
# Also if a name of an org contains the name of a org with roar, this new org, should be created and
# linked to the org with the roar. like (Forschungszentrum Jülich GmbH, PGI-7)


def complete_affiliations(data: dict, roar_id_dict: dict, re3data_dict: dict, blank_node_identifier='_:N'):
    """
    Completes the given affiliation and organization where possible.

    roar_dict={ror_id1:{metadata}, ror_id2:{metadata}}
    the roar_id_dict is the inverse, of that. i.e: {'name': [roar_ids], 'grid_id': roar_id}

    for example:
    "affiliation": "Helmholtz-Zentrum Dresden-Rossendorf",
    - > "affiliation": {'@id': 'roar', '@type': organization 'name': "Helmholtz-Zentrum Dresden-Rossendorf"}

    more information about it should be somewhere else in the graph, we just want to link it to the right id

    example 2: (same for publisher, and includedInDataCatalog)
    "provider": {"@type": "Organization", "name": "J\u00fclich DATA"},
    ->  "provider": {"@type": "Organization", "name": "J\u00fclich DATA", '@id': 'http://doi.org/10.17616/R31NJMYC'},


    """
    raise NotImplementedError


def update_key(data: dict, key: Union[str, int], val_dict: dict, overwrite: bool = False):
    """
    Update the metadata of a certain key with a certain dict

    if the provider is already present, then we might want to complete the metadata, that it is linked correctly

    example:
    val = {
        "@id": " http://doi.org/10.17616/R31NJMYC",
        "@type": "Organization",
        "name": "J\u00fclich DATA"}

    """
    orgi = data.get(key, {})
    new = orgi
    if isinstance(orgi, list):
        for i, entry in enumerate(orgi):
            if isinstance(entry, dict):
                # todo
                pass
    if isinstance(orgi, dict):
        new = orgi
        if overwrite:
            new.update(val_dict)  # shallow merge for now
        else:
            for nkey, val in val_dict.items():
                if nkey not in orgi.keys():
                    new[nkey] = val
    data[key] = new
    return data


def generate_patch(graph_key='graph', patch_format='jena') -> Callable:
    """
    Generate a rdf patch for a given function which inputs a graph and outputs a graph.
    This function is meant to be used as a decorator generator.

    In order to find the graphs the input graph has to be the first argument to the function func,
    or a kwarg with the key provided by graph_key, default 'graph'.
    Also to find the output graph it requires the return value or the first return value to be a graph


    returns function
    raises ValueError
    """
    def generate_patch_dekorator(func, graph_key='graph', patch_format='jena'):
        """
        The actual decorator
        """
        def _generate_patch(*args, **kwargs):
            """
            returns the results of func plus a patch in front
            """
            # deepcopy because graph is parsed per refernce, often this will lead then to
            # the output graph == input graph after function execution
            if graph_key in kwargs:
                graph = deepcopy(kwargs[graph_key])
            else:
                if len(args) > 0:
                    if isinstance(args[0], Graph):
                        graph = deepcopy(args[0])
                    else:
                        raise ValueError(
                            f'No input graph found! Has to be provided first argument, or a kwargs {graph_key}!'
                        )

            results = func(*args, **kwargs)

            out_graph = None
            if isinstance(results, Graph):
                out_graph = results
            elif isinstance(results, list):
                if len(results) > 0:
                    if isinstance(results[0], Graph):
                        out_graph = results[0]
            if out_graph is None:
                raise ValueError('No output graph found! Has to single return or first return!')

            in_both, in_first, in_second = graph_diff(graph, out_graph)
            metadata = {
                'function_module': func.__module__,
                'function_name': func.__name__,
                'creation_time': datetime.now().isoformat()
            }
            patch = generate_patch_from_graph(in_first, in_second, patch_format=patch_format, metadata=metadata)

            return patch, results

        return _generate_patch

    return generate_patch_dekorator


def generate_patch_from_graph(in_first: Graph, in_second: Graph, patch_format='jena', metadata=None) -> Graph:
    """
    Generate a rdf patch for a given graph difference

    :param in_first: a graph, set of tiples containing triples only in the first/input graph
        from a diff, i.e. these were deleted
    :type in_first: Graph
    :param in_first: a graph, set of tiples containing triples only in the second/output graph
        from a diff, i.e. these were added
    :type in_first: Graph

    :param patch_format: Format in which the patch shall be returned, default 'jena'
        see: https://jena.apache.org/documentation/rdf-patch/, or
        https://github.com/afs/rdf-delta
    :type patch_format: str

    """
    pat = RDFPatch(metadata=metadata)
    patch_id = generate_uuid()  # maybe hash the changes instead?
    if patch_format != 'jena':  # for now
        raise ValueError(f'The requested patch format: {patch_format} is not supported.')

    # Header
    pat.add(('H', Literal('id'), Literal(patch_id), Literal('.')))

    # Start transfer
    pat.add(('TX', '.'))

    # The order does not play a role since these are sets
    for sub, pre, obj in in_first:
        pat.add(('D', sub, pre, obj, '.'))

    for sub, pre, obj in in_second:
        pat.add(('A', sub, pre, obj, '.'))
    # End transfer
    pat.add(('TC', '.'))
    return pat


class RDFPatch(object):
    """
    This class represents a RDF patch

    Created, since one could not parse the Jena Patch format into a simple RDF graph and
    rdf-delta is in java (https://github.com/afs/rdf-delta).

    If there is a other common way already out there this should be used instead
    for example see: https://www.w3.org/TR/ldpatch/

    and https://github.com/pchampin/ld-patch-py (LGPL).
    There are other formats one could serialize a patch to. These do not overlap in power.
    Problems with the current implementation of this:
    - Merging of a stack of RDFPatches would not work properly by the current 'several graph' design,
    since the order of the transactions matters...

    """
    names = ['header', 'addprefix', 'deleteprefix', 'add_triples', 'delete_triples']
    abbr = ['h', 'PA', 'PD', 'A', 'D']
    header = Graph()
    addprefix = Graph()
    deleteprefix = Graph()
    add_triples = Graph()
    delete_triples = Graph()
    metadata: dict = {}

    def __init__(
        self,
        metadata: Optional[dict] = None,
        header: Optional[Graph] = None,
        addprefix: Optional[Graph] = None,
        deleteprefix: Optional[Graph] = None,
        add_triples: Optional[Graph] = None,
        delete_triples: Optional[Graph] = None,
        patch_format: str = 'jena'
    ):
        """
        Init a RDF patch.

        :param metadata:
        :type metadata: Optional[dict]
        """
        if metadata is not None:
            self.metadata = metadata

        total_triples = 0
        for i, key in enumerate([header, addprefix, deleteprefix, add_triples, delete_triples]):
            if key is None:
                setattr(self, self.names[i], Graph())
            else:
                setattr(self, self.names[i], key)
                total_triples += len(key)

    '''
    # make the whole class iterateable
        self._current_index = 0
        self._class_size = total_triples
    def __iter__(self):
        #return chain(iter(self.header), iter(self.addprefix), iter(self.deleteprefix), iter(self.add_triples),
        # iter(self.delete_triples))
        return chain(self.header, self.addprefix, self.deleteprefix, self.add_triples, self.delete_triples)

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < self._class_size:
            lh = len(self.header)
            lap = len(self.addprefix)
            ldp = len(self.deleteprefix)
            ld = len(self.delete_triples)

            # graphs cannot be index like this.
            if self._current_index < lh:
                triple = ('H', *self.header[self._current_index])
            elif self._current_index < (lh+lap):
                triple = ('PA', *self.addprefix[self._current_index-lh])
            elif self._current_index < (lh+lap+ldp):
                triple = ('PD', *self.deleteprefix[self._current_index-lh-lap])
            elif self._current_index < (lh+lap+ldp+ld):
                triple = ('D', *self.delete_triples[self._current_index-lh-lap-ldp])
            else:
                triple = self.add_triples[self._current_index - lh+lap-ldp-ld]
            self._current_index += 1
            return triple

        raise StopIteration
    '''

    def to_string(self, patch_format='jena'):
        """
        Serialize Patch to string, to a format required for a certain backend.
        default Jena, see: https://jena.apache.org/documentation/rdf-patch/, or
        https://github.com/afs/rdf-delta
        """
        patch_text = ''
        if self.header is not None:
            graph = getattr(self, 'header')
            for (sub, pre, obj) in graph:
                patch_text += f'H {sub} {pre} {obj}\n'
        patch_text += 'TX .\n'

        for i, key in enumerate(self.abbr[1:]):
            gname = self.names[1 + i]
            graph = getattr(self, gname)

            for (sub, pre, obj) in graph:
                patch_text += f'{key} {sub} {pre} {obj} .\n'
        patch_text += 'TC .'
        return patch_text

    def add(self, nquad, patch_format='jena'):
        """
        Add a given tuple to the corresponding graph
        """
        if nquad[0] == 'H':
            self.header.add(nquad[1:])
        elif nquad[0] == 'PA':
            self.addprefix.add(nquad[1:-1])
        elif nquad[0] == 'PD':
            self.deleteprefix.add(nquad[1:-1])
        elif nquad[0] == 'A':
            self.add_triples.add(nquad[1:-1])
        elif nquad[0] == 'D':
            self.delete_triples.add(nquad[1:-1])
        elif any(nquad[0] == trans for trans in ['TX', 'TA', 'TC']):
            pass
        else:  # not supported just ignore
            raise ValueError('Warning: {nquad[0]} of {nquad} not supported')

        #self._class_size += 1

    def from_string(self, patch_text, patch_format='jena'):
        """
        Add a patch from a patch string.

        important since the patches will be serialized as strings
        and have to be read again
        """
        lines = patch_text.split('\n')

        for line in lines:
            nquad = line.split()
            self.add(nquad)


# What about patch sequences? then the current class is not sufficient. since graph, can not captures
# order


def apply_patch(graph: Graph, patch: RDFPatch, patch_format='jena') -> Graph:
    """
    Apply a given patch to a graph
    Since a patch is written a specific backend triple store like jena, this provides a way to apply
    the patch through python to a given graph outside of the backened
    """
    # todo implement PA
    o_graph = graph + patch.add_triples - patch.delete_triples
    #o_graph =
    #EX = Namesspace('')
    #o_graph.bind()

    return o_graph


def revert_patch(graph: Graph, patch: RDFPatch, patch_format='jena') -> Graph:
    """
    Apply a given patch to a graph
    Since a patch is written a specific backend triple store like jena, this provides a way to apply
    the patch through python to a given graph outside of the backened
    """
    # todo implement PA
    o_graph = graph - patch.add_triples + patch.delete_triples
    return o_graph
