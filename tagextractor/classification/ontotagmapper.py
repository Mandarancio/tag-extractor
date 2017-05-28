"""ontology classifier."""
# TODO add more concepts (boat) and
# NONE concepts (color, geography, lake)  as well
import owlready as owlr
from nltk.corpus import wordnet as wn

NONE_CATEGORY = "NONE"


def __get_synset__(owlclass):
    name = owlclass.name.lower()
    synsets = wn.synsets(name)
    if synsets:
        return synsets[0]
    return None


def __classify__(tag, classes):
    if tag['synset']:
        synset = wn.synset(tag['synset'])
        shortest = 0.1
        category = NONE_CATEGORY
        for name in classes:
            syn = classes[name][1]
            taxonomy_distance = synset.path_similarity(syn)
            if taxonomy_distance and taxonomy_distance > shortest:
                category = name
                shortest = taxonomy_distance
        # if shortest > 0.1:
            # print("{}: {}[{}]".format(tag['raw'], category, shortest))
        return category
    return NONE_CATEGORY


def classifier(pictures, base_path, ontology):
    """Simple classifier."""
    owlr.onto_path.append(base_path)
    ontology = owlr.get_ontology(ontology)
    ontology.load()
    # TODO how to get only the concept sub-class?
    owlclasses = owlr.ONTOLOGIES['http://tagis.kr.com'].classes
    classes = {}
    for owlclass in owlclasses:
        # print(owlclass.name)
        syn = __get_synset__(owlclass)
        if syn:
            classes[owlclass.name] = (owlclass, syn)
    for picture in pictures:
        tags = picture['tags']
        for tag in tags:
            tag['concept'] = __classify__(tag, classes)
        # TODO infere picture category
        yield picture


if __name__ == '__main__':
    from tagextractor.classification.loader import DBLoader
    LOADER = DBLoader("sqlite:///database/synx_instagram.db")
    print(LOADER.photo_number())
    for pic in classifier(LOADER.load(20), "resources", "kr-owlxml.owl"):
        print(pic['name'])
        for ptag in pic['tags']:
            print('  {}: {}'.format(ptag['raw'], ptag['concept']))
