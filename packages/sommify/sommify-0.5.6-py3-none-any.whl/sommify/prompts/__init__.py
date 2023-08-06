from thefuzz import fuzz, process
from nltk import ngrams
from .data import ent_to_iso, default
import re


def extract_mentions_naive(
    prompt,
    region_pool=default.region_pool,
    subregion_pool=default.subregion_pool,
    grape_pool=default.grape_pool,
):
    """
    Given a prompt, extract mentions of countries (iso), regions, subregions, and grapes.
    Naive approach, fuzzy string matching.
    """

    prompt = prompt.lower()

    isos = []
    regions = []
    subregions = []
    grapes = []

    combined_pool = list(ent_to_iso.keys()) + subregion_pool + region_pool + grape_pool

    # split text to list of sentences split by punctuation
    subsentences = re.split(r"[^\w\s]+", prompt)

    for ent in combined_pool:
        for ss in subsentences:
            for ngram in ngrams(
                ss.split(),
                n=len(ent.split()),
            ):
                score = fuzz.QRatio(" ".join(ngram), ent)

                if ent == "austria" and " ".join(ngram) == "australia":
                    print(score)

                if score >= 92:
                    if ent in subregion_pool:
                        subregions.append(ent)
                    elif ent in region_pool:
                        regions.append(ent)
                    elif ent in grape_pool:
                        grapes.append(ent)
                    else:
                        if isinstance(ent_to_iso[ent], list):
                            isos.extend(ent_to_iso[ent])
                        else:
                            isos.append(ent_to_iso[ent])

                    prompt = prompt.replace(" ".join(ngram), "")

    # also extract years between 1900 and 2100 (inclusive)
    years = re.findall(r"\b(19|20)\d{2}\b", prompt)
    years = [int(y) for y in years if int(y) >= 1900 and int(y) <= 2100]

    return {
        "countries": list(set(isos)),
        "regions": list(set(regions)),
        "subregions": list(set(subregions)),
        "grapes": list(set(grapes)),
        "years": years,
    }
