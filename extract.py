"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.
"""
import csv
import json
import pathlib

from models import NearEarthObject, CloseApproach

cad_json_path = pathlib.Path('./data/cad.json')
neo_csv_path = pathlib.Path('./data/neos.csv')


def load_neos(path=neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    output_neos = []
    with open(path) as neos_file:
        neos_reader = csv.DictReader(neos_file)
        for raw_neo in neos_reader:
            designation = raw_neo['pdes']
            name = raw_neo['name']
            diameter = float((raw_neo['diameter'])) if raw_neo['diameter'] else 0
            hazardous = raw_neo['pha'] == 'Y'

            neo = NearEarthObject(designation, name, diameter, hazardous)
            output_neos.append(neo)

    return output_neos


def load_approaches(path=cad_json_path):
    """Read close approach data from a JSON file.

    :param path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    output_cas = []
    with open(path) as cas_file:
        cas_data = json.load(cas_file)
        cas_fields = cas_data['fields']
        cas_data = cas_data['data']

        des_index = cas_fields.index('des')
        dist_index = cas_fields.index('dist')
        date_index = cas_fields.index('cd')
        vel_index = cas_fields.index('v_rel')

        for raw_ca in cas_data:
            designation = raw_ca[des_index]
            distance = float(raw_ca[dist_index])
            date = raw_ca[date_index]
            velocity = float(raw_ca[vel_index])

            ca = CloseApproach(designation, date, distance, velocity)
            output_cas.append(ca)

    return output_cas
