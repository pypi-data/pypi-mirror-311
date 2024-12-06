from re import T
import time

from flask import app

from citybrain_platform import JobStatus
import citybrain_platform
from citybrain_platform import Column, ColumnType
from citybrain_platform.computing import data_types
from citybrain_platform.computing.data_types import ExternalFiletype, ResourceType


citybrain_platform.api_key = "MiQxNjkyMTU1Nzk3JGJxaXplaXRu"
citybrain_platform.api_baseurl = "http://127.0.0.1:8080/platform/"

# result = citybrain_platform.Computing.create_resource(
#     name="add.py",
#     type=ResourceType.PY,
#     comment="for add",
#     local_file="udf.py"
# )
# print(result)


# result = citybrain_platform.Computing.create_function(
#     name="test_udf_add3",
#     class_file="add.py",
#     class_name="MyPlus",
#     comment="test add function",
#     resources=["add.py"]
# )
# print(result)

# citybrain_platform.Computing.update_table_status(name="mbt_test1130", public=True)


# upload parquet file to storage service
# res = citybrain_platform.Storage.upload_file(
#     remote_path="tbl_test_cmip/user_storage_1_cmiptest_cmip6_ta_Amon_IITM-ESM_ssp585_r1i1p1f1_gn_208501-209412.nc.gzip", 
#     local_file="user_storage_1_cmiptest_cmip6_ta_Amon_IITM-ESM_ssp585_r1i1p1f1_gn_208501-209412.nc.gzip"
# )
# print(res)

# create table using files from storage service
# columns = [
#     Column("cfc113global", ColumnType.DOUBLE, ""),
#     Column("time_bnds", ColumnType.TIMESTAMP, ""),
#     Column("time", ColumnType.TIMESTAMP, ""),
#     Column("bnds", ColumnType.DOUBLE, "")
# ]

# res = citybrain_platform.Computing.create_table(
#     name="tbl_test_cmip", 
#     columns=columns,
#     description="test table",
#     storage_filesource="/tbl_test_cmip",
#     storage_filetype=data_types.ExternalFiletype.PARQUET
# );
# print(res);

# job_id = citybrain_platform.Computing.create_job("select test_udf_add3(12, 14);")
# print(job_id);

# # make a select query
# status = citybrain_platform.Computing.get_job_status(job_id='99c1ce12-6a45-48f8-9685-6115093bfaff');
# print(status);

# # get results of the query
citybrain_platform.Computing.get_job_results(job_id='99c1ce12-6a45-48f8-9685-6115093bfaff', filepath="tbl_test_cmip21.csv", header=True)


# res = citybrain_platform.Storage.delete_file(remote_path="fawda/fsaw/a.csv")
# print(res)

# res = citybrain_platform.Storage.list_files(prefix="", direct_only=False)
# print(res)

# res = citybrain_platform.Storage.upload_file(remote_path="testaa/a.csv", local_file="a.csv")
# print(res)


# citybrain_platform.Storage.download_file(remote_path="fawda/faw/a.csv", local_file="b.csv")


columns = [
    Column("id1", ColumnType.INT, "aa"),
    Column("id2", ColumnType.INT, "bb"),
]

# create table
# ok = citybrain_platform.Computing.create_table(name="mbt_testaaaa", columns=columns, description="ssdad")
# print(ok)

# result = citybrain_platform.Computing.upload_table_data(name="mbt_testaaa", append=True, csv_filepath="a.csv")
# print(result)

# partition_columns = [
#     Column("col_pt", ColumnType.INT, "ppt")
# ]

# job_id=citybrain_platform.Computing.create_job("select * from mbt_testaaa limit 12;")
# print(job_id)
# print(citybrain_platform.Computing.get_job_status(job_id='18bf62d1-d9c9-41cd-8e74-a1f064381e89'))
# citybrain_platform.Computing.get_job_results(job_id='18bf62d1-d9c9-41cd-8e74-a1f064381e89', filepath="testaa.csv")

# columns = [
#     Column("time", ColumnType.TIMESTAMP, ""),
#     Column("bnds", ColumnType.BIGINT, ""),
#     Column("plev", ColumnType.DOUBLE, ""),
#     Column("lat", ColumnType.DOUBLE, ""),
#     Column("lon", ColumnType.DOUBLE, ""),
#     Column("time_bnds", ColumnType.TIMESTAMP, ""),
#     Column("lat_bnds", ColumnType.DOUBLE, ""),
#     Column("lon_bnds", ColumnType.DOUBLE, ""),
#     Column("ta", ColumnType.DOUBLE, ""),
# ]


# create table
# ok = citybrain_platform.Computing.create_table(name="mbt_testcmip6", columns=columns, description="ssdad", storage_filesource="cmiptest/", storage_filetype=ExternalFiletype.PARQUET)
# print(ok)

# get table schema
# schema = citybrain_platform.Computing.get_table_schema(name="mbt_test4")
# print(schema)

# upload data to table
# result = citybrain_platform.Computing.upload_table_data(name="mbt_test2", append=True, csv_filepath="aa.csv", partition_key={"col_pt": "19"})
# print(result)

# truncate table
# result = citybrain_platform.Computing.truncate_table(name="mbt_test1", partition_key={"col_pt": "1"})
# print(result)

# drop table
# result = citybrain_platform.Computing.drop_table(name="mbt_test2")
# print(result)

# public table
# public_table_name = citybrain_platform.Computing.public_table(name="mbt_test1")
# print(public_table_name)

# get available table list
# result = citybrain_platform.Computing.list_tables()
# print(result)

# create sql job
# job_id = citybrain_platform.Computing.create_job(
#     sql="select osmid from osm_node where osmid between 80080000 and 80081000;",
#     worker_limit=100,
#     split_size=256
# )
# print(job_id)

# stop running job
# result = citybrain_platform.Computing.stop_job(job_id="fab7b329-aef9-4c96-a9ac-1b47b1468e79")
# print(result)

# get job status
# job_status = citybrain_platform.Computing.get_job_status(job_id="e5597f65-b12a-4c3f-bb36-6cd742ec9b44")
# print(job_status)


# job_id = citybrain_platform.Computing.create_job(sql="select * from eric.zhang.city_Oklahoma limit 10;")
# print(job_id)

# get job results
# citybrain_platform.Computing.get_job_results(job_id="dc9132b8-8697-4c1e-9e77-796eb0ec7584", filepath="a.csv")


# sqlresult = "select * from cesm_ass1_50year_0730 limit 1000"
# jobresult_id = citybrain_platform.Computing.create_job(sql=sqlresult)

# while True:
#     status = citybrain_platform.Computing.get_job_status(job_id=jobresult_id)
#     print(status.status)
#     if status.status == JobStatus.RUNNING:
#         print(status.progress)
#     if status.status == JobStatus.TERMINATED:
#         break
#     time.sleep(1)

# print("downloading result")
# citybrain_platform.Computing.get_job_results(job_id=jobresult_id, filepath="cesm_ass1_50year_0730.csv")

# citybrain_platform.Data.download(data_address="174B948F17421000", save_file="a.txt")
