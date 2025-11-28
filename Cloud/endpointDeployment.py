import sagemaker
from sagemaker.huggingface import HuggingFaceModel

# 1. Setup Permissions
# If running locally, ensure you have ran `aws configure`
# If running on SageMaker Notebook, use get_execution_role()
try:
    role = sagemaker.get_execution_role()
except ValueError:
    import boto3
    iam = boto3.client('iam')
    # Replace with your actual SageMaker execution role name if running locally
    role = iam.get_role(RoleName='YourSageMakerExecutionRole')['Role']['Arn']

# 2. Configure the Model
# We use a standard Hugging Face PyTorch container
huggingface_model = HuggingFaceModel(
    role=role,
    transformers_version='4.37.0', # reliable version
    pytorch_version='2.1.0',       
    py_version='py310',
    entry_point='inference.py',    # Points to your custom script
    source_dir='code',             # Points to the folder with inference.py
    # We do NOT set HF_MODEL_ID here because we load it manually in model_fn
    # to handle 'trust_remote_code=True' explicitly.
)

# 3. Deploy the Endpoint
print("Deploying model... This will take 5-10 minutes.")
predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type='ml.m5.xlarge' # CPU instance (cheaper). Use 'ml.g4dn.xlarge' for GPU.
)

print(f"\nEndpoint deployed! Name: {predictor.endpoint_name}")