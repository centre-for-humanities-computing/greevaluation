'''
Download stanza grc pipeline.
Save to disk for usage in spacy CLI.
'''

import os
import stanza
import spacy_stanza

if not os.path.exists('models/stanza-perseus') and not os.path.exists("models/stanza-proiel"):
    # donwload newest stanza models
    stanza.download(lang='grc', package='perseus')
    stanza.download(lang='grc', package='proiel')

    # load as spacy models
    model_perseus = spacy_stanza.load_pipeline('grc', package='perseus')
    model_proiel = spacy_stanza.load_pipeline('grc', package='proiel')

    # serialize
    model_perseus.to_disk('models/stanza-perseus')
    model_proiel.to_disk('models/stanza-proiel')
