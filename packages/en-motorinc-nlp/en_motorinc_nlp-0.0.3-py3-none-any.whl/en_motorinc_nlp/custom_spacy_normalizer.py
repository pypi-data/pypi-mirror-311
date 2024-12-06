from spacy.language import Language
from spacy.tokens import Span
import re


# Define the price normalization component globally
@Language.component("normalize_prices")
def normalize_prices(doc):
    if not Span.has_extension("normalized_value"):
        Span.set_extension("normalized_value", default=None)

    for ent in doc.ents:
        if ent.label_ == "PRICE":
            try:
                text = " ".join(ent.text.lower().split())
                number = float(re.findall(r"\d+(?:\.\d+)?", text)[0])

                if any(suffix in text for suffix in ["cr", "crore", "crores"]):
                    normalized = number * 10000000
                elif any(
                    suffix in text for suffix in ["l", "lakh", "lakhs", "lac", "lacs"]
                ):
                    normalized = number * 100000
                elif any(suffix in text for suffix in ["k"]):
                    normalized = number * 1000
                else:
                    normalized = number

                ent._.normalized_value = normalized
            except Exception as e:
                print(f"Error normalizing price {ent.text}: {str(e)}")
    return doc


@Language.component("normalize_engine_displacement")
def normalize_engine_displacement(doc):
    if not Span.has_extension("normalized_value"):
        Span.set_extension("normalized_value", default=None)
    for ent in doc.ents:
        if ent.label_ == "EngineDisplacement":
            try:
                text = " ".join(ent.text.lower().split())
                number = float(re.findall(r"\d+(?:\.\d+)?", text)[0])
                normalized = None

                if any(suffix in text for suffix in ["l", "L", "liter", "litre", "cc"]):
                    normalized = number

                if normalized is None:
                    return
                ent._.normalized_value = normalized
            except Exception as e:
                print(f"""Error normalizing engine displacement {
                    ent.text}: {str(e)}""")
    return doc


@Language.component("normalize_entities")
def normalize_entities(doc):
    if not Span.has_extension("original_pattern"):
        Span.set_extension("original_pattern", default=None)

    pattern_mapping = doc.vocab.cfg.get("pattern_mapping", {})
    for ent in doc.ents:
        # Get the original pattern based on the matched ID
        if hasattr(ent, "ent_id_") and ent.ent_id_ in pattern_mapping:
            ent._.original_pattern = pattern_mapping[ent.ent_id_]
    return doc
