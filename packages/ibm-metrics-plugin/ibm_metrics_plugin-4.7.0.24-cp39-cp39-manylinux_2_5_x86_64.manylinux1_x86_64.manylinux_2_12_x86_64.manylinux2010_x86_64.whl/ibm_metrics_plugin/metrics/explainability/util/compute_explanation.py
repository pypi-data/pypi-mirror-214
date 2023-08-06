# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2023  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import base64
import uuid
import json
from math import isnan
from decimal import Decimal
import pandas as pd
from collections import OrderedDict
from random import sample
try:
    from pyspark.sql import Row
except ImportError as e:
    pass

from more_itertools import ichunked
from ibm_metrics_plugin.metrics.explainability.entity.constants import DEFAULT_CHUNK_SIZE, Status
from ibm_wos_utils.explainability.utils.date_time_util import DateTimeUtil


class ComputeExplanation():

    def __init__(self, config, explainer, subscription, columns, global_exp_accumulator, explanations_counter, data_chunk_size=DEFAULT_CHUNK_SIZE, created_by="openscale", local_exps_dist_accumulator=None, local_exps_dist_frac=None, **kwargs):
        self.config = config
        self.explainer = explainer
        self.subscription = subscription
        self.columns = columns
        self.global_exp_accumulator = global_exp_accumulator
        self.explanations_counter = explanations_counter
        self.data_chunk_size = data_chunk_size
        self.created_by = created_by
        self.local_exps_dist_accumulator = local_exps_dist_accumulator
        self.local_exps_dist_frac = local_exps_dist_frac
        self.kwargs = kwargs

    def compute(self, data):
        chunks = ichunked(data, self.data_chunk_size)
        for chunk in chunks:
            df = pd.DataFrame(chunk, columns=self.columns)
            response = self.explainer.explain(data=df, **self.kwargs)
            local_exps = response.get("local_explanations")
            exp_rows = []
            if self.subscription:
                df["explanation"] = local_exps
                for _, row in df.iterrows():
                    created_at = DateTimeUtil.get_current_datetime()
                    exp_rows.append(self.get_response_row(row, created_at))

            if self.global_exp_accumulator:
                self.global_exp_accumulator.add(self.explainer.get_data_to_accumulate(
                    response))

            if self.local_exps_dist_accumulator and self.local_exps_dist_frac:
                if self.subscription:
                    local_exps_dist = self.__get_sample_exps(exp_rows)
                else:
                    local_exps_dist = self.__get_sample_exps(local_exps)

                self.local_exps_dist_accumulator.add(
                    {"local_explanations": local_exps_dist})
            if self.subscription:
                for r in exp_rows:
                    yield r

    def __get_sample_exps(self, exp_rows):
        exp_rows_len = len(exp_rows)
        sample_size = int(exp_rows_len *
                          self.local_exps_dist_frac)
        if exp_rows_len > sample_size:
            return sample(exp_rows, int(exp_rows_len*self.local_exps_dist_frac))
        else:
            return exp_rows

    def get_response_row(self, row, created_at):

        explanations = [row["explanation"]]
        status = Status.ERROR if all(
            e.get("error") for e in explanations) else Status.FINISHED
        scoring_id = row[self.subscription.scoring_id_column]
        if self.explanations_counter:
            counter_dict = {
                "failed": 1 if status is Status.ERROR else 0,
                "total": 1,
                "failed_scoring_ids": [scoring_id] if status is Status.ERROR else []
            }
            self.explanations_counter.add(counter_dict)

        errors = []
        for e in explanations:
            if e.get("error"):
                errors.append(e.get("error"))
                del e["error"]

        return Row(asset_name=self.subscription.asset_name,
                   binding_id=self.subscription.binding_id,
                   created_at=created_at,
                   created_by=self.created_by,
                   data_mart_id=self.subscription.data_mart_id,
                   deployment_id=self.subscription.deployment_id,
                   deployment_name=self.subscription.deployment_name,
                   error=bytearray(base64.b64encode(json.dumps(errors).encode(
                       "utf-8"))) if errors else None,
                   explanation=self.__encode_explanations(row, explanations),
                   explanation_input=None,
                   explanation_output=None,
                   explanation_type=self.config.metric_types[0].value,
                   finished_at=DateTimeUtil.get_current_datetime(),
                   object_hash=self.__get_object_hash(row),
                   prediction=row[self.config.prediction_column],
                   probability=max(row[self.config.probability_column]
                                   ) if self.config.probability_column in row else None,
                   request_id=row["explanation_task_id"] if "explanation_task_id" in row else str(
                       uuid.uuid4()),
                   scoring_id=scoring_id,
                   status=status.name,
                   subscription_id=self.subscription.subscription_id)

    def __encode_explanations(self, row, explanations):
        input_features = []
        meta_features = []
        for f in self.config.features:
            val = row[f]
            if f in self.config.categorical_features:
                ftype = "categorical"
            else:
                ftype = "numerical"
                val = None if val is None or isnan(val) else val

            input_features.append({"name": f,
                                   "value": float(val) if isinstance(val, Decimal) else val,
                                   "feature_type": ftype})
        if self.config.meta_fields:
            for meta_field in self.config.meta_fields:
                meta_val = row[meta_field]
                meta_features.append(
                    {"name": meta_field, "value": meta_val})

        entity = {"entity": {
            "asset": {
                "id": self.subscription.asset_id,
                "name": self.subscription.asset_name,
                "problem_type": self.config.problem_type.value,
                "input_data_type": self.config.input_data_type.value,
                "deployment": {
                    "id": self.subscription.deployment_id,
                    "name": self.subscription.deployment_name
                }
            },
            "input_features": input_features,
            "meta_features": meta_features,
            "explanations": explanations
        }}
        return bytearray(base64.b64encode(json.dumps(entity).encode("utf-8")))

    def __get_object_hash(self, row):
        feature_values = {f: row[f]
                          for f in self.config.features}

        feature_values_sorted = OrderedDict(
            sorted(feature_values.items()))
        # convert the dict to a single row rectangular dataframe and get hash for first row
        feature_row_df = pd.DataFrame(feature_values_sorted, index=[0])
        return str(abs(pd.util.hash_pandas_object(
            feature_row_df, encoding="utf8").iloc[0]))
