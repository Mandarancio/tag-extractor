import json
import extractors as X
import hashtokenizer as ht
import argparse
import sys


class Processor(object):

    def __init__(self, photos):
        self._photos = photos
        self._filters = []

    def add_filter(self, new_filter):
        if callable(new_filter):
            self._filters.append(new_filter)

    def process(self):
        # this is the pattern for creating a generator
        # pipeline, we start with a generator then wrap
        # each consecutive generator with the pipeline itself
        pipeline = self._photos
        for new_filter in self._filters:
            pipeline = new_filter(pipeline)
        return pipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tag extraction and\
                                     preprocessing')
    parser.add_argument('--config', dest='config',
                        default='config.json',
                        help='Configuration file (default: config.json)')
    args = parser.parse_args()
    cfg_path = args.config
    print("Load configuration")

    with open(cfg_path) as f:
        config = json.load(f)
    if config["api"] == "JSON":
        extractor = X.JsonExtractor(config["api"]["apicfg"]["file"])
    elif config["api"] == "instagram":
        ACCESS_TOKEN = config["apicfg"]["ACCESS_TOKEN"]
        ACCESS_SECRET = config["apicfg"]["ACCESS_SECRET"]
        CONSUMER_KEY = config["apicfg"]["CONSUMER_KEY"]
        CONSUMER_SECRET = config["apicfg"]["CONSUMER_SECRET"]
        extractor = X.TwitInstaExtractor(ACCESS_TOKEN, ACCESS_SECRET,
                                         CONSUMER_KEY, CONSUMER_SECRET)
    else:
        API_KEY = config["apicfg"]["API_KEY"]
        API_SECRET = config["apicfg"]["API_SECRET"]
        extractor = X.FlickrExtractor(API_KEY, API_SECRET)

    pipliner = Processor(extractor.get_tags(lat=config["location"]["lat"],
                                            lon=config["location"]["lon"],
                                            radius=config[
                                                "location"]["radius"],
                                            num_photos=config["number"]))
    # for fiter in config["pipeline"]:
    # if filter == "Babel":
    # htt =
    if config["output_type"] == "STDOUT":
        for x in pipliner.process():
            print(x)
    elif config["output_type"] == "JSON":
        d = []
        i = 0
        for x in pipliner.process():
            i += 1
            sys.stdout.write('\r {}/{}'.format(i, config["number"]))
            sys.stdout.flush()
            d.append(x)
        print('\r {}/{}'.format(i, config['number']))
        with open(config["output_path"], "w") as f:
            json.dump(d, f, indent=4)
    else:
        for x in pipliner.process():
            print("save {}".format(x["id"]))
