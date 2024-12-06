# Copyright 2020-2024 Datum Technology Corporation
# All rights reserved.
#######################################################################################################################
import re
from typing import List, Dict

from ..core.configuration import LogicSimulators
from ..services.regression import RegressionDatabase, RegressionReport, RegressionConfiguration, RegressionRunner, Regression
from ..core.ip import Ip, IpDefinition, IpPkgType
from ..core.command import Command
from ..core.phase import Phase
from ..core.scheduler import JobScheduler
from ..core.service import ServiceType
from ..services.simulation import LogicSimulator, LogicSimulatorCompilationConfiguration, \
    LogicSimulatorElaborationConfiguration, \
    LogicSimulatorCompilationAndElaborationConfiguration, LogicSimulatorSimulationConfiguration, UvmVerbosity, \
    LogicSimulatorCoverageMergeConfiguration, LogicSimulatorCoverageMergeReport
from ..services.simulation import LogicSimulatorCompilationReport, LogicSimulatorElaborationReport, LogicSimulatorCompilationAndElaborationReport, LogicSimulatorSimulationReport



#######################################################################################################################
# API Entry Point
#######################################################################################################################
def get_commands():
    return [SimulateCommand, RegressionCommand]


#######################################################################################################################
# Sim Command
#######################################################################################################################
SIM_HELP_TEXT = """Moore.io Logic Simulation Command
   Performs necessary steps to run simulation of an IP.  Only supports Digital Logic Simulation for the time being.
   
   An optional target may be specified for the IP. Ex: my_ip#target.
   
   While the controls for individual steps (DUT setup, compilation, elaboration and simulation) are exposed, it is
   recommended to let `mio sim` manage this process as much as possible.  In the event of corrupt simulator artifacts,
   see `mio clean`.  Combining any of the step-control arguments (-D, -C, -E, -S) with missing steps is illegal
   (ex: `-DS`).
   
   Two types of arguments (--args) can be passed: compilation (+define+NAME[=VALUE]) and simulation (+NAME[=VALUE]).
   
   For running multiple tests in parallel, see `mio regr`.
   
Usage:
   mio sim IP[#TARGET] [OPTIONS] [--args ARG ...]
   
Options:
   -t TEST     , --test      TEST       Specify the UVM test to be run.
   -s SEED     , --seed      SEED       Positive Integer. Specify randomization seed  If none is provided, a random one will be picked.
   -v VERBOSITY, --verbosity VERBOSITY  Specifies UVM logging verbosity: none, low, medium, high, debug. [default: medium]
   -+ ARGS     , --args      ARGS       Specifies compilation-time (+define+ARG[=VAL]) or simulation-time (+ARG[=VAL]) arguments
   -e ERRORS   , --errors    ERRORS     Specifies the number of errors at which compilation/elaboration/simulation is terminated.  [default: 10]
   -a APP      , --app       APP        Specifies simulator application to use: viv, mdc, vcs, xcl, qst, riv. [default: viv]
   -w          , --waves                Enable wave capture to disk.
   -c          , --cov                  Enable code & functional coverage capture.
   -g          , --gui                  Invokes simulator in graphical or 'GUI' mode.
   
   -S   Simulate
   -E   Elaborate
   -C   Compile
   -D   Prepare Device-Under-Test (DUT) for logic simulation. Ex: invoke FuseSoC to prepare core(s) for compilation.
   
Examples:
   mio sim my_ip -t smoke -s 1 -w -c             # Compile, elaborate and simulate test 'my_ip_smoke_test_c'
                                                 # for IP 'my_ip' with seed '1' and waves & coverage capture enabled.
   mio sim my_ip -t smoke -s 1 --args +NPKTS=10  # Compile, elaborate and simulate test 'my_ip_smoke_test_c'
                                                 # for IP 'my_ip' with seed '1' and a simulation argument.
   mio sim my_ip -S -t smoke -s 42 -v high -g    # Only simulates test 'my_ip_smoke_test_c' for IP 'my_ip'
                                                 # with seed '42' and UVM_HIGH verbosity using the simulator in GUI mode.
   mio sim my_ip#dw64b -C                        # Only compile 'my_ip' target 'dw64b'.
   mio sim my_ip -E                              # Only elaborate 'my_ip'.
   mio sim my_ip -CE                             # Compile and elaborate 'my_ip'."""
VERBOSITY_LEVELS = ["none", "low", "medium", "high", "full", "debug"]
LOGIC_SIMULATORS = ["dsim", "vivado"]

class SimulateCommand(Command):
    @staticmethod
    def name() -> str:
        return "sim"

    @staticmethod
    def add_to_subparsers(subparsers):
        parser_sim = subparsers.add_parser('sim', help=SIM_HELP_TEXT, add_help=False)
        parser_sim.add_argument('ip', help='Target IP')
        parser_sim.add_argument('-t', "--test", help='Delete compiled IP dependencies.', required=False)
        parser_sim.add_argument('-s', "--seed",
                                help='Specify the seed for constrained-random testing.  If none is provided, a random one will be picked.',
                                type=int, required=False)
        parser_sim.add_argument('-v', "--verbosity",
                                help='Specify the UVM verbosity level for logging: none, low, medium, high or debug.  Default: medium',
                                choices=VERBOSITY_LEVELS, required=False)
        parser_sim.add_argument('-e', "--errors",
                                help='Specifies the number of errors at which compilation/elaboration/simulation is terminated.',
                                type=int, required=False)
        parser_sim.add_argument('-a', "--app",
                                help='Specifies which simulator to use: dsim only one supported for now.',
                                choices=LOGIC_SIMULATORS)
        parser_sim.add_argument('-w', "--waves", help='Enable wave capture to disk.', action="store_true",
                                required=False)
        parser_sim.add_argument('-c', "--cov", help='Enable code & functional coverage capture.', action="store_true",
                                required=False)
        parser_sim.add_argument('-g', "--gui", help="Invoke the simulator's Graphical User Interface.",
                                action="store_true", required=False)
        parser_sim.add_argument('-S', help='Force mio to simulate target IP.  Can be combined with -D, -C and/or -E.',
                                action="store_true", required=False)
        parser_sim.add_argument('-E', help='Force mio to elaborate target IP.  Can be combined with -D, -C and/or -S.',
                                action="store_true", required=False)
        parser_sim.add_argument('-C', help='Force mio to compile target IP.  Can be combined with -D, -E and/or -S.',
                                action="store_true", required=False)
        parser_sim.add_argument('-D',
                                help='Force mio to prepare Device-Under-Test (DUT).  Can be combined with -C, -E and/or -S.',
                                action="store_true", required=False)
        parser_sim.add_argument('-+', "--args",
                                help='Add arguments for compilation (+define+NAME[=VALUE]) or simulation (+NAME[=VALUE])).',
                                nargs='+', dest='add_args', required=False)

    def __init__(self):
        super().__init__()
        self._ip_definition: IpDefinition = None
        self._ip: Ip = None
        self._app: LogicSimulators = LogicSimulators.UNDEFINED
        self._simulator: LogicSimulator = None
        self._scheduler: JobScheduler = None
        self._do_prepare_dut: bool = False
        self._do_compile: bool = False
        self._do_elaborate: bool = False
        self._do_compile_and_elaborate: bool = False
        self._do_simulate: bool = False
        self._compilation_configuration: LogicSimulatorCompilationConfiguration
        self._elaboration_configuration: LogicSimulatorElaborationConfiguration
        self._compilation_and_elaboration_configuration: LogicSimulatorCompilationAndElaborationConfiguration
        self._simulation_configuration: LogicSimulatorSimulationConfiguration
        self._coverage_merge_configuration: LogicSimulatorCoverageMergeConfiguration
        self._compilation_report: LogicSimulatorCompilationReport
        self._elaboration_report: LogicSimulatorElaborationReport
        self._compilation_and_elaboration_report: LogicSimulatorCompilationAndElaborationReport
        self._simulation_report: LogicSimulatorSimulationReport
        self._coverage_merge_report: LogicSimulatorCoverageMergeReport
        self._success: bool = False
        self._defines_boolean: List[str] = []
        self._defines_value: Dict[str, str] = {}
        self._args_boolean: List[str] = []
        self._args_value: Dict[str, str] = {}

    @property
    def simulator(self) -> LogicSimulator:
        return self._simulator

    @property
    def scheduler(self) -> JobScheduler:
        return self._scheduler

    @property
    def do_prepare_dut(self) -> bool:
        return self._do_prepare_dut

    @property
    def do_compile(self) -> bool:
        return self._do_compile

    @property
    def do_elaborate(self) -> bool:
        return self._do_elaborate

    @property
    def do_compile_and_elaborate(self) -> bool:
        return self._do_compile_and_elaborate

    @property
    def do_simulate(self) -> bool:
        return self._do_simulate

    @property
    def compilation_configuration(self) -> LogicSimulatorCompilationConfiguration:
        return self._compilation_configuration

    @property
    def elaboration_configuration(self) -> LogicSimulatorElaborationConfiguration:
        return self._elaboration_configuration

    @property
    def compilation_and_elaboration_configuration(self) -> LogicSimulatorCompilationAndElaborationConfiguration:
        return self._compilation_and_elaboration_configuration

    @property
    def simulation_configuration(self) -> LogicSimulatorSimulationConfiguration:
        return self._simulation_configuration

    @property
    def coverage_merge_configuration(self) -> LogicSimulatorCoverageMergeConfiguration:
        return self._coverage_merge_configuration

    @property
    def compilation_report(self) -> LogicSimulatorCompilationReport:
        return self._compilation_report

    @property
    def elaboration_report(self) -> LogicSimulatorElaborationReport:
        return self._elaboration_report

    @property
    def compilation_and_elaboration_report(self) -> LogicSimulatorCompilationAndElaborationReport:
        return self._compilation_and_elaboration_report

    @property
    def simulation_report(self) -> LogicSimulatorSimulationReport:
        return self._simulation_report

    @property
    def coverage_merge_report(self) -> LogicSimulatorCoverageMergeReport:
        return self._coverage_merge_report

    @property
    def success(self) -> bool:
        return self._success

    @property
    def defines_boolean(self) -> list[str]:
        return self._defines_boolean

    @property
    def defines_value(self) -> dict[str, str]:
        return self._defines_value

    @property
    def args_boolean(self) -> list[str]:
        return self._args_boolean

    @property
    def args_value(self) -> dict[str, str]:
        return self._args_value

    @property
    def ip_definition(self) -> IpDefinition:
        return self._ip_definition

    @property
    def ip(self) -> Ip:
        return self._ip

    @property
    def app(self) -> LogicSimulators:
        return self._app

    def needs_authentication(self) -> bool:
        return False

    def phase_init(self, phase: Phase):
        ip_def_str = ""
        ip_target = "default"
        if "#" in self.parsed_cli_arguments.ip:
            spit_ip_def = self.parsed_cli_arguments.ip.split("#")
            if len(spit_ip_def) != 2:
                phase.error = Exception(f"Invalid IP/target specification: '{self.parsed_cli_arguments.ip}'")
                return
            else:
                ip_def_str = spit_ip_def[0].strip().lower()
                ip_target = spit_ip_def[1].strip().lower()
        else:
            ip_def_str = self.parsed_cli_arguments.ip.strip().lower()
        self._ip_definition = Ip.parse_ip_definition(ip_def_str)
        self.ip_definition.target = ip_target
        if not self.parsed_cli_arguments.D and not self.parsed_cli_arguments.C and not self.parsed_cli_arguments.E and not self.parsed_cli_arguments.S:
            self._do_prepare_dut = True
            self._do_compile = True
            self._do_elaborate = True
            self._do_simulate = True
        else:
            self._do_prepare_dut = self.parsed_cli_arguments.D
            self._do_compile = self.parsed_cli_arguments.C
            self._do_elaborate = self.parsed_cli_arguments.E
            self._do_simulate = self.parsed_cli_arguments.S

        if self.parsed_cli_arguments.add_args:
            patterns = {
                re.compile(r'^\+define\+(\w+)$'): self.defines_boolean,
                re.compile(r'^\+define\+(\w+)=(\w+)$'): self.defines_value,
                re.compile(r'^\+(\w+)$'): self.args_boolean,
                re.compile(r'^\+(\w+)=(\w+)$'): self.args_value
            }
            for arg in self.parsed_cli_arguments.add_args:
                match_found = False
                for pattern, target_list in patterns.items():
                    match = pattern.match(arg)
                    if match:
                        if isinstance(target_list, list):
                            target_list.append(match.group(1))
                        else:
                            target_list[match.group(1)] = match.group(2)
                        match_found = True
                        break
                if not match_found:
                    raise Exception(f"Argument '{arg}' does not match any of the expected patterns.")
        self._app = LogicSimulators[self.parsed_cli_arguments.app.upper()]

    def phase_post_validate_configuration_space(self, phase: Phase):
        if self.app == LogicSimulators.UNDEFINED:
            if not self.rmh.configuration.logic_simulation.default_simulator:
                phase.error = Exception(
                    f"No simulator specified (-a/--app) and no default simulator in the Configuration")
                return
            else:
                self._app = self.rmh.configuration.logic_simulation.default_simulator.value

    def phase_post_scheduler_discovery(self, phase: Phase):
        try:
            # TODO Add support for other schedulers
            self._scheduler = self.rmh.scheduler_database.get_default_scheduler()
        except Exception as e:
            phase.error = e

    def phase_post_service_discovery(self, phase: Phase):
        try:
            self._simulator = self.rmh.service_database.find_service(ServiceType.LOGIC_SIMULATION, self.app.value)
        except Exception as e:
            phase.error = e
        else:
            if not self.simulator.supports_uvm:
                phase.error = Exception(f"Simulator '{self.simulator}' does not support UVM")

    def phase_post_ip_discovery(self, phase: Phase):
        self._ip = self.rmh.ip_database.find_ip_definition(self.ip_definition, raise_exception_if_not_found=False)
        if not self.ip:
            phase.error = Exception(f"IP '{self.ip_definition}' could not be found")
        else:
            if self.do_simulate and (self.ip.ip.pkg_type != IpPkgType.DV_TB):
                phase.error = Exception(f"IP '{self.ip}' is not a Test Bench")
                return
            if self.ip.has_vhdl_content:
                # VHDL must be compiled and elaborated separately
                if self.do_compile_and_elaborate:
                    self._do_compile = True
                    self._do_elaborate = True
                    self._do_compile_and_elaborate = False
            else:
                if self.do_compile and self.do_elaborate:
                    if self.simulator.supports_two_step_simulation:
                        self._do_compile = False
                        self._do_elaborate = False
                        self._do_compile_and_elaborate = True
                    else:
                        self._do_compile = True
                        self._do_elaborate = True
                        self._do_compile_and_elaborate = False

    def phase_main(self, phase: Phase):
        if self.do_prepare_dut:
            self.prepare_dut(phase)
        if self.do_compile:
            self.compile(phase)
            if not self.compilation_report.success:
                self._do_elaborate = False
                self._do_simulate = False
        if self.do_elaborate:
            self.elaborate(phase)
            if not self.elaboration_report.success:
                self._do_simulate = False
        if self.do_compile_and_elaborate:
            self.compile_and_elaborate(phase)
            if not self.compilation_and_elaboration_report.success:
                self._do_simulate = False
        if self.do_simulate:
            self.simulate(phase)

    def prepare_dut(self, phase: Phase):
        pass

    def compile(self, phase: Phase):
        self._compilation_configuration = LogicSimulatorCompilationConfiguration()
        if self.parsed_cli_arguments.errors:
            self.compilation_configuration.max_errors = self.parsed_cli_arguments.errors
        if self.parsed_cli_arguments.waves:
            self.compilation_configuration.enable_waveform_capture = True
        if self.parsed_cli_arguments.cov:
            self.compilation_configuration.enable_coverage = True
        self.compilation_configuration.defines_boolean = self.defines_boolean
        self.compilation_configuration.defines_value = self.defines_value
        self.compilation_configuration.target = self.ip_definition.target
        self._compilation_report = self.simulator.compile(self.ip, self.compilation_configuration, self.scheduler)

    def elaborate(self, phase: Phase):
        self._elaboration_configuration = LogicSimulatorElaborationConfiguration()
        self._elaboration_report = self.simulator.elaborate(self.ip, self.elaboration_configuration, self.scheduler)

    def compile_and_elaborate(self, phase: Phase):
        self._compilation_and_elaboration_configuration = LogicSimulatorCompilationAndElaborationConfiguration()
        if self.parsed_cli_arguments.errors:
            self._compilation_and_elaboration_configuration.max_errors = self.parsed_cli_arguments.errors
        if self.parsed_cli_arguments.waves:
            self._compilation_and_elaboration_configuration.enable_waveform_capture = True
        if self.parsed_cli_arguments.cov:
            self._compilation_and_elaboration_configuration.enable_coverage = True
        self.compilation_and_elaboration_configuration.defines_boolean = self.defines_boolean
        self.compilation_and_elaboration_configuration.defines_value = self.defines_value
        self.compilation_and_elaboration_configuration.target = self.ip_definition.target
        self._compilation_and_elaboration_report = self.simulator.compile_and_elaborate(self.ip,
                                                                                        self.compilation_and_elaboration_configuration,
                                                                                        self.scheduler)

    def simulate(self, phase: Phase):
        self._simulation_configuration = LogicSimulatorSimulationConfiguration()
        self.simulation_configuration.seed = self.parsed_cli_arguments.seed if self.parsed_cli_arguments.seed is not None else 1
        self.simulation_configuration.verbosity = self.parsed_cli_arguments.verbosity if self.parsed_cli_arguments.verbosity is not None else UvmVerbosity.MEDIUM
        self.simulation_configuration.max_errors = self.parsed_cli_arguments.errors if self.parsed_cli_arguments.errors is not None else 10
        self.simulation_configuration.gui_mode = self.parsed_cli_arguments.gui
        self.simulation_configuration.enable_waveform_capture = self.parsed_cli_arguments.waves
        self.simulation_configuration.enable_coverage = self.parsed_cli_arguments.cov
        self.simulation_configuration.test_name = self.parsed_cli_arguments.test.strip().lower()
        self.simulation_configuration.args_boolean = self.args_boolean
        self.simulation_configuration.args_value = self.args_value
        self.simulation_configuration.target = self.ip_definition.target
        self._simulation_report = self.simulator.simulate(self.ip, self.simulation_configuration, self.scheduler)
        if self.simulation_configuration.enable_coverage:
            self._coverage_merge_configuration = LogicSimulatorCoverageMergeConfiguration()
            self.coverage_merge_configuration.target_name = self.ip_definition.target
            self.coverage_merge_configuration.output_path = self.simulation_report.coverage_directory
            self.coverage_merge_configuration.create_html_report = True
            self.coverage_merge_configuration.html_report_path = self.simulation_report.coverage_directory
            self.coverage_merge_configuration.merge_log_file_path = self.simulation_report.coverage_directory / f"coverage_merge.{self.simulator.name}.log"
            self.coverage_merge_configuration.input_simulation_reports.append(self.simulation_report)
            self._coverage_merge_report = self.simulator.coverage_merge(self.ip, self.coverage_merge_configuration,
                                                                        self.scheduler)

    def phase_report(self, phase: Phase):
        self._success = True
        if self.do_compile:
            self._success &= self.compilation_report.success
        if self.do_elaborate:
            self._success &= self.elaboration_report.success
        if self.do_compile_and_elaborate:
            self._success &= self.compilation_and_elaboration_report.success
        if self.do_simulate:
            self._success &= self.simulation_report.success
        if self.success:
            banner = f"{'*' * 53}\033[32m SUCCESS \033[0m{'*' * 54}"
        else:
            banner = f"{'*' * 53}\033[31m\033[4m FAILURE \033[0m{'*' * 54}"
        print(banner)
        if self.do_prepare_dut:
            self.print_prepare_dut_report(phase)
        if self.do_compile:
            self.print_compilation_report(phase)
        if self.do_elaborate:
            self.print_elaboration_report(phase)
        if self.do_compile_and_elaborate:
            self.print_compilation_and_elaboration_report(phase)
        if self.do_simulate:
            self.print_simulation_report(phase)
        print(banner)

    def phase_final(self, phase: Phase):
        if not self.success:
            phase.error = Exception(f"Logic Simulation failed.")

    def print_prepare_dut_report(self, phase: Phase):
        pass

    def print_compilation_report(self, phase: Phase):
        errors_str = f"\033[31m\033[1m{self.compilation_report.num_errors}E\033[0m" if self.compilation_report.num_errors > 0 else "0E"
        warnings_str = f"\033[33m\033[1m{self.compilation_report.num_errors}W\033[0m" if self.compilation_report.num_errors > 0 else "0W"
        fatal_str = f" \033[33m\033[1mF\033[0m" if self.compilation_report.num_fatals > 0 else ""
        if self.compilation_report.has_sv_files_to_compile and self.compilation_report.has_vhdl_files_to_compile:
            print(f" Compilation results - {errors_str} {warnings_str}{fatal_str}:")
            print(f"  * {self.rmh.configuration.applications.editor} {self.compilation_report.sv_log_path}")
            print(f"  * {self.rmh.configuration.applications.editor} {self.compilation_report.vhdl_log_path}")
        else:
            if self.compilation_report.has_sv_files_to_compile:
                print(f" Compilation results - {errors_str} {warnings_str}{fatal_str}:")
                print(f"  * {self.rmh.configuration.applications.editor} {self.compilation_report.sv_log_path}")
            elif self.compilation_report.has_vhdl_files_to_compile:
                print(f" Compilation results - {errors_str} {warnings_str}{fatal_str}:")
                print(f"  * {self.rmh.configuration.applications.editor} {self.compilation_report.vhdl_log_path}")
        if not self.compilation_report.success:
            print('*' * 119)
            for error in self.compilation_report.errors:
                print(f"\033[31m{error}\033[0m")
            for fatal in self.compilation_report.fatals:
                print(f"\033[31m{fatal}\033[0m")

    def print_elaboration_report(self, phase: Phase):
        errors_str = f"\033[31m\033[1m{self.elaboration_report.num_errors}E\033[0m" if self.elaboration_report.num_errors > 0 else "0E"
        warnings_str = f"\033[33m\033[1m{self.elaboration_report.num_warnings}W\033[0m" if self.elaboration_report.num_warnings > 0 else "0W"
        fatal_str = f" \033[33m\033[1mF\033[0m" if self.elaboration_report.num_fatals > 0 else ""
        print(f" Elaboration results - {errors_str} {warnings_str}{fatal_str}:")
        print(f"  * Log: {self.rmh.configuration.applications.editor} {self.elaboration_report.log_path}")
        if not self.elaboration_report.success:
            print('*' * 119)
            for error in self.elaboration_report.errors:
                print(f"\033[31m{error}\033[0m")
            for fatal in self.elaboration_report.fatals:
                print(f"\033[31m{fatal}\033[0m")

    def print_compilation_and_elaboration_report(self, phase: Phase):
        errors_str = f"\033[31m\033[1m{self.compilation_and_elaboration_report.num_errors}E\033[0m" if self.compilation_and_elaboration_report.num_errors > 0 else "0E"
        warnings_str = f"\033[33m\033[1m{self.compilation_and_elaboration_report.num_warnings}W\033[0m" if self.compilation_and_elaboration_report.num_warnings > 0 else "0W"
        fatal_str = f" \033[33m\033[1mF\033[0m" if self.compilation_and_elaboration_report.num_fatals > 0 else ""
        print(f" Compilation+Elaboration results - {errors_str} {warnings_str}{fatal_str}:")
        print(
            f"  * Log: {self.rmh.configuration.applications.editor} {self.compilation_and_elaboration_report.log_path}")
        if not self.compilation_and_elaboration_report.success:
            print('*' * 119)
            for error in self.compilation_and_elaboration_report.errors:
                print(f"\033[31m{error}\033[0m")
            for fatal in self.compilation_and_elaboration_report.fatals:
                print(f"\033[31m{fatal}\033[0m")

    def print_simulation_report(self, phase: Phase):
        errors_str = f"\033[31m\033[1m{self.simulation_report.num_errors}E\033[0m" if self.simulation_report.num_errors > 0 else "0E"
        warnings_str = f"\033[33m\033[1m{self.simulation_report.num_warnings}W\033[0m" if self.simulation_report.num_warnings > 0 else "0W"
        fatal_str = f" \033[33m\033[1mF\033[0m" if self.simulation_report.num_fatals > 0 else ""
        print(f" Simulation results - {errors_str} {warnings_str}{fatal_str}:")
        print(f"  * Log: {self.rmh.configuration.applications.editor} {self.simulation_report.log_path}")
        if self.simulation_configuration.enable_waveform_capture:
            view_waves_command: str = self.simulator.get_view_waves_command(self.simulation_configuration,
                                                                            self.simulation_report)
            print(f"  * Waves: {view_waves_command} &")
        if self.simulation_configuration.enable_coverage:
            print(
                f"  * Coverage: {self.rmh.configuration.applications.web_browser} {self.coverage_merge_report.html_report_index_path} &")
        if not self.simulation_report.success:
            print('*' * 119)
            for error in self.simulation_report.errors:
                print(f"\033[31m{error}\033[0m")
            for fatal in self.simulation_report.fatals:
                print(f"\033[31m{fatal}\033[0m")



#######################################################################################################################
# Regression Command
#######################################################################################################################
REGR_HELP_TEXT = """Moore.io Regression Command
   Runs a set of tests against a specific IP.  Regressions are described in Test Suite files (`[<target>.]ts.yml`).
   
   An optional target may be specified for the IP. Ex: my_ip#target.
   
Usage:
   mio regr IP[#TARGET] [TEST SUITE.]REGRESSION [OPTIONS]
   
Options:
   -d, --dry-run  Compiles, elaborates, but only prints the tests mio would normally run (does not actually run them).
   
Examples:
   mio regr my_ip sanity            # Run sanity regression for IP 'uvm_my_ip', from test suite 'ts.yml'
   mio regr my_ip apb_xc.sanity     # Run sanity regression for IP 'uvm_my_ip', from test suite 'apb_xc.ts.yml'
   mio regr my_ip axi_xc.sanity -d  # Dry-run sanity regression for IP 'uvm_my_ip', from test suite 'axi_xc.ts.yml"""

class RegressionCommand(Command):
    @staticmethod
    def name() -> str:
        return "regr"

    @staticmethod
    def add_to_subparsers(subparsers):
        parser_regr = subparsers.add_parser('regr', help=REGR_HELP_TEXT, add_help=False)
        parser_regr.add_argument('ip'         , help='Target IP')
        parser_regr.add_argument('regr'       , help='Regression to be run.  For Test Bench IPs with multiple Test Suites, the suite must be specified. Ex: `mio regr my_ip apbxc.sanity`')
        parser_regr.add_argument('-a', "--app", help='Specifies which simulator to use: dsim', choices=LOGIC_SIMULATORS , required=False)
        parser_regr.add_argument('-d', "--dry", help='Compiles and elaborates target IP but only prints out the tests that would be run.', action="store_true", default=False , required=False)

    def __init__(self):
        super().__init__()
        self._ip_definition: IpDefinition = None
        self._ip: Ip = None
        self._test_suite_name: str = ""
        self._test_suite_name_is_specified: bool=False
        self._regression: Regression = None
        self._regression_name: str = ""
        self._dry_mode: bool = False
        self._app: LogicSimulators = LogicSimulators.UNDEFINED
        self._regression_database: RegressionDatabase = None
        self._simulator: LogicSimulator = None
        self._regression_runner: RegressionRunner = None
        self._scheduler: JobScheduler = None
        self._do_compile: bool = False
        self._do_elaborate: bool = False
        self._do_compile_and_elaborate: bool = False
        self._compilation_configuration: LogicSimulatorCompilationConfiguration
        self._elaboration_configuration: LogicSimulatorElaborationConfiguration
        self._compilation_and_elaboration_configuration: LogicSimulatorCompilationAndElaborationConfiguration
        self._regression_configuration: RegressionConfiguration
        self._compilation_report: LogicSimulatorCompilationReport
        self._elaboration_report: LogicSimulatorElaborationReport
        self._compilation_and_elaboration_report: LogicSimulatorCompilationAndElaborationReport
        self._regression_report: RegressionReport
        self._success: bool = False

    @property
    def ip_definition(self) -> IpDefinition:
        return self._ip_definition

    @property
    def ip(self) -> Ip:
        return self._ip

    @property
    def app(self) -> LogicSimulators:
        return self._app

    @property
    def test_suite_name(self) -> str:
        return self._test_suite_name

    @property
    def test_suite_name_is_specified(self) -> bool:
        return self._test_suite_name_is_specified

    @property
    def regression(self) -> Regression:
        return self._regression

    @property
    def regression_name(self) -> str:
        return self._regression_name

    @property
    def dry_mode(self) -> bool:
        return self._dry_mode

    @property
    def regression_database(self) -> RegressionDatabase:
        return self._regression_database

    @property
    def simulator(self) -> LogicSimulator:
        return self._simulator

    @property
    def regression_runner(self) -> RegressionRunner:
        return self._regression_runner

    @property
    def scheduler(self) -> JobScheduler:
        return self._scheduler

    @property
    def do_compile(self) -> bool:
        return self._do_compile
    @property
    def do_elaborate(self) -> bool:
        return self._do_elaborate
    @property
    def do_compile_and_elaborate(self) -> bool:
        return self._do_compile_and_elaborate

    @property
    def compilation_configuration(self) -> LogicSimulatorCompilationConfiguration:
        return self._compilation_configuration

    @property
    def elaboration_configuration(self) -> LogicSimulatorElaborationConfiguration:
        return self._elaboration_configuration

    @property
    def compilation_and_elaboration_configuration(self) -> LogicSimulatorCompilationAndElaborationConfiguration:
        return self._compilation_and_elaboration_configuration

    @property
    def regression_configuration(self) -> RegressionConfiguration:
        return self._regression_configuration

    @property
    def compilation_report(self) -> LogicSimulatorCompilationReport:
        return self._compilation_report

    @property
    def elaboration_report(self) -> LogicSimulatorElaborationReport:
        return self._elaboration_report

    @property
    def compilation_and_elaboration_report(self) -> LogicSimulatorCompilationAndElaborationReport:
        return self._compilation_and_elaboration_report

    @property
    def regression_report(self) -> RegressionReport:
        return self._regression_report

    @property
    def success(self) -> bool:
        return self._success

    def needs_authentication(self) -> bool:
        return False

    def phase_init(self, phase: Phase):
        # Decompose IP Definition
        ip_target = "default"
        if "#" in self.parsed_cli_arguments.ip:
            spit_ip_def = self.parsed_cli_arguments.ip.split("#")
            if len(spit_ip_def) != 2:
                phase.error = Exception(f"Invalid IP/target specification: '{self.parsed_cli_arguments.ip}'")
                return
            else:
                ip_def_str = spit_ip_def[0].strip().lower()
                ip_target = spit_ip_def[1].strip().lower()
        else:
            ip_def_str = self.parsed_cli_arguments.ip.strip().lower()
        self._ip_definition = Ip.parse_ip_definition(ip_def_str)
        self.ip_definition.target = ip_target
        # Decompose Regression Definition
        if "." in self.parsed_cli_arguments.regr:
            split_regr_def = self.parsed_cli_arguments.regr.split('.')
            if len(split_regr_def) != 2:
                phase.error = Exception(f"Invalid regression specification: '{self.parsed_cli_arguments.regr}'")
                return
            else:
                self._test_suite_name_is_specified = True
                self._test_suite_name = split_regr_def[0].strip().lower()
                self._regression_name = split_regr_def[1].strip().lower()
        else:
            self._regression_name = self.parsed_cli_arguments.regr.strip().lower()
        self._dry_mode = self.parsed_cli_arguments.dry
        self._app = LogicSimulators[self.parsed_cli_arguments.app.upper()]

    def phase_post_validate_configuration_space(self, phase: Phase):
        if self.app == LogicSimulators.UNDEFINED:
            if not self.rmh.configuration.logic_simulation.default_simulator:
                phase.error = Exception(f"No simulator specified (-a/--app) and no default simulator in the Configuration")
                return
            else:
                self._app = self.rmh.configuration.logic_simulation.default_simulator.value
        if self.app == LogicSimulators.DSIM:
            self.rmh.configuration.project.local_mode = True

    def phase_post_scheduler_discovery(self, phase: Phase):
        try:
            # TODO Add support for other schedulers
            self._scheduler = self.rmh.scheduler_database.get_default_scheduler()
        except Exception as e:
            phase.error = e

    def phase_post_service_discovery(self, phase: Phase):
        try:
            self._simulator = self.rmh.service_database.find_service(ServiceType.LOGIC_SIMULATION, self.app.value)
            self._regression_database = self.rmh.service_database.find_default_service(ServiceType.REGRESSION)
        except Exception as e:
            phase.error = e
        else:
            if not self.simulator.supports_uvm:
                phase.error = Exception(f"Simulator '{self.simulator}' does not support UVM")

    def phase_post_ip_discovery(self, phase: Phase):
        self._ip = self.rmh.ip_database.find_ip_definition(self.ip_definition, raise_exception_if_not_found=False)
        if not self.ip:
            phase.error = Exception(f"IP '{self.ip_definition}' could not be found")
        else:
            if self.ip.ip.pkg_type != IpPkgType.DV_TB:
                phase.error = Exception(f"IP '{self.ip}' is not a Test Bench")
            else:
                self.regression_database.discover_test_suites(self.ip.root_path)
                if self.test_suite_name_is_specified:
                    self._regression = self.regression_database.find_regression(self.test_suite_name, self.regression_name, raise_exception_if_not_found=False)
                else:
                    self._regression = self.regression_database.find_regression_default_test_suite(self.regression_name, raise_exception_if_not_found=False)
                if not self._regression:
                    phase.error = Exception(f"Regression '{self.parsed_cli_arguments.regr}' could not be found")
                else:
                    self.regression.set_ip(self.ip)
                    if self.ip.has_vhdl_content:
                        # VHDL must be compiled and elaborated separately
                        self._do_compile = True
                        self._do_elaborate = True
                        self._do_compile_and_elaborate = False
                    else:
                        if self.simulator.supports_two_step_simulation:
                            self._do_compile = False
                            self._do_elaborate = False
                            self._do_compile_and_elaborate = True
                        else:
                            self._do_compile = True
                            self._do_elaborate = True
                            self._do_compile_and_elaborate = False
    
    def phase_main(self, phase: Phase):
        self.prepare_dut(phase)
        if not self.app == LogicSimulators.DSIM:
            if self.do_compile:
                self.compile(phase)
                if not self.compilation_report.success:
                    self._do_elaborate = False
                    self._do_simulate = False
            if self.do_elaborate:
                self.elaborate(phase)
                if not self.elaboration_report.success:
                    self._do_simulate = False
            if self.do_compile_and_elaborate:
                self.compile_and_elaborate(phase)
                if not self.compilation_and_elaboration_report.success:
                    self._do_simulate = False
        self.simulate(phase)

    def prepare_dut(self, phase: Phase):
        pass

    def compile(self, phase: Phase):
        self._compilation_configuration = self.regression.render_cmp_config(self.ip_definition.target)
        self.compilation_configuration.dry_mode = self.dry_mode
        self._compilation_report = self.simulator.compile(self.ip, self.compilation_configuration, self.scheduler)

    def elaborate(self, phase: Phase):
        self._elaboration_configuration = self.regression.render_elab_config(self.ip_definition.target)
        self._elaboration_configuration.dry_mode = self.dry_mode
        self._elaboration_report = self.simulator.elaborate(self.ip, self.elaboration_configuration, self.scheduler)

    def compile_and_elaborate(self, phase: Phase):
        self._compilation_and_elaboration_configuration = self.regression.render_cmp_elab_config(self.ip_definition.target)
        self._compilation_and_elaboration_configuration.dry_mode = self.dry_mode
        self._compilation_and_elaboration_report = self.simulator.compile_and_elaborate(self.ip, self.compilation_and_elaboration_configuration, self.scheduler)

    def simulate(self, phase: Phase):
        self._regression_configuration = RegressionConfiguration()
        self.regression_configuration.target = self.ip_definition.target
        self.regression_configuration.dry_mode = self.dry_mode
        self.regression_configuration.app = self.app
        self._regression_runner = self.regression_database.get_regression_runner(self.ip, self.regression, self.simulator, self.regression_configuration)
        self._regression_report = self.regression_runner.execute_regression(self.scheduler)
        if self.app == LogicSimulators.DSIM:
            self._compilation_report = self.regression_report.compilation_report
            self._elaboration_report = self.regression_report.elaboration_report
            self._compilation_and_elaboration_report = self.regression_report.compilation_and_elaboration_report

    def phase_report(self, phase: Phase):
        self._success = True
        if self.do_compile:
            self._success &= self.compilation_report.success
        if self.do_elaborate:
            self._success &= self.elaboration_report.success
        if self.do_compile_and_elaborate:
            self._success &= self.compilation_and_elaboration_report.success
        self._success &= self.regression_report.success
        if self.success:
            banner = f"{'*' * 53}\033[32m SUCCESS \033[0m{'*' * 54}"
        else:
            banner = f"{'*' * 53}\033[31m\033[4m FAILURE \033[0m{'*' * 54}"
        print(banner)
        self.print_prepare_dut_report(phase)
        if self.do_compile:
            self.print_compilation_report(phase)
        if self.do_elaborate:
            self.print_elaboration_report(phase)
        if self.do_compile_and_elaborate:
            self.print_compilation_and_elaboration_report(phase)
        self.print_regression_report(phase)
        print(banner)

    def phase_final(self, phase: Phase):
        if not self.dry_mode:
            if not self.success:
                phase.error = Exception(f"Logic Simulation Regression failed.")

    def print_prepare_dut_report(self, phase: Phase):
        pass

    def print_compilation_report(self, phase: Phase):
        if not self.dry_mode:
            errors_str = f"\033[31m\033[1m{self.compilation_report.num_errors}E\033[0m" if self.compilation_report.num_errors > 0 else "0E"
            warnings_str = f"\033[33m\033[1m{self.compilation_report.num_warnings}W\033[0m" if self.compilation_report.num_warnings > 0 else "0W"
            fatal_str = f" \033[33m\033[1mF\033[0m" if self.compilation_report.num_fatals > 0 else ""
            if self.compilation_report.has_sv_files_to_compile and self.compilation_report.has_vhdl_files_to_compile:
                print(f" Compilation results - {errors_str} {warnings_str}{fatal_str}:")
                print(f"  * {self.rmh.configuration.applications.editor} {self.compilation_report.sv_log_path}")
                print(f"  * {self.rmh.configuration.applications.editor} {self.compilation_report.vhdl_log_path}")
            else:
                if self.compilation_report.has_sv_files_to_compile:
                    print(f" Compilation results - {errors_str} {warnings_str}{fatal_str}:")
                    print(f"  * {self.rmh.configuration.applications.editor} {self.compilation_report.sv_log_path}")
                if self.compilation_report.has_vhdl_files_to_compile:
                    print(f" Compilation results - {errors_str} {warnings_str}{fatal_str}:")
                    print(f"  * {self.rmh.configuration.applications.editor} {self.compilation_report.vhdl_log_path}")
            if not self.compilation_report.success:
                print('*' * 119)
                for error in self.compilation_report.errors:
                    print(f"\033[31m{error}\033[0m")
                for fatal in self.compilation_report.fatals:
                    print(f"\033[31m{fatal}\033[0m")
    
    def print_elaboration_report(self, phase: Phase):
        if not self.dry_mode:
            errors_str = f"\033[31m\033[1m{self.elaboration_report.num_errors}E\033[0m" if self.elaboration_report.num_errors > 0 else "0E"
            warnings_str = f"\033[33m\033[1m{self.elaboration_report.num_warnings}W\033[0m" if self.elaboration_report.num_warnings > 0 else "0W"
            fatal_str = f" \033[33m\033[1mF\033[0m" if self.elaboration_report.num_fatals > 0 else ""
            print(f" Elaboration results - {errors_str} {warnings_str}{fatal_str}:")
            print(f"  * Log: {self.rmh.configuration.applications.editor} {self.elaboration_report.log_path}")
            if not self.elaboration_report.success:
                print('*' * 119)
                for error in self.elaboration_report.errors:
                    print(f"\033[31m{error}\033[0m")
                for fatal in self.elaboration_report.fatals:
                    print(f"\033[31m{fatal}\033[0m")
    
    def print_compilation_and_elaboration_report(self, phase: Phase):
        if not self.dry_mode:
            errors_str = f"\033[31m\033[1m{self.compilation_and_elaboration_report.num_errors}E\033[0m" if self.compilation_and_elaboration_report.num_errors > 0 else "0E"
            warnings_str = f"\033[33m\033[1m{self.compilation_and_elaboration_report.num_warnings}W\033[0m" if self.compilation_and_elaboration_report.num_warnings > 0 else "0W"
            fatal_str = f" \033[33m\033[1mF\033[0m" if self.compilation_and_elaboration_report.num_fatals > 0 else ""
            print(f" Compilation+Elaboration results - {errors_str} {warnings_str}{fatal_str}:")
            print(f"  * Log: {self.rmh.configuration.applications.editor} {self.compilation_and_elaboration_report.log_path}")
            if not self.compilation_and_elaboration_report.success:
                print('*' * 119)
                for error in self.compilation_and_elaboration_report.errors:
                    print(f"\033[31m{error}\033[0m")
                for fatal in self.compilation_and_elaboration_report.fatals:
                    print(f"\033[31m{fatal}\033[0m")

    def print_regression_report(self, phase: Phase):
        if self.dry_mode:
            print(f" Regression Dry Mode - {len(self.regression_configuration.simulation_configs)} tests would have been run:")
            for seed in self.regression_configuration.simulation_configs:
                simulation_config = self.regression_configuration.simulation_configs[seed]
                print(f" * {simulation_config.summary_str()}")
            if self.parsed_cli_arguments.app == "dsim":
                print(f" DSim Cloud Simulation Job File: '{self.regression_report.dsim_cloud_simulation_job_file_path}'")
        else:
            self.regression_report.generate_junit_xml_report()
            self.regression_report.generate_html_report()
            if self.regression_report.success:
                print(f" Regression passed: {len(self.regression_report.simulation_reports)} tests")
            else:
                print(f"{len(self.regression_report.failing_tests)} tests failed:")
                for failed_test in self.regression_report.failing_tests:
                    args_str: str = ""
                    for arg in failed_test.sim_report.user_args_boolean:
                        args_str += f" +{arg}"
                    for arg in failed_test.sim_report.user_args_value:
                        args_str += f" +{arg}={failed_test.sim_report.user_args_value[arg]}"
                    print(f" * {failed_test.sim_report.test_name} - {failed_test.sim_report.seed}{args_str}")
            print(f"T est Report: '{self.regression_report.html_report_file_name}'")
            if self.regression_report.cov_enabled:
                print(f" Coverage Report: '{self.regression_report.coverage_report_file_name}'")
            print(f" JUnit XML Report: '{self.regression_report.junit_xml_report_file_name}'")
