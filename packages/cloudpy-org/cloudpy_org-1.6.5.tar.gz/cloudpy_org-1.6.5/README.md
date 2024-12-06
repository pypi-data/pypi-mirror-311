* Free software: MIT license

# cloudpy_org
A library to programmatically create, interact, encrypt and automate your data pipelines making it simple to scale to the most popular cloud plattforms.

### Installation
```
pip install cloudpy_org
```
### Documentation

https://www.cloudpy.org

### Get started
How to call the different tools from cloudpy_org
```Python
import cloudpy_org as co 
#for local usage only
pt = co.processing_tools()
#for aws framework usage
aws = co.cloudpy_org_aws_framework_client(aws_namespace='my_aws_namespace',env='dev or prod')
#This requires a cloudpy_org service token. Check https://www.cloudpy.org for more info.
```
