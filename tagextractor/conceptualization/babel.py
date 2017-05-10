"""Babel utilities.

author: Damien Morard
"""
import json
import requests

BN_URI = "https://babelnet.io/v4/"
BF_URI = "https://babelfy.io/v1/"
SENSE_URI = "getSenses?"
DISAMBIGUATE_URI = "disambiguate?"


def save_json(parsed, json_path):
    """
    Save json in the request r in a file
    """
    with open(json_path, "w") as json_file:
        json_file.write(json.dumps(parsed, indent=4))


class Babel:
    '''
    Utilisation of Babel
    @Damien Morard
    '''

    def __init__(self, apikey):
        # please do not publish it on github
        self.apikey = apikey
        self.lang = "EN"

    def get_sense(self, word, output_file):
        """
        Give the sense of a word and put it in an output file
        :param word:
        :param outputFile:
        :return: a file with the sense of the word
        """
        uri_request = "{}{}word={}&lang={}&key={}".format(
            BN_URI, SENSE_URI, word, self.lang, self.apikey)

        response = requests.get(uri_request)
        parsed = json.loads(response.text)
        save_json(parsed, output_file)

    def desambiguate(self, sentence):
        """
        Desambiguate a sentence
        :param sentence:
        :return: a new sentence without useless words
        """

        # L'url contient un argument annRes = WN qui signifie qu'on restreint
        # notre desambiguisation à wordnet
        url_request = "{}{}text={}&lang={}&annRes=WN&key={}".format(
            BF_URI,
            DISAMBIGUATE_URI,
            sentence,
            self.lang,
            self.apikey)
        response = requests.get(url_request)
        parsed = json.loads(response.text)
        words_keep = []
        for element in parsed:
            start = element["charFragment"]["start"]
            end = element["charFragment"]["end"] + 1
            words_keep.append(sentence[start:end])
        return words_keep

    def add_lemmas(self, list_photos):
        """
        Return lemmas for each tag of each photos
        :param dicPhotos: dictionnary photos
        :return: the same dictionnary with a new field for each tag which
        is lemmas
        """
        for photo in list_photos:
            for tags in photo["tags"]:
                clean_tag = tags["raw"]
                if "#" in clean_tag:
                    clean_tag = clean_tag.replace("#", "")
                lemmas_temp = self.desambiguate(clean_tag)
                tags["lemmas"] = lemmas_temp
            yield photo
