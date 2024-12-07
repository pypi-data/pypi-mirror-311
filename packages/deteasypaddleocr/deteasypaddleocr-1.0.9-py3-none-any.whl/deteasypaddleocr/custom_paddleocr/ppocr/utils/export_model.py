import os
import yaml
import copy
import paddle
from collections import OrderedDict
from ppocr.modeling.architectures import build_model
from ppocr.utils.save_load import load_model
from ppocr.utils.logging import get_logger


def represent_dictionary_order(self, dict_data):
    return self.represent_mapping("tag:yaml.org,2002:map", dict_data.items())


def setup_orderdict():
    yaml.add_representer(OrderedDict, represent_dictionary_order)


def dump_infer_config(config, path, logger):
    setup_orderdict()
    infer_cfg = OrderedDict()
    if config["Global"].get("hpi_config_path", None):
        hpi_config = yaml.safe_load(open(config["Global"]["hpi_config_path"], "r"))
        if hpi_config["Hpi"]["backend_config"].get("paddle_tensorrt", None):
            hpi_config["Hpi"]["supported_backends"]["gpu"].remove("paddle_tensorrt")
            del hpi_config["Hpi"]["backend_config"]["paddle_tensorrt"]
        if hpi_config["Hpi"]["backend_config"].get("tensorrt", None):
            hpi_config["Hpi"]["supported_backends"]["gpu"].remove("tensorrt")
            del hpi_config["Hpi"]["backend_config"]["tensorrt"]
        hpi_config["Hpi"]["selected_backends"]["gpu"] = "paddle_infer"
        infer_cfg["Hpi"] = hpi_config["Hpi"]

    infer_cfg["PreProcess"] = {"transform_ops": config["Eval"]["dataset"]["transforms"]}

    with open(path, "w") as f:
        yaml.dump(
            infer_cfg, f, default_flow_style=False, encoding="utf-8", allow_unicode=True
        )
    logger.info("Export inference config file to {}".format(os.path.join(path)))


def export_single_model(
    model, arch_config, save_path, logger, input_shape=None, quanter=None
):
    if arch_config["model_type"] != "sr" and arch_config["Backbone"]["name"] == "PPLCNetV3":
        # for rep lcnetv3
        for layer in model.sublayers():
            if hasattr(layer, "rep") and not getattr(layer, "is_repped"):
                layer.rep()

    if quanter is None:
        paddle.jit.save(model, save_path)
    else:
        quanter.save_quantized_model(model, save_path)
    logger.info("inference model is saved to {}".format(save_path))
    return


def export(config, base_model=None, save_path=None):
    if paddle.distributed.get_rank() != 0:
        return
    logger = get_logger()

    # build model
    model = build_model(config["Architecture"])
    load_model(config, model, model_type=config["Architecture"]["model_type"])
    model.eval()

    if not save_path:
        save_path = config["Global"]["save_inference_dir"]
    yaml_path = os.path.join(save_path, "inference.yml")

    arch_config = config["Architecture"]

    save_path = os.path.join(save_path, "inference")
    export_single_model(
        model, arch_config, save_path, logger
    )
    dump_infer_config(config, yaml_path, logger)