#! /usr/bin/python3
"""Main entry point.

author: Martino Ferrari
"""
import sys
import json
import argparse
import yaml
import tagextractor.extraction.extractors as X
import tagextractor.storage.dbmanager as dbm
import tagextractor.classification.storage.dbmanager as cbm
from tagextractor.storage.base import BASE
from tagextractor.classification.storage.base import CLASSIFIED_BASE
from tagextractor.conceptualization.wordnetreader import Wordnetreader

import tagextractor.classification.ontotagmapper as owlc
from tagextractor.classification.loader import DBLoader


class Processor(object):
    """Pipeline Processor."""
    def __init__(self, photos):
        """Init pipeline."""
        self._photos = photos
        self._filters = []

    def add_filter(self, new_filter):
        """Add pipeline step."""
        if callable(new_filter):
            self._filters.append(new_filter)

    def process(self):
        """Execute the pipeline.

        this is the pattern for creating a generator
        pipeline, we start with a generator then wrap
        each consecutive generator with the pipeline itself.
        """
        pipeline = self._photos
        for new_filter in self._filters:
            pipeline = new_filter(pipeline)
        return pipeline

    def config(self, config):
        """Load pipeline configuration."""
        if config['WordNet']:
            wn_r = Wordnetreader()
            self.add_filter(wn_r.extract)


def __load_cfg__(path):
    with open(path) as config_file:
        return yaml.load(config_file)


def __load_extractor__(config):
    if config["api"] == "JSON":
        extractor = X.JsonExtractor(config["api"]["api_cfg"]["path"])
    elif config["api"] == "instagram":
        access_token = config["api_cfg"]["ACCESS_TOKEN"]
        access_secret = config["api_cfg"]["ACCESS_SECRET"]
        consumer_key = config["api_cfg"]["CONSUMER_KEY"]
        consumer_secret = config["api_cfg"]["CONSUMER_SECRET"]
        frequency_path = config["api_cfg"]["frequency"]
        extractor = X.TwitInstaExtractor(X.TwitterAPI(
            access_token, access_secret,
            consumer_key, consumer_secret),
                                         frequency_path)
    else:
        api_key = config["api_cfg"]["API_KEY"]
        api_secret = config["api_cfg"]["API_SECRET"]
        extractor = X.FlickrExtractor(api_key, api_secret)
    return extractor


def __export__(pipeline, config):
    if config["module"] == "STDOUT":
        for processed in pipeline.process():
            print(processed)
    elif config["module"] == "JSON":
        output = []
        i = 0
        for processed in pipeline.process():
            i += 1
            sys.stdout.write('\r {}'.format(i))
            sys.stdout.flush()
            output.append(processed)
        print()
        with open(config["module_cfg"]['path'], "w") as output_file:
            json.dump(output, output_file, indent=4)
    elif config["module"] == "DB":
        manager = dbm.DBManager(config["module_cfg"]["path"])
        BASE.metadata.create_all(manager.engine())
        i = 0
        session = manager.session()
        for processed in pipeline.process():
            i += 1
            # print(processed)
            ntags = len(processed['tags'])
            sys.stdout.write('\r {:04d}, tags: {:02d}'.format(i, ntags))
            sys.stdout.flush()
            dbm.add_pict_to_db(processed, session)
            session.commit()
        manager.close()
    else:
        for processed in pipeline.process():
            print("save {}".format(processed["id"]))


def __classify__(config):
    loader = DBLoader(config['inputdb'])
    print("Photos to load: {}".format(loader.photo_number()))
    ontology = owlc.load_ontology(config['ontology_path'], config['ontology'],
                                  config['ontology_name'])
    picts = []
    for pic in owlc.classifier(loader.load(), ontology):
        print(pic['name'])
        for ptag in pic['tags']:
            print('  {}: {}'.format(ptag['raw'], ptag['concept']))
        picts.append(pic)

    owlc.make_distinct(ontology)
    ontology.sync_reasoner()
    owlc.write_ontology(ontology, config['result_ontology'])

    manager = cbm.DBManager(config['outputdb'])
    CLASSIFIED_BASE.metadata.create_all(manager.engine())
    session = manager.session()
    for pic in picts:
        cbm.add_pict_to_db(pic, session)


def main():
    """Main enrty point function."""
    parser = argparse.ArgumentParser(description='Tag extraction and\
                                     preprocessing')
    parser.add_argument('--config', dest='config', required=True,
                        help='Configuration file (default: config.yml)')
    args = parser.parse_args()
    cfg_path = args.config
    print("Load configuration")
    config = __load_cfg__(cfg_path)
    extraction = config['extraction']
    if extraction['enabled']:
        extractor = __load_extractor__(extraction)
        lat = extraction["location"]["lat"]
        lon = extraction["location"]["lon"]
        radius = extraction["location"]["radius"]
        num_photos = extraction["number"]
        pipeliner = Processor(extractor.get_tags(lat=lat,
                                                 lon=lon,
                                                 radius=radius,
                                                 num_photos=num_photos))
        pipeliner.config(extraction['pipeline'])
        __export__(pipeliner, extraction['storage'])
    classification = config['classification']
    if classification['enabled']:
        print("\nClassification:\n")
        __classify__(classification)


if __name__ == "__main__":
    main()
