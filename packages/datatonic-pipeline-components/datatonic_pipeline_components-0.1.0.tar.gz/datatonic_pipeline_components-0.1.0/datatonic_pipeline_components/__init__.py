import os
from kfp.components import load_component_from_file

gpt_tokenize = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "gpt_tokenize/gpt_tokenize/component.yaml")
)
load_huggingface_tensorflow = load_component_from_file(
    os.path.join(
        os.path.dirname(__file__),
        "load_huggingface_tensorflow/load_huggingface_tensorflow/component.yaml",
    )
)
load_huggingface_torch = load_component_from_file(
    os.path.join(
        os.path.dirname(__file__),
        "load_huggingface_torch/load_huggingface_torch/component.yaml",
    )
)
upload_pytorch_model = load_component_from_file(
    os.path.join(
        os.path.dirname(__file__),
        "upload_pytorch_model/upload_pytorch_model/component.yaml",
    )
)
xgboost_shap_gpu = load_component_from_file(
    os.path.join(os.path.dirname(__file__), "xgboost_shap_gpu/component.yaml")
)
