import os
import sagemaker, boto3
from sagemaker import get_execution_role
from sagemaker.pytorch import PyTorchModel

role = get_execution_role()
sess = sagemaker.Session()
bucket = sess.default_bucket()

tarFile = 'model.tar.gz'
s3 = boto3.client('s3')
s3.upload_file(
    FileName=tarFile,
    Bucket=bucket,
    Key=os.path.basename(tarFile)
)

model_uri = f"s3://{bucket}/{os.path.basename(tarFile)}"
entryPoint = "inference.py"

model = PyTorchModel(
    model_data=model_uri,
    role=role,
    entry_point=entryPoint,
    framework_version='2.0',
    py_version='py310',
    sagemaker_session=sess,
)

endpointName = 'oguri-face'
instanceType = 'ml.m5.xlarge'
predictor = model.deploy(
    initial_instance_count=1,
    instance_type=instanceType,
    endpoint_name=endpointName,
    serializer=sagemaker.serializers.JSONSerializer(),
    deserializer=sagemaker.deserializers.JSONDeserializer(),
    )