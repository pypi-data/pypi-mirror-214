from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

import pandas as pd
import plotly.express as px
from tqdm import tqdm

import dqfit as dq
from dqfit.dimensions import Complete, Conformant, Plausible, Recent
from dqfit.transform import transform_to_fhir_path


class DQIBase(ABC):
    def __init__(
        self,
        context_key: str,
        Dimensions: list = [Conformant],
    ) -> None:
        self.context_key = context_key
        self.context = dq.io.load_context(context_key)
        self.Dimensions = Dimensions  # Model Dimensions
        self.M = Dimensions  # Model Dimensions
        self.m = pd.DataFrame(self.context["dim"])  # Context Dimensions

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def M_KEYS(self):
        return [dim.__name__ for dim in self.M]

    @property
    def shape(self):
        """
        (Patient x Resource x Path) x (Context Dimensions x Model Dimensions)
        ::
        (organism x molecule x atom) x (context x model)
        """
        return (
            (
                self.fhir_path["patient_id"].nunique(),
                self.fhir_path["id"].nunique(),
                len(self.fhir_path),
            ),
            (len(self.m), len(self.M)),  # weight
        )
    
    def row_score(self, row):
        return (row[self.M_KEYS] * row["W"]).sum()

    def fit(self, fhir_resources: List[dict]):
        """
        Emulates sklearn fit method.
        1. Takes in a list of FHIR resources
        2. Transforms into FHIR Path
        3. Fits each Model Dimension
        4. Aggregates Patient Level Scores
        5. Returns Results DataFrame of shape (m, M)
        """
        fhir_path = transform_to_fhir_path(fhir_resources)
        for Dim in self.Dimensions:
            fhir_path = Dim.fit(fhir_path, self.context)
        fhir_path = fhir_path.query("Conformant == 1").reset_index(drop=True)
        self.fhir_path = fhir_path  # for patient level results

        ## consider handling this in the get_patient_level_score method
        frequencies = (
            fhir_path.groupby(["path"])
            .agg(
                n=("patient_id", "nunique"),
                m=("id", "nunique"),
            )
            .reset_index()
        )
        frequencies = frequencies.merge(self.m, on="path", how="outer").fillna(0)

        # patient level results
        self.patient_ids = fhir_path["patient_id"].unique()
        patient_level = pd.concat([
            self.get_patient_level_result(patient_id)
            for patient_id in tqdm(self.patient_ids) # can this turn off?
        ])
        
        self.patient_level = patient_level

        # perhaps should be a method
        self.patient_level['Score'] = self.patient_level.apply(self.row_score, axis=1)
        self.patient_scores = self.patient_level.groupby('patient_id').agg(
            Score=("Score","sum")
        ).sort_values("Score").reset_index()


        result = (
            patient_level
            .groupby("path")
            .agg({dim.__name__: dim.agg_fn() for dim in self.Dimensions}) # dim.agg_fn()?
            .reset_index()
        )

        result = frequencies.merge(result, on="path", how="left")

        result["Score"] = result.apply(self.row_score, axis=1)

        self.result = result
        self.index = round(result["Score"].sum(), 1)
        return result

    def get_patient_level_result(self, patient_id: str):
        assert self.fhir_path is not None
        # consider moving to polars for memory efficiency
        patient_level_result = (
            (
                self.fhir_path.query(f"patient_id == '{patient_id}'")
                .groupby("path")
                .agg(
                    {dim.__name__: dim.agg_fn() for dim in self.Dimensions}
                )  # max for Recent
            )
            .reset_index()
            .merge(self.m, how="right", left_on="path", right_on="path")
            .fillna(0)
        )
        patient_level_result.insert(0, "patient_id", patient_id)
        return patient_level_result

    def draw_patient_score_distribution(self):
        return px.histogram(
            self.patient_scores,
            x="Score",
            title=f"Patient Score Distribution | n={len(self.patient_ids)}",
            height=600,
        )

    def visualize(self):
        # todo, make order consistent for facet_col, etc such that comparison is apples to apples
        df = self.result.copy()
        df["resourceType"] = df["path"].apply(lambda x: x.split(".")[0])
        dft = df.melt(
                id_vars=["path", "W", "resourceType"],
                var_name="Dimension",
                value_vars=self.M_KEYS,
                value_name="score",
            )
        dft['Dimension'] = pd.Categorical(dft['Dimension'], categories=self.M_KEYS, ordered=True)
        dft = dft.sort_values(["Dimension","path"], ascending=True)
        return px.scatter(
            dft,
            x="score",
            y="path",
            facet_col="Dimension",
            color="resourceType",
            size="W",
            size_max=10,
            title=f"{self} | {self.context_key} | Index: {self.index} <sup><br>{self.shape} | (Patient x Resource x Path), (ContextDimension, ModelDimension, W)",
            height=600,
        )


class DQI2(DQIBase):
    def __init__(
        self,
        context_key: str,
        Dimensions: list = [Conformant, Complete],
    ) -> None:
        super().__init__(context_key, Dimensions)


class DQI3(DQIBase):
    def __init__(
        self,
        context_key: str,
        Dimensions: list = [Conformant, Complete, Plausible],
    ) -> None:
        super().__init__(context_key, Dimensions)


class DQI4(DQIBase):
    def __init__(
        self,
        context_key: str,
        Dimensions: list = [Conformant, Complete, Plausible, Recent],
    ) -> None:
        super().__init__(context_key, Dimensions)
