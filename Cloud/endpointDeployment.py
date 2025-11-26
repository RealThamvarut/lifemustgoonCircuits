import sagemaker
from sagemaker.tensorflow import TensorFlowModel 

#iam
role = 'arn:aws:iam::ACCOUNT_ID:role/service-role/AmazonSageMaker-ExecutionRole'
sess = sagemaker.Session()
bucket = sess.default_bucket()

model_data = sess.upload_data(
    path='model/model.tar.gz', 
    bucket=bucket, 
    key_prefix='model/deepface-endpoint' 
)

model = TensorFlowModel(
    model_data=model_data,
    role=role,
    framework_version='2.11.0',
    py_version='py39',
    entry_point='inference.py',
    source_dir='model/code',
    )

#deploy the model
from sagemaker.serverless import ServerlessInferenceConfig

serverlessConfig = ServerlessInferenceConfig(
    memory_size_in_mb=4096,
    max_concurrency=5,
)
print("deploying endpoint...")
predictor = model.deploy(
    endpoint_name='deepface-endpoint',
    serverless_inference_config=serverlessConfig
)

print("deployed endpoint successfully. i guess?")
