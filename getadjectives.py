from nltk.corpus import wordnet

with open('adjectives.txt', 'w') as ofile:
    words = set(lemma.name().replace('_', ' ')
                for synset in wordnet.all_synsets(wordnet.ADJ)
                for lemma in synset.lemmas())
    for word in sorted(words):
        ofile.write(word)
        ofile.write('\n')
