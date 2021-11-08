"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""

import csv
import json


def make_results_dict_csv(results):
    """Given a collection of result CloseApproaches, make a list of dictionaries of the CloseApproaches for writing to a CSV.

    The keys are:
        fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    """
    results_dicts = []
    for ca in results:
        ca_dict = dict()
        ca_dict['datetime_utc'] = ca.time_str
        ca_dict['distance_au'] = ca.distance
        ca_dict['velocity_km_s'] = ca.velocity
        ca_dict['designation'] = str(ca.neo.designation)
        ca_dict['name'] = ca.neo.name
        ca_dict['diameter_km'] = ca.neo.diameter
        ca_dict['potentially_hazardous'] = str(ca.neo.hazardous)
        results_dicts.append(ca_dict)
    return results_dicts


def make_results_dict_json(results):
    """Given a collection of result CloseApproaches, make a list of dictionaries of the CloseApproaches for writing to a JSON file.

    The JSON  object is a list of dictionaries. Each dictionary ca_dict represents a Close Approach, with mapping.
    'datetime_utc', 'distance_au', 'velocity_km_s' to the associated attributes of the CloseApproach

    'neo' to another dictionary mapping
    'designation', 'name', 'diameter_km', 'potentially_hazardous' to the attributes of the neo.
    """
    results_dicts = []
    for ca in results:
        ca_dict = dict()
        ca_dict['datetime_utc'] = ca.time_str
        ca_dict['distance_au'] = ca.distance
        ca_dict['velocity_km_s'] = ca.velocity

        ca_dict['neo'] = dict()
        ca_dict['neo']['designation'] = str(ca.neo.designation)
        ca_dict['neo']['name'] = ca.neo.name
        ca_dict['neo']['diameter_km'] = ca.neo.diameter
        ca_dict['neo']['potentially_hazardous'] = ca.neo.hazardous

        results_dicts.append(ca_dict)
    return results_dicts


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    results_dicts = make_results_dict_csv(results)

    with open(filename, 'w') as out_file:
        writer = csv.DictWriter(out_file, fieldnames)
        writer.writeheader()
        for result in results_dicts:
            writer.writerow(result)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    results_dicts = make_results_dict_json(results)
    with open(filename, 'w') as out_file:
        json.dump(results_dicts, out_file, indent=2)
