#!/usr/bin/python3
r"""
Author: Alex Cooper
Date: 04/18/2026
Name: libsafe_parser.py
Purpose: Parse Keep csv to create csv's for Libsafe
"""

import sys
import pandas as pd
from pathlib import Path
import requests

def create_collection_csv(df,my_set,mp):
    df.fillna('', inplace=True)
    df.rename(columns={'collection_source_id':'local_call_number','date_created':'date_createdx','coverage':'date_created','rights':'rights_statement','content_md5':'md5'}, inplace=True)
    df['holding_repository'] = "Stuart A. Rose Manuscript, Archives, and Rare Book Library"
    df['content_type'] = "Mixed material"
    df['primary_language'] = ""
    df['note'] = df['description'].astype(str) + '|' + df['hasDerivation'].astype(str) + '|' + df['isDerivationOf'].astype(str)
    df['rights_statement_controlled'] = ""
    df['restrictions'] = "Preservation copy; no researcher access without further review."
    df['ref_id'] = ""
    df['component_id'] = ""
    df['acc_number'] = ""

    for item in my_set:
        collection = item
        read_it = df.loc[df['collection_label'] == collection]
        collection = str(collection)
        collection = collection.replace(" ", "_").replace("'", "").replace("\"", "").replace("(", "").replace(")", "").replace("?", "").replace("[", "").replace("]", "").replace("!", "").replace("&", "")
        filename2 = f"{collection}.csv"
        output2 = Path("/alma/integrations/libsafe_out/collections") / filename2
        read_it.to_csv(output2, mode='a', columns=['title', 'local_call_number', 'holding_repository', 'content_type', 'creator', 'date_created', 'primary_language', 'note', 'rights_statement', 'rights_statement_controlled', 'restrictions', 'ref_id', 'component_id', 'acc_number', 'pid', 'md5'], index=False, header=True)

    filename = f"libsafe.csv"
    output = Path("/alma/integrations/libsafe_out/collections") / filename
    df.to_csv(output, mode='a', columns=['title', 'local_call_number', 'holding_repository', 'content_type', 'creator', 'date_created', 'primary_language', 'note', 'rights_statement', 'rights_statement_controlled', 'restrictions', 'ref_id', 'component_id', 'acc_number', 'pid', 'md5'], index=False, header=True)
    return

def parse_rows(df):
    mc = "/alma/integrations/libsafe_out/collections/my.csv"
    mc = pd.read_csv(mc)
    for index, row in mc.iterrows():
        my_pid = row['pid']
        my_pid = my_pid.lstrip("emory:")
        filename = f"{my_pid}_KeepMetadata.csv"
        output = Path("/alma/integrations/libsafe_out/rows") / filename
        row.to_frame().T.to_csv(output, index=False, header=True)
    return

def parse_collection(df,my_set,mp):
    mc = Path("/alma/integrations/libsafe_out/collections/my.csv")
    header = "/alma/integrations/keep_in/header.csv"
    header = pd.read_csv(header)
    header.to_csv(mc, mode='a', index=False, header=True)
    for item in my_set:
        collection = item
        identifier = mp.loc[mp['Title'] == collection, ['Identifier']]
        identifier = identifier.to_string(index=False, header=False).lstrip(" ")
        container = mp.loc[mp['Title'] == collection, ['Container ID']]
        container = container.to_string(index=False, header=False).lstrip(" ")
        df['Identifier'] = identifier
        df['Container ID'] = container
        read_it = df.loc[df['collection_label'] == collection]
        filename = f"my.csv"
        output = Path("/alma/integrations/libsafe_out/collections") / filename
        read_it.to_csv(output, mode='a', index=False, header=False)
    return

def main():
    my_csv = "/alma/integrations/keep_in/test_me.csv"
#    my_csv = "/alma/integrations/keep_in/disk_images_all_fields_report_04_15_26.csv"
    my_mapping = "/alma/integrations/keep_in/mapping.csv"
    df = pd.read_csv(my_csv)
    column_values = df['collection_label'].tolist()
    my_set = set(column_values)
    mp = pd.read_csv(my_mapping)
    parse_collection(df,my_set,mp)
    parse_rows(df)
    create_collection_csv(df,my_set,mp)

if __name__=="__main__":
    sys.exit(main())
