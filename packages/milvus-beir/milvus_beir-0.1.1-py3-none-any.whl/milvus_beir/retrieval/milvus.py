import logging
from typing import Dict, List
from tqdm.autonotebook import tqdm
from pymilvus import (connections, Collection, FieldSchema, CollectionSchema,
                      DataType, utility, FunctionType, Function, AnnSearchRequest, WeightedRanker)
import numpy as np
from pandas import DataFrame

logger = logging.getLogger(__name__)

from abc import ABC, abstractmethod
from typing import Dict


class BaseSearch(ABC):

    @abstractmethod
    def search(self,
               corpus: Dict[str, Dict[str, str]],
               queries: Dict[str, str],
               top_k: int,
               **kwargs) -> Dict[str, Dict[str, float]]:
        pass


class SearchType:
    DENSE = "dense"
    FTS = "fts"
    HYBRID = "hybrid"


class MilvusSearch(BaseSearch):
    def __init__(self, collection_name: str, nq: int = 100, nb: int = 2000, uri: str = "localhost",
                 token: str = "19530",
                 search_type: str = "dense", initialize: bool = True, schema: CollectionSchema = None):
        self.nq = nq
        self.nb = nb
        self.collection_name = collection_name
        self.uri = uri
        self.token = token
        self.schema = schema
        self.initialize = initialize
        self.collection = None
        self.results = {}
        self.search_type = search_type
        if self.schema is None:
            self.schema = self._create_schema()
        self.connection = connections.connect(uri=self.uri, token=self.token)
        if self.initialize:
            self.init_collection()
        else:
            self.collection = Collection(name=self.collection_name)
        assert search_type in ["dense", "fts" "hybrid"], "Invalid search type"

    def _create_schema(self):
        analyzer_params = {
            "type": "english",
        }
        fields = [
            FieldSchema(name="_id", dtype=DataType.VARCHAR, max_length=10000, is_primary=True),
            FieldSchema(name="document", dtype=DataType.VARCHAR, max_length=65535,
                        enable_analyzer=True, analyzer_params=analyzer_params),
            FieldSchema(name="document_sparse_emb", dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(name="dense_emb", dtype=DataType.FLOAT_VECTOR, dim=1028),
        ]
        schema = CollectionSchema(fields=fields, description="beir test collection")
        for field in ["document"]:
            bm25_function = Function(
                name=f"{field}_bm25_emb",
                function_type=FunctionType.BM25,
                input_field_names=[field],
                output_field_names=[f"{field}_sparse_emb"],
                params={},
            )
            schema.add_function(bm25_function)
        schema = CollectionSchema(fields, description=f"BEIR collection for {self.search_type} search")
        return schema

    def init_collection(self):
        has = utility.has_collection(self.collection_name)
        if has:
            logging.info(f"Collection {self.collection_name} already exists, will drop it")
            utility.drop_collection(self.collection_name)
        self.collection = Collection(name=self.collection_name, schema=self.schema)
        # init index
        self.init_index()

    def init_index(self):
        fields = self.schema.fields
        float_vec_field = [field for field in fields if
                           field.dtype in [DataType.FLOAT_VECTOR, DataType.FLOAT16_VECTOR, DataType.BFLOAT16_VECTOR]]
        binary_vec_field = [field for field in fields if field.dtype in [DataType.BINARY_VECTOR]]

        functions = self.schema.functions
        bm25_func = [func for func in functions if func.type == FunctionType.BM25]
        bm25_outputs = []
        for func in bm25_func:
            bm25_outputs.extend(func.output_field_names)
        bm25_outputs = list(set(bm25_outputs))
        fts_vec_field = bm25_outputs
        sparse_vec_field = [field for field in fields if field.dtype in [DataType.SPARSE_FLOAT_VECTOR]
                            and field.name not in fts_vec_field]
        for field in float_vec_field:
            index_params = {"index_type": "AUTOINDEX", "metric_type": "COSINE", "params": {}}
            self.collection.create_index(field.name, index_params)
        for field in binary_vec_field:
            index_params = {"index_type": "BIN_IVF_FLAT", "metric_type": "JACCARD", "params": {"M": 48}}
            self.collection.create_index(field.name, index_params)
        for field in sparse_vec_field:
            index_params = {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "IP", "params": {}}
            self.collection.create_index(field.name, index_params)
        for field in fts_vec_field:
            index_params = {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "BM25",
                            "params": {"bm25_k1": 1.2, "bm25_b": 0.75}}
            self.collection.create_index(field, index_params)
        self.collection.load()

    def index(self, corpus: DataFrame):
        batch_size = self.nb
        total_rows = len(corpus)
        corpus["document"] = corpus["title"] + " " + corpus["text"]
        corpus = corpus.drop(columns=["title", "text"])
        for start in tqdm(range(0, total_rows, batch_size)):
            end = min(start + batch_size, total_rows)
            batch = corpus.iloc[start:end]
            records = batch.to_dict('records')
            self.collection.insert(records)

    def search(self, queries: DataFrame, top_k: int, **kwargs) -> Dict[str, Dict[str, float]]:

        if self.search_type == SearchType.DENSE:
            return self.embedding_dense_search(queries, top_k)
        elif self.search_type == SearchType.FTS:
            return self.full_text_search(queries, top_k)
        elif self.search_type == SearchType.HYBRID:
            return self.hybrid_search(queries, top_k)
        else:
            raise ValueError("Invalid search type")

    def full_text_search(self, queries: DataFrame, top_k: int) -> Dict[str, Dict[str, float]]:
        batch_size = self.nq
        total_rows = len(queries)
        result_list = []
        for start in tqdm(range(0, total_rows, batch_size)):
            end = min(start + batch_size, total_rows)
            batch = queries.iloc[start:end]
            texts = batch["document"].tolist()
            result = self.collection.search(data=texts,
                                            anns_field="document_sparse",
                                            param={},
                                            limit=top_k,
                                            output_fields=["_id"])
            result_list.extend(result)
        result_dict = {}
        for i in range(len(queries)):
            data = {}
            for hit in result_list[i]:
                data[hit.id] = hit.distance
            result_dict[queries[i]["id"]] = data
        return result_dict

    def embedding_dense_search(self, queries: DataFrame, top_k: int) -> Dict[str, Dict[str, float]]:
        batch_size = self.nq
        total_rows = len(queries)
        result_list = []
        for start in tqdm(range(0, total_rows, batch_size)):
            end = min(start + batch_size, total_rows)
            batch = queries.iloc[start:end]
            embeddings = batch["emb"].tolist()
            result = self.collection.search(data=embeddings,
                                            anns_field="dense_emb",
                                            param={},
                                            limit=top_k,
                                            output_fields=["_id"])
            result_list.extend(result)
        result_dict = {}
        for i in range(len(queries)):
            data = {}
            for hit in result_list[i]:
                data[hit.id] = hit.distance
            result_dict[queries[i]["id"]] = data
        return result_dict

    def hybrid_search(self, queries: DataFrame, top_k: int) -> Dict[str, Dict[str, float]]:
        batch_size = self.nq
        total_rows = len(queries)
        result_list = []
        for start in tqdm(range(0, total_rows, batch_size)):
            end = min(start + batch_size, total_rows)
            batch = queries.iloc[start:end]
            embeddings = batch["emb"].tolist()
            texts = batch["document"].tolist()
            fts_search_req = AnnSearchRequest(
                data=texts,
                anns_field="document_sparse_emb",
                param={},
                limit=top_k,
            )
            dense_search_req = AnnSearchRequest(
                data=embeddings,
                anns_field="dense_emb",
                param={},
                limit=top_k,
            )
            result = self.collection.hybrid_search(
                reqs=[fts_search_req, dense_search_req],
                rerank=WeightedRanker(0.5, 0.5),
                limit=top_k,
                output_fields=["_id"]
            )
            result_list.extend(result)
        result_dict = {}
        for i in range(len(queries)):
            data = {}
            for hit in result_list[i]:
                data[hit.id] = hit.distance
            result_dict[queries[i]["id"]] = data
        return result_dict
