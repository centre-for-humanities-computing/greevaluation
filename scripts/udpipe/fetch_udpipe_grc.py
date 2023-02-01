'''
Download udpipe grc pipelines.
Save to disk for usage in spacy CLI.
'''

import os
import spacy_udpipe

if not os.path.exists('models/udpipe-perseus') and not os.path.exists("models/udpipe-proiel"):
    # donwload newest stanza models
    spacy_udpipe.download("grc-perseus")
    spacy_udpipe.download("grc-proiel")

    # SERIALIZATION DOESN'T WORK WITH spacy-udpipe
    # # load as spacy models
    # model_perseus = spacy_udpipe.load("grc-perseus")
    # model_proiel = spacy_udpipe.load("grc-proiel")

    # # serialize
    # model_perseus.to_disk('models/udpipe-perseus')
    # model_proiel.to_disk('models/udpipe-proiel')
