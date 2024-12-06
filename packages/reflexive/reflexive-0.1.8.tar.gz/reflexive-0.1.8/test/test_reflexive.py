# Add the source path for testing
import os
import sys
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"reflexive/src"
)
sys.path.append(SOURCE_PATH)

import pandas as pd
import reflexive as rfx

# account_number,region,name_prefix="refex_",local_path=None,date_string=None
params = rfx.Parameters('432433400321','ap-southeast-2',name_prefix="nov03",local_path="/workspaces/python_dev/reflexive/test/data")
params.set_s3_parameters('qut-gibsonap-reflexive',"au-edu-qld-qut-gibsonap-reflexive")
params.set_comprehend_parameters("AmazonComprehendServiceRole-gibsonap-reflexive")
params.set_comprehend_custom_entity_parameters("ReflexiveExpressionRecogniser","v17")

#print(params.all_parameters())

test_dict = {"text":["This is a test text. I hope that this will work for some basic analysis. Previously, this has not been as straight forward as I thought. Perhaps this time may be different. With any luck, this will not be a frustrating experience, but will just work straight away. I can only hope!"]}
test_series = pd.Series(test_dict['text'])

aws_s3 = rfx.S3(params)
#s3_client = aws_s3.client()

#s3_resp = aws_s3.upload_docs(test_series)
#print(s3_resp)

# Save locally
local = rfx.Local(params)
local.set_sub_dir("docs")
#local.save_docs(test_series,"docs")

aws_comp = rfx.Comprehend(params)
#comp_client = aws_comp.client()

# refex = rfx.ReflexiveExpressions(params,aws_s3,local,aws_comp)
# df = pd.DataFrame.from_dict(test_dict)
# response = refex.analyse_reflexive_expressions(df)
# print(response)

vis = rfx.Display()
print(vis.options)