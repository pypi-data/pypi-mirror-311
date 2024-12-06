# Copyright 2020-2024 Datum Technology Corporation
# All rights reserved.
#######################################################################################################################
from pathlib import Path
from typing import Dict, List

from ..services.init import InitServiceModes, InitServiceReport, InitService, InitProjectConfiguration, \
    InitIpConfiguration
from ..core.service import ServiceType
from ..core.phase import Phase
from ..core.command import Command
from ..core.ip import Ip, IpPkgType, DutType


#######################################################################################################################
# Init Command
#######################################################################################################################
INIT_HELP_TEXT = """Moore.io Initialization Command
   Creates a new Project skeleton if not already within a Project.  If not, a new IP skeleton is created.
   This is the recommended method for importing code to the Moore.io ecosystem.
   
Usage:
   mio init [OPTIONS]

Options:
   -i, --input-file  # Specifies YAML input file path (instead of prompting user)
   
Examples:
   mio init                   # Create a new empty Project/IP in this location.
   mio init -i ~/answers.yml  # Create a new empty Project/IP in this location with pre-filled data.
   mio -C ~/my_proj init      # Create a new empty Project at a specific location."""


def get_commands():
    return [InitCommand]


class InitCommand(Command):
    def __init__(self):
        super().__init__()
        self._prompt_user: bool = False
        self._user_input_file: Path = Path()
        self._mode: InitServiceModes = InitServiceModes.UNDEFINED
        self._init_project_configuration: InitProjectConfiguration
        self._init_ip_configuration: InitIpConfiguration
        self._init_service: InitService
        self._report: InitServiceReport
        self._success: bool = False

    @staticmethod
    def name() -> str:
        return "init"

    @property
    def prompt_user(self) -> bool:
        return self._prompt_user
    
    @property
    def user_input_file(self) -> Path:
        return self._user_input_file
    
    @property
    def mode(self) -> InitServiceModes:
        return self._mode
    
    @property
    def init_project_configuration(self) -> InitProjectConfiguration:
        return self._init_project_configuration
    
    @property
    def init_ip_configuration(self) -> InitIpConfiguration:
        return self._init_ip_configuration
    
    @property
    def init_service(self) -> InitService:
        return self._init_service

    @property
    def report(self) -> InitServiceReport:
        return self._report

    @property
    def success(self) -> bool:
        return self._success

    @staticmethod
    def add_to_subparsers(subparsers):
        parser_init = subparsers.add_parser('init', help=INIT_HELP_TEXT, add_help=False)
        parser_init.add_argument('-i', "--input-file", help='Specifies YAML input file path (instead of prompting user)', type=str, required=False)

    def needs_authentication(self) -> bool:
        return False

    def phase_init(self, phase: Phase):
        if self.parsed_cli_arguments.input_file:
            self._user_input_file = Path(self.parsed_cli_arguments.input_file.strip())
            if not self.rmh.file_exists(self.user_input_file):
                phase.error = Exception(f"File '{self.user_input_file}' does not exist.")
            else:
                self._prompt_user = False

    def phase_pre_locate_project_file(self, phase: Phase):
        project_path: Path = self.rmh.locate_project_file()
        if project_path:
            self._mode = InitServiceModes.NEW_IP
        else:
            self._mode = InitServiceModes.NEW_PROJECT
            self._init_service: InitService = InitService(self.rmh)
            try:
                self.fill_project_configuration_from_user_input()
                self.init_project_configuration.input_path = self.rmh.wd
            except Exception as e:
                self._success = False
                phase.error = Exception(f"Failed to obtain valid Project data from user: {e}")
            else:
                try:
                    self._report = self.init_service.init_project(self.init_project_configuration)
                except Exception as e:
                    phase.error = Exception(f"Failed to initialize Project: {e}")
                    self._success = False
                else:
                    self._success = self.report.success

    def phase_pre_ip_discovery(self, phase: Phase):
        if self.mode == InitServiceModes.NEW_IP:
            try:
                self._init_service = self.rmh.service_database.find_service(ServiceType.CODE_GENERATION, "init")
            except Exception as e:
                phase.error = e
            else:
                try:
                    self.fill_ip_configuration_from_user_input()
                    self.init_ip_configuration.input_path = self.rmh.wd
                except Exception as e:
                    self._success = False
                    phase.error = Exception(f"Failed to obtain valid IP data from user: {e}")
                else:
                    try:
                        self._report = self.init_service.init_ip(self.init_ip_configuration)
                    except Exception as e:
                        phase.error = Exception(f"Failed to initialize IP: {e}")
                        self._success = False
                    else:
                        self._success = self.report.success
        else:
            self.print_report(phase)
            phase.end_process = True

    def phase_report(self, phase: Phase):
        self.print_report(phase)

    def print_report(self, phase: Phase):
        if self.success:
            banner = f"{'*' * 53}\033[32m SUCCESS \033[0m{'*' * 54}"
        else:
            banner = f"{'*' * 53}\033[31m\033[4m FAILURE \033[0m{'*' * 54}"
        print(banner)
        if self.mode == InitServiceModes.NEW_PROJECT:
            print(f"New Project '{self.report.name}' initialized at '{self.rmh.wd}'")
        else:
            print(f"New IP '{self.report.name}' initialized at '{self.rmh.wd}'")
        print(banner)
    
    def fill_project_configuration_from_user_input(self):
        if self.prompt_user:
            name: str = input("Enter the project name: ").strip()
            full_name: str = input("Enter the project full name: ").strip()
            ip_directories_raw: List[str] = input("Enter the name of directories where Project IP are located (separated by commas): ").split(",")
            ip_directories: List[str] = []
            for ip_directory in ip_directories_raw:
                ip_directories.append(ip_directory.strip())
            sim_directory: str = input("Enter the logic simulation directory: ").strip()
            docs_directory: str = input("Enter the documentation directory: ").strip()
            self._project_configuration: InitProjectConfiguration = InitProjectConfiguration(
                input_path=str(self.rmh.wd),
                name=name.strip().lower(),
                full_name=full_name.strip(),
                ip_directories=ip_directories,
                sim_directory=sim_directory,
                docs_directory=docs_directory
            )
        else:
            self._init_project_configuration = InitProjectConfiguration.load_from_yaml(self.user_input_file)
    
    def fill_ip_configuration_from_user_input(self):
        if self.prompt_user:
            ip_types_options = [member.name for member in IpPkgType]
            ip_types_str: str = ', '.join(ip_types_options).lower()
            ip_dut_types_options = [member.name for member in DutType]
            ip_dut_types_str: str = ', '.join(ip_dut_types_options).lower()
            vendor: str = input("Enter the IP vendor: ").strip().lower()
            name: str = input("Enter the IP name: ").strip().lower()
            full_name: str = input("Enter the full IP name: ").strip()
            version: str = input("Enter the IP version (e.g., 1.0.0): ").strip()
            ip_type: Ip.IpType = Ip.IpType[input(f"Enter the IP type [{ip_types_str}]: ").strip().upper()]
            has_docs_directory: bool = bool(input("Does the IP have a documentation directory? (True/False): "))
            docs_directory: str = ""
            if has_docs_directory:
                docs_directory = input("Enter the documentation directory (path): ").strip()
            has_scripts_directory: bool = bool(input("Does the IP have a scripts directory? (True/False): "))
            scripts_directory: str = ""
            if has_scripts_directory:
                scripts_directory = input("Enter the scripts directory (path): ").strip()
            has_examples_directory: bool = bool(input("Does the IP have examples directory? (True/False): "))
            examples_directory: str = ""
            if has_examples_directory:
                examples_directory = input("Enter the examples directory (path): ").strip()
            hdl_src_directory = input("Enter the HDL source directory path: ").strip()
            hdl_src_sub_directories: List[str] = []
            if hdl_src_directory != ".":
                hdl_src_sub_directories_raw: List[str] = input("Enter source sub-directories, separated by commas: ").split(",")
                for hdl_src_sub_directory in hdl_src_sub_directories_raw:
                    hdl_src_sub_directories.append(hdl_src_sub_directory.strip())
            hdl_top_sv_files_raw: List[str] = input("Enter the top SystemVerilog file(s), separated by commas: ").split(",")
            hdl_top_sv_files: List[str] = []
            for hdl_top_sv_file in hdl_top_sv_files_raw:
                hdl_top_sv_files.append(hdl_top_sv_file.strip())
            hdl_top_vhdl_files_raw: List[str] = input("Enter the top VHDL file(s), separated by commas: ").split(",")
            hdl_top_vhdl_files: List[str] = []
            for hdl_top_vhdl_file in hdl_top_vhdl_files_raw:
                hdl_top_vhdl_files.append(hdl_top_vhdl_file.strip())
            dut_type: DutType = DutType.MIO_IP
            dut_name: str = ""
            dut_version: str = ""
            hdl_top: List[str] = []
            hdl_tests_path: str = ""
            hdl_tests_name_template: str = ""
            if ip_type == IpPkgType.DV_TB:
                dut_type = DutType[input(f"Enter the DUT type [{ip_dut_types_str}]: ").strip().upper()]
                dut_name = input("Enter the DUT name: ").strip().lower()
                dut_version = input("Enter the DUT version (e.g., 1.0.0): ").strip()
                hdl_top_raw: List[str] = input("Enter the top design construct(s), separated by commas: ").split(",")
                for top in hdl_top_raw:
                    hdl_top.append(top.strip())
                hdl_tests_path = input("Enter the tests directory (path): ").strip()
                hdl_tests_name_template = input(f"Enter the template for test class names (e.g., '{name}_{{{{ name }}}}_test_c' ): ").strip()
            self._init_ip_configuration = InitIpConfiguration(
                input_path=str(self.rmh.wd),
                vendor=vendor,
                name=name,
                full_name=full_name,
                version=version,
                ip_type=ip_type,
                has_docs_directory=has_docs_directory,
                docs_directory=docs_directory,
                has_scripts_directory=has_scripts_directory,
                scripts_directory=scripts_directory,
                has_examples_directory=has_examples_directory,
                examples_directory=examples_directory,
                dut_type=dut_type,
                dut_name=dut_name,
                dut_version=dut_version,
                hdl_src_directory=hdl_src_directory,
                hdl_src_sub_directories=hdl_src_sub_directories,
                hdl_top_sv_files=hdl_top_sv_files,
                hdl_top_vhdl_files=hdl_top_vhdl_files,
                hdl_top=hdl_top,
                hdl_tests_path=hdl_tests_path,
                hdl_tests_name_template=hdl_tests_name_template
            )
        else:
            self._init_ip_configuration = InitIpConfiguration.load_from_yaml(self.user_input_file)