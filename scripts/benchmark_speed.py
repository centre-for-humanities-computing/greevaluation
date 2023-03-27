import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, TypedDict

import numpy as np
import spacy
import spacy_stanza
import spacy_udpipe
from spacy.cli.benchmark_speed import benchmark, bootstrap, warmup
from spacy.language import Language
from spacy.tokens import Doc
from spacy.training import Corpus


class BenchmarkStats(TypedDict):
    mean: np.floating
    low: np.floating
    high: np.floating


class Model(TypedDict):
    loader: Callable
    loader_args: List
    loader_kwargs: Dict
    name: str


def get_stats(wps: np.ndarray) -> BenchmarkStats:
    """Calculates mean an 95% confidence interval
    of sample with bootstrapping."""
    wps_mean = np.mean(wps)
    bootstrap_means = bootstrap(wps)
    bootstrap_means.sort()

    # 95% confidence interval
    wps_low = np.quantile(wps, q=0.025)
    wps_high = np.quantile(wps, q=0.975)
    return {"mean": wps_mean, "low": wps_low, "high": wps_high}


def benchmark_speed_nlp(
    nlp: Language,
    data_path: Path,
    warmup_epochs: int = 3,
    n_batches: int = 50,
    batch_size: Optional[int] = None,
) -> BenchmarkStats:
    """Benchmarks nlp pipeline on given documents, returns mean word-per-second
    and confidence interval in a dict."""
    corpus = Corpus(data_path)
    docs = [eg.predicted for eg in corpus(nlp)]
    batch_size = batch_size or nlp.batch_size

    if len(docs) == 0:
        raise ValueError("Cannot benchmark speed using an empty corpus...")

    print(f"Warming up for {warmup_epochs} epochs...")
    warmup(nlp, docs, warmup_epochs, batch_size)

    print(f"Benchmarking {n_batches} batches...")
    wps = benchmark(nlp, docs, warmup_epochs, batch_size)

    return get_stats(wps)


def write_stats(path: Path, stats: BenchmarkStats) -> None:
    """Wrties benchmark stats to disk as JSON."""
    with open(path, "w", encoding="utf-8") as out_file:
        json.dump(stats, out_file)


GOLD_DIR = "corpus/binary"
OUT_DIR = "metrics"

MODELS: List[Model] = [
    # Stanza models
    Model(
        loader=spacy_stanza.load_pipeline,
        loader_args=["grc"],
        loader_kwargs=dict(package="perseus"),
        name="stanza-grc-perseus",
    ),
    Model(
        loader=spacy_stanza.load_pipeline,
        loader_args=["grc"],
        loader_kwargs=dict(package="proiel"),
        name="stanza-grc-proiel",
    ),
    # UDPipe models
    Model(
        loader=spacy_udpipe.load,
        loader_args=["grc-perseus"],
        loader_kwargs={},
        name="udpipe-grc-perseus",
    ),
    Model(
        loader=spacy_udpipe.load,
        loader_args=["grc-proiel"],
        loader_kwargs={},
        name="udpipe-grc-proiel",
    ),
    # greCy models
    Model(
        loader=spacy.load,
        loader_args=["grc_ud_perseus_trf"],
        loader_kwargs={},
        name="grc_ud_perseus_trf",
    ),
    Model(
        loader=spacy_udpipe.load,
        loader_args=["grc_ud_proiel_trf"],
        loader_kwargs={},
        name="grc_ud_proiel_trf",
    ),
    # odyCy models
    Model(
        loader=spacy.load,
        loader_args=["grc_dep_treebanks_trf"],
        loader_kwargs={},
        name="grc_dep_treebanks_trf",
    ),
]


def main() -> None:
    print("---------------")
    print("Speed benchmark")
    print("---------------")
    print()
    for corpus in ["perseus", "proiel"]:
        gold_path = Path(GOLD_DIR).joinpath(f"{corpus}.spacy")
        for model in MODELS:
            print(f"Benchmarking model: {model['name']}")
            nlp = model["loader"](*model["loader_args"], **model["loader_kwargs"])
            stats = benchmark_speed_nlp(nlp, data_path=gold_path)
            out_path = Path(OUT_DIR).joinpath(model["name"], "speed.json")
            write_stats(out_path, stats=stats)
    print("DONE")


if __name__ == "__main__":
    main()
