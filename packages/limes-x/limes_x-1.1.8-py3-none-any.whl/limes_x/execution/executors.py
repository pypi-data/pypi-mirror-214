from __future__ import annotations
import os, sys
import time
import json
from pathlib import Path
from typing import Callable, Iterable
import inspect
from threading import Condition

from .modules import ComputeModule, JobContext, JobResult, Params, Item
from .instances import JobInstance
from .comms import FileSyncedDictionary, CommsObject
from ..common.utils import LiveShell, Timestamp, CurrentTimeMillis

class Job:
    instance: JobInstance
    context: JobContext
    run_command: str
    workspace: Path
    _verbose: bool

    def __init__(self, instance: JobInstance, workspace: Path, params: Params, _save=True) -> None:
        self.instance = instance
        self.workspace = workspace
        self._verbose = True

        c = JobContext()
        c.job_id = self.instance.GetID()
        c.output_folder = Path(instance.GetFolderName())
        c.params = params.Copy()
        c.manifest = dict((Item(k), [ii.value for ii in v] if isinstance(v, list) else v.value) for k, v in self.instance.inputs.items())
        if _save: c.Save(workspace)
        self.context = c

    def SaveContext(self):
        self.context.Save(self.workspace)

    def Shell(self, cmd: str):
        err_log = []
        pr = lambda s: print(s, end="")
        code=LiveShell(cmd, echo_cmd=False, onErr=lambda s: err_log.append(s), onOut=pr if self._verbose else lambda s: None)
        return code==0, "".join(err_log)

ExecutionHandler = Callable[[Job], tuple[bool, str]]
SetupHandler = Callable[[list[ComputeModule], Path, Params], None]
class Executor:
    def __init__(self, execute_procedure: ExecutionHandler|None=None, prepare_procedure: SetupHandler|None=None) -> None:
        self._execute_procedure: ExecutionHandler = execute_procedure if execute_procedure is not None else lambda j: j.Shell(j.run_command)
        self._prepare_run = (lambda x, y, z: None) if prepare_procedure is None else prepare_procedure
        self._sync = Condition()

    # currently not used
    def PrepareRun(self, modules: list[ComputeModule], inputs_folder: Path, params: Params):
        self._prepare_run(modules, inputs_folder, params)

    def _print_start(self, job: Job):
        with self._sync:
            print(f"{Timestamp()}    - started {job.instance.step.name}:{job.instance.GetID()}")
            sys.stdout.flush()

    def _override_params(self, job: Job):
        step = job.instance.step
        params = job.context.params
        if step.threads is not None: params.threads = step.threads
        if step.memory_gb is not None: params.mem_gb = step.memory_gb
        return job

    def _make_job(self, instance: JobInstance, workspace: Path, params: Params, _save=True, _override=False):
        job = Job(
            instance = instance,
            workspace = workspace,
            params = params,
            _save = False,
        )
        if _override: job = self._override_params(job)
        if _save: job.context.Save(workspace=workspace)
        return job

    def Run(self, instance: JobInstance, workspace: Path, params: Params) -> JobResult:
        job = self._make_job(instance, workspace, params)

        from ..environments import local
        entry_point = Path(os.path.abspath(inspect.getfile(local)))
        args = [
            entry_point, job.instance.step.location, workspace, job.context.output_folder, False,
        ]
        job.run_command = f"""\
            PYTHONPATH={':'.join(os.path.abspath(p) for p in sys.path)}
            python {" ".join(f'"{a}"' for a in args)}
        """[:-1].replace("  ", "")
        # self._print_start(job)
        success, msg = self._execute_procedure(job)

        return self._compile_result(job, success, msg)

    def _compile_result(self, job: Job, success: bool, msg: str):
        if not success:
            return self._make_failed_result(job.instance, msg)
        else:
            return self._get_result(job.context, job.instance)

    def _get_result(self, context: JobContext, job: JobInstance) -> JobResult:
        result_json = context.output_folder.joinpath('result.json')
        if not os.path.exists(result_json):
            w = context.params.file_system_wait_sec
            if w > 0:
                print(f"waiting {w} sec. for {job.step.name}:{job.GetID()}")
                time.sleep(w)

        if os.path.exists(result_json):
            err_msg = None
            try:
                with open(result_json) as j:
                    r = JobResult.FromDict(json.load(j))
                    r.made_by = job.GetID()
                    if r.manifest is None:
                        r.error_message = f"no output created{'' if r.error_message is None else f', err: {r.error_message}'}"
                        r.manifest = {}
                    else:
                        realtime_log = context.output_folder.joinpath("realtime.log")
                        if os.path.exists(realtime_log): os.remove(realtime_log)
                    return r
            except Exception as e:
                err_msg = f'result manifest corrupted'
        else:
            WS = '{workspace}'
            err_msg = f'missing result manifest at [{WS}/{result_json}]'

        r = JobResult()
        r.made_by = job.GetID()
        if err_msg is not None:
            if err_msg[-1] == '\n': err_msg = err_msg[:-1]
            r.error_message = err_msg
        return r

    def _make_failed_result(self, job: JobInstance, msg: str):
        r = JobResult()
        r.made_by = job.GetID()
        r.error_message = f"executor failed:\n{msg}"
        return r

class HpcExecutor(Executor):
    _EXT = 'tgz'
    _SRC_FOLDER_NAME = 'limesx_src'
    _NO_ZIP = ['tgz', 'tar.gz', 'sif']

    def __init__(self,
        hpc_procedure: ExecutionHandler,
        logistical_procedure: ExecutionHandler|None=None,
        prerun: Callable[[Path], None] | None = None,
        tmp_dir_name: str="TMP",
    ) -> None:

        def _prepare_run(modules: list[ComputeModule], inputs_dir: Path, params: Params):
            _shell = lambda cmd: LiveShell(cmd=cmd.replace('  ', ''), echo_cmd=False)
            HERE = os.getcwd()
            EXT = self._EXT
            THREADS = params.threads

            ## limes_x env ##
            import limes_x
            src = os.path.abspath(Path(os.path.dirname(inspect.getfile(limes_x))).joinpath('..'))
            _shell(f"""\
                cd {src}
                tar --exclude=__pycache__ -hcf - {limes_x.__name__} | pigz -5 -p {THREADS} >{HERE}/{self._SRC_FOLDER_NAME}.{EXT}
            """)    
            if prerun is not None: prerun(inputs_dir)
            sys.stdout.flush()
            
        super().__init__(execute_procedure=logistical_procedure, prepare_procedure=_prepare_run)
        self._hpc_procedure = hpc_procedure
        self._tmp_dir_name = tmp_dir_name
        self.max_active_io_jobs: int = 5
        self.update_frequency: int|float = 5
        self._num_active_io: int = 0
        self._last_check: int = 0
        self._first_run = True

    def _can_run(self, workspace: Path, key: str, force_update: bool=False):
        elapsed = (CurrentTimeMillis() - self._last_check)/1000.0
        def _update():
            perm = False
            with FileSyncedDictionary(workspace) as com:
                if self._first_run:
                    com.Clear()
                    self._first_run = False
                if len(com.GetIoTasks()) < self.max_active_io_jobs:
                    com.QueueIoTask(key)
                    com.SwitchIoTaskToActive(key)
                    perm = True
                self._num_active_io = len(com.GetIoTasks())
            return perm

        permission = False
        if force_update or elapsed >= self.update_frequency or self._num_active_io < self.max_active_io_jobs:
            permission = _update()
            self._last_check = CurrentTimeMillis()
        return permission

    def Run(self, instance: JobInstance, workspace: Path, params: Params) -> JobResult:
        job = self._make_job(instance, workspace, params, _override=True)

        from ..environments import hpc
        entry_point = Path(os.path.abspath(inspect.getfile(hpc)))
        args = [
            entry_point, job.instance.step.location, workspace, job.context.output_folder, False,
            workspace.joinpath(f'{self._SRC_FOLDER_NAME}.{self._EXT}'), self._tmp_dir_name,
        ]
        job.run_command = f"""\
            python {" ".join(f'"{a}"' for a in args)}\
        """.replace("  ", "")
        job._verbose = False # since non local

        success, msg = False, ""
        try:
            me = job.context.job_id
            if not self._can_run(workspace, me, force_update=True):
                while not self._can_run(workspace, me):
                    time.sleep(self.update_frequency)
            # print(f"- started {job.context.job_id}")
            # self._print_start(job)
            success, msg = self._hpc_procedure(job)
        except Exception as e:
            success, msg = False, str(e)
            print(f"ERROR: in executor: {e}")
            sys.stdout.flush()
        except KeyboardInterrupt:
            success, msg = False, "force stopped"
            print(f"force stopped")
        finally:
            with FileSyncedDictionary(workspace) as com:
                com.RemoveIoTask(job.context.job_id)

        result = self._compile_result(job, success, msg)
        return result

