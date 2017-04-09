import requests
import json


class Babel:
    '''
    Utilisation of Babel
    @Damien Morard
    '''

    def __init__(self, apikey):
        # please do not publish it on github
        self.apikey = apikey
        self.lang = "EN"

    def getSense(self, word, outputFile):
        """
        Give the sense of a word and put it in an output file
        :param word:
        :param outputFile:
        :return: a file with the sense of the word
        """
        urlRequest = \
            "https://babelnet.io/v4/getSenses?word={}&lang={}&key={}".format(
                word, self.lang, self.apikey)
        r = requests.get(urlRequest)
        parsed = json.loads(r.text)
        self.saveJson(parsed, outputFile)

    def desambiguate(self, sentence):
        """
        Desambiguate a sentence
        :param sentence:
        :return: a new sentence without useless words
        """

        # L'url contient un argument annRes = WN qui signifie qu'on restreint
        # notre desambiguisation à wordnet
        urlRequest = \
            "https://babelfy.io/v1/disambiguate?text={}&lang={}&annRes=WN&key={}".format(
                sentence, self.lang, self.apikey)
        r = requests.get(urlRequest)
        parsed = json.loads(r.text)
        wordsKeep = []
        for element in parsed:
            start = element["charFragment"]["start"]
            end = element["charFragment"]["end"] + 1
            wordsKeep.append(sentence[start:end])
        return wordsKeep

    def returnLemmas(self, listPhotos):
        """
        Return lemmas for each tag of each photos
        :param dicPhotos: dictionnary photos
        :return: the same dictionnary with a new field for each tag which is lemmas
        """

        print(listPhotos)
        listPhotosLem = []
        for photo in listPhotos:
            for tags in photo["tags"]:
                cleanTag = tags["raw"]
                if "#" in cleanTag:
                    cleanTag = cleanTag.replace("#", "")
                lemmasTemp = self.desambiguate(cleanTag)
                tags["lemmas"] = lemmasTemp
            listPhotosLem.append(photo)
        return listPhotosLem

    def saveJson(self, parsed, nameFile):
        """
        Save json in the request r in a file
        """
        mon_fichier = open(nameFile, "w")
        mon_fichier.write(json.dumps(parsed, indent=4))
        mon_fichier.close()
