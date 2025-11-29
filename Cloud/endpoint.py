import os
import sagemaker, boto3
from sagemaker import get_execution_role
from sagemaker.pytorch import PyTorchModel

role = get_execution_role()

model_uri = f"s3://"
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