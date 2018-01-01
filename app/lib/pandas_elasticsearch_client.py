"""Unit tests for the Espandas class"""

import pandas as pd
import numpy as np
from espandas import Espandas
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError, ConnectionError
import app.config as config

# ES variables
INDEX = 'unit_tests_index'
TYPE = 'foo_bar'

# Example data frame
df = (100 * pd.DataFrame(np.round(np.random.rand(100, 5), 2))).astype(int)
df.columns = ['A', 'B', 'C', 'D', 'E']
df['indexId'] = df.index + 100
df = df.astype('str')
print df

def create_es():
    """
    Before running other tests, ensure connection to ES is established
    """
    es = Elasticsearch([config.ES_HOST],
                                http_auth=('admin', 'admin'),
                                port=config.ES_PORT)
    try:

        es.indices.create(INDEX)
        es.indices.delete(INDEX)
        return True
    except RequestError:
        print('Index already exists: skipping tests.')
        return False
    except ConnectionError:
        print('The ElasticSearch backend is not running: skipping tests.')
        return False
    except Exception as e:
        print('An unknown error occured connecting to ElasticSearch: %s' % e)
        return False


def es_client():
    """
    Insert a DataFrame and test that is is correctly extracted
    """
    # Only run this test if the index does not already exist
    # and can be created and deleted
    if create_es():
        try:
            print('Connection to ElasticSearch established: testing write and read.')
            es = Elasticsearch([config.ES_HOST],
                                http_auth=('admin', 'admin'),
                                port=config.ES_PORT)

            es.indices.create(INDEX)

            esp = Espandas(es)
            esp.es_write(df, INDEX, TYPE)
            k = list(df['indexId'].astype('str'))
            res = esp.es_read(k, INDEX, TYPE)

            # The returned DataFrame should match the original
            print res


        finally:
            # Cleanup
            es.indices.delete(INDEX)

es_client()