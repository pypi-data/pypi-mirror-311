import importlib

from diffusers import DiffusionPipeline


def parallelize_transformer(transformer, *args, **kwargs) -> None:
    transformer_cls_name = transformer.__class__.__name__
    if transformer_cls_name.startswith("Flux"):
        adapter_name = "flux"
    elif transformer_cls_name.startswith("Mochi"):
        adapter_name = "mochi"
    elif transformer_cls_name.startswith("CogVideoX"):
        adapter_name = "cogvideox"
    else:
        raise ValueError(f"Unknown transformer class name: {transformer_cls_name}")

    adapter_module = importlib.import_module(f".{adapter_name}", __package__)
    parallelize_transformer_fn = getattr(adapter_module, "parallelize_transformer")
    parallelize_transformer_fn(transformer, *args, **kwargs)


def parallelize_pipe(pipe: DiffusionPipeline, *args, **kwargs) -> None:
    assert isinstance(pipe, DiffusionPipeline)

    pipe_cls_name = pipe.__class__.__name__
    if pipe_cls_name.startswith("Flux"):
        adapter_name = "flux"
    elif pipe_cls_name.startswith("Mochi"):
        adapter_name = "mochi"
    elif pipe_cls_name.startswith("CogVideoX"):
        adapter_name = "cogvideox"
    else:
        raise ValueError(f"Unknown pipeline class name: {pipe_cls_name}")

    adapter_module = importlib.import_module(f".{adapter_name}", __package__)
    parallelize_pipe_fn = getattr(adapter_module, "parallelize_pipe")
    parallelize_pipe_fn(pipe, *args, **kwargs)
