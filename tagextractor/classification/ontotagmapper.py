"""ontology classifier."""
import owlready as owlr
from nltk.corpus import wordnet as wn


def __get_synset__(owlclass):
    name = owlclass.name.lower()
    synsets = wn.synsets(name)
    if synsets:
        return synsets[0]
    return None


def classifier(pictures, base_path, ontology):
    """Simple classifier."""
    owlr.onto_path.append(base_path)
    ontology = owlr.get_ontology(ontology)
    ontology.load()
    owlclasses = owlr.ONTOLOGIES['http://tagis.kr.com'].classes
    classes = {}
    for owlclass in owlclasses:
        # print(owlclass.name)
        syn = __get_synset__(owlclass)
        if syn:
            classes[owlclass.name] = (owlclass, syn)
            print("{} {}".format(owlclass.name, syn))
    for picture in pictures:
        print(picture)

if __name__ == '__main__':
    from tagextractor.classification.loader import DBLoader
    loader = DBLoader("sqlite:///database/synx_instagram.db")
    classifier(loader.load(), "resources", "kr-owlxml.owl")
