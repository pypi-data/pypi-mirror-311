# Copyright 2020-2024 Datum Technology Corporation
# All rights reserved.
#######################################################################################################################
import os
from abc import ABC
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional, Dict
import toml
import yaml

from semantic_version import Version

from ..core.scheduler import JobScheduler, Job, JobSchedulerConfiguration
from ..core.service import Service, ServiceType
from ..core.ip import Ip, DutType, IpPkgType
from ..core.model import Model, VALID_NAME_REGEX
from .regression import TestSuite


#######################################################################################################################
# API Entry Point
#######################################################################################################################
def get_services():
    return [InitService]


#######################################################################################################################
# Support Classes
#######################################################################################################################
class InitServiceModes(Enum):
    UNDEFINED = auto()
    NEW_PROJECT = auto()
    NEW_IP = auto()

class InitConfiguration(ABC, Model):
    input_path: Optional[str] = ""
    name: str
    full_name: str

class InitProjectConfiguration(InitConfiguration):
    ip_directories: List[str]
    sim_directory: str
    docs_directory: str
    @classmethod
    def load_from_yaml(cls, file_path: Path) -> 'InitProjectConfiguration':
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)
    def save_to_yaml(self, file_path: Path):
        with open(file_path, 'w') as f:
            yaml.safe_dump(self.model_dump(), f)

class InitIpConfiguration(InitConfiguration):
    vendor: str
    version: str
    ip_type: IpPkgType
    has_docs_directory: bool
    docs_directory: Optional[str] = ""
    has_scripts_directory: bool
    scripts_directory: Optional[str] = ""
    has_examples_directory: bool
    examples_directory: Optional[str] = ""
    dut_type: Optional[DutType] = DutType.MIO_IP
    dut_name: Optional[str] = ""
    dut_version: Optional[str] = ""
    hdl_src_directory: str
    hdl_src_sub_directories: Optional[List[str]] = []
    hdl_top_sv_files: Optional[List[str]] = []
    hdl_top_vhdl_files: Optional[List[str]] = []
    hdl_top: Optional[List[str]] = []
    hdl_tests_path: Optional[str] = ""
    hdl_tests_name_template: Optional[str] = ""
    @classmethod
    def load_from_yaml(cls, file_path: Path) -> 'InitIpConfiguration':
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)
    def save_to_yaml(self, file_path: Path):
        with open(file_path, 'w') as f:
            yaml.safe_dump(self.model_dump(), f)

class InitServiceReport(Model):
    name: Optional[str] = ""
    full_name: Optional[str] = ""
    mode: Optional[InitServiceModes] = InitServiceModes.UNDEFINED
    success: Optional[bool] = False
    output_path: Optional[Path] = Path()


#######################################################################################################################
# Service
#######################################################################################################################
class InitService(Service):
    def __init__(self, rmh: 'RootManager'):
        super().__init__(rmh, 'datum', 'init', 'Init')
        self._type = ServiceType.CODE_GENERATION

    def is_available(self) -> bool:
        return True

    def create_directory_structure(self):
        pass

    def create_files(self):
        pass

    def get_version(self) -> Version:
        return Version('1.0.0')

    def init_project(self, configuration: InitProjectConfiguration) -> InitServiceReport:
        report = InitServiceReport()
        report.mode = InitServiceModes.NEW_PROJECT
        mio_toml_path: Path = Path(os.path.join(configuration.input_path, 'mio.toml'))
        if mio_toml_path.exists():
            raise FileExistsError(f"'{mio_toml_path}' already exists.")
        else:
            report.output_path = configuration.input_path
            project_file = {
                'project' : {
                    'sync' : False,
                    'name' : configuration.name,
                    'full_name' : configuration.full_name,
                },
                'logic_simulation' : {
                    'root_path' : configuration.sim_directory,
                },
                'docs' : {
                    'root_path' : configuration.docs_directory,
                },
                'ip' : {
                    'local_paths' : configuration.ip_directories
                }
            }
            with open(mio_toml_path, 'w') as f:
                toml.dump(project_file, f)
        return report
    
    def init_ip(self, configuration: InitIpConfiguration) -> InitServiceReport:
        report = InitServiceReport()
        report.mode = InitServiceModes.NEW_IP
        ip_yml_path = Path(os.path.join(configuration.input_path, 'ip.yml'))
        ts_yml_path = Path(os.path.join(configuration.input_path, 'ts.yml'))
        if ip_yml_path.exists():
            raise FileExistsError(f"'{ip_yml_path}' already exists.")
        else:
            report.output_path = configuration.input_path
            ip_file = {
                'ip' : {
                    'sync' : False,
                    'pkg_type' : configuration.ip_type.value,
                    'vendor' : configuration.vendor,
                    'name' : configuration.name,
                    'full_name' : configuration.full_name,
                    'version' : configuration.version
                },
                'dependencies' : {},
                'structure' : {
                    'hdl_src_path' : configuration.hdl_src_directory,
                },
                'targets' : {
                    'default': {}
                },
            }
            if configuration.has_docs_directory:
                ip_file['structure']['docs_path'] = configuration.docs_directory
            if configuration.has_scripts_directory:
                ip_file['structure']['scripts_path'] = configuration.scripts_directory
            if configuration.has_examples_directory:
                ip_file['structure']['examples_path'] = configuration.examples_directory
            ip_file['hdl_src'] = {}
            ip_file['hdl_src']['directories'] = configuration.hdl_src_sub_directories
            ip_file['hdl_src']['top_sv_files'] = configuration.hdl_top_sv_files
            ip_file['hdl_src']['top_vhdl_files'] = configuration.hdl_top_vhdl_files
            if configuration.ip_type == IpPkgType.DV_TB:
                ip_file['dut'] = {}
                ip_file['dut']['type'] = configuration.dut_type.value
                ip_file['dut']['name'] = configuration.dut_name
                ip_file['dut']['version'] = configuration.dut_version
                ip_file['dut']['target'] = 'default'
                ip_file['hdl_src']['top'] = configuration.hdl_top
                ip_file['hdl_src']['tests_path'] = configuration.hdl_tests_path
                ip_file['hdl_src']['tests_name_template'] = configuration.hdl_tests_name_template
            try:
                new_ip: Ip = Ip(**ip_file)
            except Exception as e:
                report.success = False
                raise Exception(f"Failed to create IP object: {e}")
            else:
                new_ip.save_to_yaml(ip_yml_path)
                if configuration.ip_type == IpPkgType.DV_TB:
                    test_suite_file = {
                        'ts' : {
                            'name' : 'default',
                            'ip' : configuration.name,
                            'target' : ['*']
                        },
                        'tests' : {
                            'functional' : {}
                        }
                    }
                    try:
                        test_suite: TestSuite = TestSuite(**test_suite_file)
                    except Exception as e:
                        report.success = False
                        raise Exception(f"Failed to create Test Suite object: {e}")
                    else:
                        test_suite.save(ts_yml_path)
                        report.success = True
                else:
                    report.success = True
        return report
