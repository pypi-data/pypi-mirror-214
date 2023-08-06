import importlib
import os

import yaml
from yaml.loader import SafeLoader

from kaxi import log as logger


class Runner:
    def __init__(self, settings: dict):
        self._settings = settings

    @classmethod
    def from_yaml(cls, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} not found")

        with open(filename) as f:
            settings = yaml.load(f, Loader=SafeLoader)

        return cls(settings)

    @property
    def steps(self) -> dict:
        return self._steps

    @property
    def settings(self) -> dict:
        return self._settings

    def update_params(self, params: dict):
        if isinstance(params, dict):
            output = {}
            for key, value in params.items():
                output[key] = self.update_params(value)

            return output
        elif isinstance(params, list):
            return [self.update_params(v) for v in params]
        elif isinstance(params, str):
            if params.startswith("${") and params.endswith("}"):
                if params[2:-1] not in self._memory:
                    logger.error(f"Missing memory value: {params[2:-1]}")
                    raise ValueError(f"Missing memory value: {params[2:-1]}")

                return self._memory[params[2:-1]]

        return params

    def _run_step(self, metadata: dict, skip_errors: bool = False):
        uses = metadata.get("uses", None)
        if not uses:
            logger.error(f"Missing uses in {metadata}")
            if not skip_errors:
                raise ValueError(f"Missing uses in {metadata}")
            return

        logger.info(f"Running: {uses}")
        params = metadata.get("with", {})

        uses_parts = uses.split(".")

        if len(uses_parts) == 0:
            raise ValueError(f"Invalid uses: {uses}")
        elif len(uses_parts) > 1:
            filename, function_name = ".".join(uses_parts[:-1]), uses_parts[-1]

            try:
                module = importlib.import_module(filename)
            except ModuleNotFoundError as e:
                logger.error(f"Module not found: {filename} ({e})")
                if not skip_errors:
                    raise e

            try:
                module_function = getattr(module, function_name)
            except AttributeError as e:
                logger.error(f"Function not found: {function_name} ({e})")
                if not skip_errors:
                    raise e
        else:
            function_name = uses_parts[0]
            module_function = globals().get(
                function_name,
                locals().get(function_name, getattr(__builtins__, function_name, None)),
            )

            if not module_function:
                raise ValueError(f"Function not found: {uses}")

        try:
            params = self.update_params(params)
            logger.debug(f"Params: {params}")
            args = params.pop("args", [])

            response = module_function(*args, **params)
        except Exception as e:
            logger.error(f"Error running: {uses} ({e})")
            if not skip_errors:
                raise e

        name = metadata.get("name", None)

        if name:
            self._memory[name] = response

        return response

    def execute(self, skip_errors: bool = False):
        self._memory = {}
        self._memory.update(self.settings.get("environment", {}))
        steps = self.settings.get("steps", [])

        logger.info(f"=== Running steps ===")
        for step in steps:
            self._run_step(step, skip_errors)

        logger.info(f"=== Finished running steps ===")
