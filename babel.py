import requests
import json


class Babel:
    '''
    Utilisation of Babel
    @Damien Morard
    '''

    def __init__(self):
        # please do not publish it on github
        self.apikey = "apikey"
        self.lang = "EN"

    def getSense(self, word, outputFile):
        """
        Give the sense of a word and put it in an output file
        :param word:
        :param outputFile:
        :return: a file with the sense of the word
        """
        urlRequest = "https://babelnet.io/v4/getSenses?word={}&lang={}&key={}".format(
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
        urlRequest = "https://babelfy.io/v1/disambiguate?text={}&lang={}&key={}".format(
            sentence, self.lang, self.apikey)
        r = requests.get(urlRequest)
        parsed = json.loads(r.text)
        wordsKeep = []
        for element in parsed:
            start = element["charFragment"]["start"]
            end = element["charFragment"]["end"] + 1
            wordsKeep.append(sentence[start:end])
        return wordsKeep

    def saveJson(self, parsed, nameFile):
        """
        Save json in the request r in a file
        """
        mon_fichier = open(nameFile, "w")
        mon_fichier.write(json.dumps(parsed, indent=4))
        mon_fichier.close()
