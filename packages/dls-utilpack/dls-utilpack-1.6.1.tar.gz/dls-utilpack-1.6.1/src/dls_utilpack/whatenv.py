import logging
import os
import platform
import sys
from io import StringIO
from typing import Optional

from ruamel.yaml import YAML

logger = logging.getLogger(__name__)


class Whatenv:
    def __init__(self, extra_dict: Optional[dict] = None):
        """
        Construct an object for gathering, componsing and logging
            environmental stuff.

        Args:
            extra_dict (Optional[dict], optional):  A dict of extra stuff
                also composed into the output. Defaults to None.
        """

        self.__extra_dict = extra_dict

    # ----------------------------------------------------------------------------------------
    def __compose_scalar(self, name: str, output: dict) -> None:
        value = os.environ.get(name)
        if value is None:
            output[name] = "not defined"
        else:
            output[name] = value

    # ----------------------------------------------------------------------------------------
    def __compose_paths(self, name: str, output: dict) -> None:
        paths = os.environ.get(name)
        if paths is None:
            output[name] = "not defined"
        else:
            output[name] = []
            for path in paths.split(":"):
                path = path.strip()
                if path == "":
                    continue
                output[name].append(path)

    # ----------------------------------------------------------------------------------------
    def compose_as_yaml(self) -> str:
        """
        Compose a yaml-like string describing the current enviornment.

        Typically put into a logging.debug statement.

        Returns:
            str: yaml-like string with newline characters separating lines
        """

        output_dict: dict = {}

        # Add keys from the provided extra_dict if given.
        if self.__extra_dict is not None:
            output_dict.update(self.__extra_dict)

        self.__compose_scalar("HOSTNAME", output_dict)
        self.__compose_scalar("USER", output_dict)
        output_dict["os.getcwd"] = os.getcwd()

        self.__compose_scalar("VIRTUAL_ENV", output_dict)

        sge_dict: dict = {}
        self.__compose_scalar("SGE_CELL", sge_dict)
        self.__compose_scalar("SGE_EXECD_PORT", sge_dict)
        self.__compose_scalar("SGE_QMASTER_PORT", sge_dict)
        self.__compose_scalar("SGE_HGR_gpu", sge_dict)
        self.__compose_scalar("SGE_HGR_m_mem_free", sge_dict)
        self.__compose_scalar("SGE_HGR_TASK_gpu", sge_dict)
        self.__compose_scalar("SGE_HGR_TASK_m_mem_free", sge_dict)
        self.__compose_scalar("PE", sge_dict)
        self.__compose_scalar("QUEUE", sge_dict)
        self.__compose_scalar("JOB_ID", sge_dict)
        self.__compose_scalar("JOB_NAME", sge_dict)
        output_dict["sge"] = sge_dict

        slurm_dict: dict = {}
        for k in os.environ.keys():
            if k.startswith("SLURM"):
                self.__compose_scalar(k, slurm_dict)
        output_dict["slurm"] = slurm_dict

        conda_dict: dict = {}
        self.__compose_scalar("CONDA_PREFIX", conda_dict)
        conda_shlvl = int(os.environ.get("CONDA_SHLVL", 0))
        for i in range(conda_shlvl - 1, 0, -1):
            self.__compose_scalar(f"CONDA_PREFIX_{i}", conda_dict)
        output_dict["conda"] = conda_dict

        modules_dict: dict = {}
        self.__compose_paths("MODULEPATH", modules_dict)
        self.__compose_paths("MODULESHOME", modules_dict)
        self.__compose_paths("LOADEDMODULES", modules_dict)
        self.__compose_paths("PATH", modules_dict)
        output_dict["modules"] = modules_dict

        uname = platform.uname()
        platform_dict = {}
        platform_dict["system"] = uname.system
        platform_dict["node"] = uname.node
        platform_dict["python_version"] = platform.python_version()
        platform_dict["release"] = uname.release
        platform_dict["version"] = uname.version
        platform_dict["machine"] = uname.machine
        platform_dict["processor"] = uname.processor
        output_dict["platform"] = platform_dict

        self.__compose_paths("PYTHONPATH", output_dict)
        output_dict["sys.path"] = sys.path
        output_dict["sys.executable"] = sys.executable

        # Print the result.
        string_stream = StringIO()

        output_yaml = YAML()
        output_yaml.default_flow_style = False
        output_yaml.indent(mapping=2, sequence=4, offset=2)
        output_yaml.preserve_quotes = True  # type: ignore
        output_yaml.dump(output_dict, string_stream)

        yaml_string = string_stream.getvalue()

        return yaml_string

    # ----------------------------------------------------------------------------------------
    def log(
        self,
        level=logging.INFO,
    ) -> None:
        """
        Log a string describing the current enviornment.

        Args:
            level (_type_, optional): A python logging level. Defaults to logging.INFO.
        """

        yaml_string = self.compose_as_yaml()

        logger.log(level, f"\n{yaml_string}")
