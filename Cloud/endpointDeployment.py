import sagemaker
from sagemaker.pytorch import PyTorchModel


role = sagemaker.get_execution_role()

model = PyTorchModel(
    entry_point="inference.py",
    source_dir="code",
    role=role,
    framework_version="2.0",
    py_version="py310",
    env={"SAGEMAKER_PROGRAM": "inference.py"},
)

print("Deploying endpoint... -> InsightFace Onnx")
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.c5.xlarge",
    endpoint_name="insightface-onnx-endpoint",
)

print(f"Endpoint deployed at: {predictor.endpoint_name}")