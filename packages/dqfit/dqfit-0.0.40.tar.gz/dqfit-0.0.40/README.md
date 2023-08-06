## Quickstart:

[Getting Started: DQFIT on Google CoLab](https://colab.research.google.com/drive/1FhI_IaJ6C249rMAY7fBseh8JuPr9dkY-)

# This is designed for use in the NCQA Bulk FHIR Data Quality Pilot and Accompanied Research # 

- Brad Ryan
- Marc Overhage, MD, PhD
- Aneesh Chopra
- Mike Berger
- Ed Yuricisin
- Ben Hamlin, DrPH
- Rob Currie
- Beau Norgeot, PhD
- Arjun Sanyal
- Dede Ainbinder
- Evan 
- Patrick B
- many many more

Lead Engineer:
- Parker Holcomb

## Developer Quickstart

Package should feel familiar to those familiar with `import pandas as pd` and running a `sklearn` model:

```python 
import dqfit as dq
...
model = dq.DQI2(context_key)
model.fit(fhir_resources)
```

For an interactive example see:

[Getting Started: DQFIT on Google CoLab](https://colab.research.google.com/drive/1FhI_IaJ6C249rMAY7fBseh8JuPr9dkY-)

To run develop mode locally:

```bash
    python setup.py develop
```

To run script (`__main__.py`):

```bash
    python -m dqfit path/to/fhir/json path/to/output CONTEXT_KEYS
```

Where `path/to/fhir/json` is a directory containing FHIR (.ndjson, .json, .json.gz), `path/to/output` is directory to write results, and `CONTEXT_KEYS` is pipe delimited string like `'hello-world|COLE'`

As Flask:

```python
import dqfit as dq
@app.route('/test_fhir_resources', methods=['POST'])
def test_fhir_resources():
    data = request.get_json()
    model = dq.DQI2(context_key=data.get('context_key','hello-world'))
    model.fit(data['fhir_resources'])
    resp = {
        "index": model.index,
        "shape": model.shape,
        "result": model.result.to_dict(orient='records')
    }
    return resp

```

## Abstract

A pure function implementation of data quality assessment that scores “fitness for use” removes a key blocker to the success of Value Based Contracts: lack of trust in the clinical data used to compute payment. Standards such as HL7 FHIR and the USCDI provide part of the solution, however, measuring data quality must go beyond schema conformance[1]. Here we describe a linear transformation model that takes in a) a Population of FHIR Resources, and b) a set of weighted context dimensions (m) that have been “tuned” for use, where by scoring each data element by Model Dimension (M) such as Conformant, Complete, Plausible, effectively yields an (m, M)-dimensional result that enables stakeholders to empirically determine population-scales data data's clinical quality and fitness for a given context.

[1] Kahn et al 2016


# Background: The Case for High-Quality Data

**Goal**: confident prediction and effective management

**Problem**: low data quality is the enemy of prediction

**How to improve**: hold ourselves, and our partners, accountable to clinical-quality data

**Blocker**: no accountability mechanism for population scale data

**Solution**: work with industry to develop NCQA certified FHIR data quality tests kit [🎯 target process]

**Progress**: Developed a data quality index model based on Kahn [📍 You are here]

### Model Architecture

![Model Architecture](https://github.com/clinicalqualitydata/dqfit-python/blob/main/examples/figures/fig_2_model_architecture.png?raw=true)

### Results: 

"...where by scoring each data element by Model Dimension (M) such as Conformant, Complete, Plausible, effectively yields an (m, M)-dimensional result that enables stakeholders to empirically determine population-scales data data's clinical quality and fitness for a given context."

`model.result`

![model.result](https://github.com/clinicalqualitydata/dqfit-python/blob/main/examples/figures/fig_1_result.png?raw=true)

NB: Results below are created from Synthea Synthetic FHIR, are way "too perfect", and not represntative of the variances

`model.index`

A column score: `model.result['Score'].sum()`

e.g. 18.5

`model.visualize()`

![model.visualize](https://github.com/clinicalqualitydata/dqfit-python/blob/main/examples/figures/fig_1a_visualize.png?raw=true)

### IO, Performance, Benchmarking

Overall, we are in an IO bound constraint set. Once loaded into python memory, model performance is order of magnitudes faster than reading from disk, or API. Current and future work will leverage sql-on-fhir (e.g. postgres, BigQuery, etc)

```python
fhir_resources = dq.read_json(...)

# WIP
fhir_resources = dq.query_api(...)

fhir_resources = dq.query_sql(...)
```
