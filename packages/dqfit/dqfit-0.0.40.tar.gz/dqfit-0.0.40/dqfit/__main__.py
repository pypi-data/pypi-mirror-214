import json
import sys
from time import time

import dqfit as dq


def main(dir: str, outdir: str, contexts: str) -> None:
    # revist
    print("...Designed for NCQA Data Quality Pilot...")

    print(f"Loading FHIR from {dir}...")

    fhir_resources = dq.read_fhir(dir=dir)

    for context_key in contexts.split("|"):
        """
        Writes:
            result to json
            and context-summary to html
        """
        model = dq.DQI2(context_key=context_key)
        model.fit(fhir_resources)
        OUT = {
            "index": model.index,  # float
            "result": model.result.to_dict(),  # (m, M)
            # "path_level_result": model.fhir_path.to_dict(), #
        }
        with open(f"{outdir}/{context_key}-result.json", "w") as f:
            json.dump(OUT, f)
        fig = model.visualize()
        fig.write_html(f"{outdir}/{context_key}-context-report.html")
        print(f"Index: {model.index}")
        print(f"Model shape: {model.shape}")
        print(f"Saved {context_key} to {outdir}/{context_key}-result.json")


if __name__ == "__main__":
    start = time()
    main(dir=sys.argv[1], outdir=sys.argv[2], contexts=sys.argv[3])
    print(f"Finished in {round(time() - start, 1)} seconds")
    # try:
    #     start = time()
    #     main(dir=sys.argv[1], outdir=sys.argv[2], contexts=sys.argv[3])
    #     print(f"Finished in {round(time() - start, 1)} seconds")
    # except Exception as e:
    #     print(e)
    #     print("To run the package: ")
    #     print("$ python -m dqfit DIR OUTDIR 'CONTEXTS' N\n")
    #     print("For example:")
    #     print("$ python -m dqfit bundles/A . 'COLE|BCSE' N\n")
    #     print("DIR: directory of FHIR (Bulk or Bundles) as .json or .json.gz")
    #     print("OUTDIR: directory to for .json and .html output")
    #     print(
    #         "CONTEXTS is pipe delimited string context keys in COLE|BCSE|PSA|ASFE; e.g. 'BCSE|COLE' "
    #     )
