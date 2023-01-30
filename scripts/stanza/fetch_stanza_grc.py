'''
Download stanza grc pipeline.
Save to disk for usage in spacy CLI.
'''

import stanza
import spacy_stanza

stanza.download("grc")
nlp = spacy_stanza.load_pipeline("grc")
nlp.to_disk('models/stanza-model')
