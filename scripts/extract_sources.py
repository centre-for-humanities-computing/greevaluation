from typing import Iterable
import pandas as pd

TEST_PATH = "corpus/conllu/joint.conllu"
OUT_PATH = "assets/sources.csv"


def collect_sources(path: str) -> Iterable[str]:
    with open(path) as in_file:
        for line in in_file:
            if line.startswith("# source = "):
                source = line.removeprefix("# source = ").removesuffix("\n")
                yield source
            elif line.startswith("# sent_id = tlg"):
                source = line.removeprefix("# sent_id = ").removesuffix("\n")
                source = source.split("@")[0]
                yield source


def main() -> None:
    # Collecting unique sources
    sources = pd.Series(collect_sources(TEST_PATH)).unique()
    # Writing out sources to disk
    source_df = pd.DataFrame(
        dict(
            source=sources,
            period="medieval",
        )
    )
    source_df.to_csv(OUT_PATH)


if __name__ == "__main__":
    main()
