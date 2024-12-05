import json
import numpy as np
import os
from asmu.io import Input, Output, Interface
from typing import List

class ASetup():
    def __init__(self, asetup_path: str) -> None:
        """The ASetup class handles .asm_settings JSON files. 
        Loading and saving, initializing the respective io classes and properties.

        Args:
            asetup_path (str): Path to .asm_setup file.
        """
        self._path, file = os.path.split(asetup_path)
        self._name = file.replace(".asm_setup", "") # extract name without file ending
        self.load_file(asetup_path)

    @property
    def name(self) -> str:
        """ASetup file name without ending."""
        return str(self._name)

    @property
    def path(self) -> str:
        """ASetup file path."""
        return str(self._path)

    @property
    def inputs(self) -> List[Input]:
        """List of all current Input instances."""
        return self._inputs

    @property
    def outputs(self) -> List[Output]:
        """List of all current Output instances."""
        return self._outputs

    @property
    def interface(self) -> Interface:
        """Current instance of Interface."""
        return self._interface
    
    def _initio(self):
        self._interface = Interface(self._setup["interface"])

        self._inputs = []
        for in_setup in self._setup["inputs"]:
            self._inputs.append(Input(in_setup))

        self._outputs = []
        for out_setup in self._setup["outputs"]:
            self._outputs.append(Output(out_setup))

    def _load_npy(self):
        """Load numpy arrays from external files into setup dicts."""
        for io in self.inputs+self.outputs:
            npys = {}
            for (k, v) in io.io_setup.items():
                try:
                    if isinstance(v, str) and v.endswith(".npy"):
                        npys[k] = np.load(v)
                except FileNotFoundError:
                    pass
            for (k, v) in npys.items(): io.io_setup[k] = v

    def _save_npy(self):
        """Save numpy arrays to external files and remove them from setup dicts."""
        for io in self.inputs+self.outputs:
            paths = {}
            for (k, v) in io.io_setup.items():
                try:
                    if isinstance(v, np.ndarray):
                        path = f"{self.path}/{self.name}/{io.name}_{k}.npy"
                        np.save(path, v)
                        paths[k] = path
                except KeyError:
                    pass
            for (k, v) in paths.items(): io.io_setup[k] = v

    def load_file(self, asetup_path: str) -> None:
        """Load .asm_setup file and calibration files from associated folder.

        Args:
            asetup_path (str): Path to .asm_setup file.
        """
        with open(asetup_path, "r") as file:
            self._setup = json.load(file)

        self._initio()
        self._load_npy()

    def save_file(self, asetup_path: str=None) -> None:
        """Overwrite .asm_setup file or create copy at given asetup_path.

        Args:
            asetup_path (str, optional): Path to .asm_setup file.
        """
        # update path
        if asetup_path is not None:
            self._path, file = os.path.split(asetup_path)
            self._name = file.replace(".asm_setup", "") # extract name without file ending
        asetup_path = f"{self.path}/{self.name}.asm_setup"

        self._save_npy()

        # save .asm_setup file
        with open(asetup_path, 'w') as file:
            file.write(json.dumps(self._setup, sort_keys=True, indent=4, separators=(',', ': ')))

        self._load_npy()

        

    

    