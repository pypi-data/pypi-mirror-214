from typing import Literal
import a2.training.training_hugging

SUPPORTED_MODELS: Literal = ["deberta_base", "deberta_small", "electra_base"]

def get_model_config(model_name: SUPPORTED_MODELS):
    if model_name == "deberta_base" or model_name == "deberta_small":
        hyper_parameters = a2.training.training_hugging.HyperParametersDebertaClassifier()
    elif model_name == "electra_base":
        hyper_parameters = a2.training.training_hugging.HyperParametersElectraClassifier()
    else:
        raise ValueError(f"{model_name=} not supported, ({SUPPORTED_MODELS=})!")
    return hyper_parameters
