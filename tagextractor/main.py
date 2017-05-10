#! /usr/bin/python3
"""Main entry point.

author: Martino Ferrari
"""
import sys
import json
import argparse
import tagextractor.extraction.extractors as X


class Processor(object):
    """Pipeline Processor."""
    def __init__(self, photos):
        self._photos = photos
        self._filters = []

    def add_filter(self, new_filter):
        """Add pipeline step."""
        if callable(new_filter):
            self._filters.append(new_filter)

    def process(self):
        """ Execute the pipeline.

        this is the pattern for creating a generator
        pipeline, we start with a generator then wrap
        each consecutive generator with the pipeline itself.
        """
        pipeline = self._photos
        for new_filter in self._filters:
            pipeline = new_filter(pipeline)
        return pipeline


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Tag extraction and\
                                     preprocessing')
    parser.add_argument('--config', dest='config',
                        default='config.json',
                        help='Configuration file (default: config.json)')
    args = parser.parse_args()
    cfg_path = args.config
    print("Load configuration")

    with open(cfg_path) as config_file:
        config = json.load(config_file)
    if config["api"] == "JSON":
        extractor = X.JsonExtractor(config["api"]["apicfg"]["file"])
    elif config["api"] == "instagram":
        access_token = config["apicfg"]["ACCESS_TOKEN"]
        access_secret = config["apicfg"]["ACCESS_SECRET"]
        consumer_key = config["apicfg"]["CONSUMER_KEY"]
        consumer_secret = config["apicfg"]["CONSUMER_SECRET"]
        extractor = X.TwitInstaExtractor(access_token, access_secret,
                                         consumer_key, consumer_secret)
    else:
        api_key = config["apicfg"]["API_KEY"]
        api_secret = config["apicfg"]["API_SECRET"]
        extractor = X.FlickrExtractor(api_key, api_secret)

    pipliner = Processor(extractor.get_tags(lat=config["location"]["lat"],
                                            lon=config["location"]["lon"],
                                            radius=config[
                                                "location"]["radius"],
                                            num_photos=config["number"]))
    # for fiter in config["pipeline"]:
    # if filter == "Babel":
    # htt =
    if config["output_type"] == "STDOUT":
        for processed in pipliner.process():
            print(processed)
    elif config["output_type"] == "JSON":
        output = []
        i = 0
        for processed in pipliner.process():
            i += 1
            sys.stdout.write('\r {}/{}'.format(i, config["number"]))
            sys.stdout.flush()
            output.append(processed)
        print('\r {}/{}'.format(i, config['number']))
        with open(config["output_path"], "w") as output_file:
            json.dump(output, output_file, indent=4)
    else:
        for processed in pipliner.process():
            print("save {}".format(processed["id"]))


if __name__ == "__main__":
    main()
