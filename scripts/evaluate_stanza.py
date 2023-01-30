# %%
import stanza
import spacy_stanza

# %%
stanza.download("en")
nlp = spacy_stanza.load_pipeline("en")

