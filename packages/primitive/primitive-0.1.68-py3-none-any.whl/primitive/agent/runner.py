import os
import threading
import typing
from pathlib import Path, PurePath
from time import sleep
from typing import Dict, Iterable, List, Optional, TypedDict

import yaml
from loguru import logger
from .process import Process
from .provision import ProvisionPython
from ..utils.cache import get_artifacts_cache, get_logs_cache
from ..utils.files import find_files_for_extension

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

if typing.TYPE_CHECKING:
    import primitive.client


class Artifact(TypedDict):
    name: str
    extension: str


class JobStep(TypedDict):
    name: str
    workdir: str
    artifacts: List[Artifact]
    cmd: str


class JobDescription(TypedDict):
    name: str
    provision: str
    steps: List[JobStep]


class AgentRunner:
    def __init__(
        self,
        primitive: "primitive.client.Primitive",
        source_dir: Path,
        job_id: str,
        job_slug: str,
        max_log_size: int = 10 * 1024 * 1024,
        job: Optional[JobDescription] = None,
    ) -> None:
        self.primitive = primitive
        self.source_dir = source_dir
        self.workdir = "."
        self.job_id = job_id
        self.job_slug = job_slug
        self.max_log_size = max_log_size
        self.artifacts_dir = get_artifacts_cache(self.job_id)
        self.logs_dir = get_logs_cache(self.job_id)
        self.logger_handle = None

        logger.enable("primitive")
        self.swap_logs(label="init")

        if job:
            self.job = job
        else:
            self.load_job_from_file()
    
    def load_job_from_file(self) -> JobDescription:
        logger.info(f"Scanning directory for job file {self.job_slug}")

        # Look for job based on slug
        yaml_file = Path(self.source_dir / ".primitive" / f"{self.job_slug}.yaml")
        yml_file = Path(self.source_dir / ".primitive" / f"{self.job_slug}.yml")

        if yaml_file.exists() and yml_file.exists():
            logger.error(
                f"Found two job descriptions with the same slug: {self.job_slug}"
            )
            self.conclude(conclusion="failure")
            raise FileExistsError

        if yaml_file.exists():
            self.job = yaml.load(open(yaml_file, "r"), Loader=Loader)
        elif yml_file.exists():
            self.job = yaml.load(open(yml_file, "r"), Loader=Loader)
        else:
            logger.error(
                f"No job description with matching slug '{self.job_slug}' found"
            )
            self.conclude(conclusion="failure")
            raise FileNotFoundError

        logger.info(f"Found job description for {self.job_slug}")

    def name(self) -> str:
        return self.job["name"]

    def steps(self) -> Iterable[JobStep]:
        for step in self.job["steps"]:
            yield step

    def execute(self) -> None:
        logger.info(f"Executing {self.job_slug} job")
        self.primitive.jobs.job_run_update(self.job_id, status="request_in_progress")

        # Initial environment is the system env
        environment = os.environ
        if "provision" in self.job:
            logger.info(f"Provisioning for {self.job['provision']} environment")
            environment = self.provision()

            if not environment:
                self.conclude("failure")
                return

        conclusion = None
        total_errors = 0
        for step in self.steps():
            # Swap logger
            self.swap_logs(label=step["name"])

            logger.info(f"Beginning step {step['name']}")

            # Update workdir
            if "workdir" in step:
                self.workdir = step["workdir"]

            # Define step proc
            proc = Process(
                cmd=step["cmd"],
                workdir=Path(self.source_dir / self.workdir),
                env=environment,
            )

            # Try to start
            try:
                proc.start()
            except Exception as e:
                logger.error(f"Error while attempting to run command {e}")
                conclusion = "failure"
                break

            def status_check():
                while proc.is_running():
                    # Check job status
                    status = self.primitive.jobs.get_job_status(self.job_id)
                    status_value = status.data["jobRun"]["status"]

                    # TODO: Should probably use request_cancelled or something
                    # once we change it, we'll have to call conclude w/ cancelled status
                    if status_value == "completed":
                        logger.warning("Job cancelled by user")
                        proc.terminate()
                        return

                    sleep(5)

            status_thread = threading.Thread(target=status_check)
            status_thread.start()

            # Wait for proc to finish
            returncode = proc.wait()
            total_errors += proc.errors

            # Wait for status check
            status_thread.join()

            # Collect artifacts
            if "artifacts" in step:
                self.collect_artifacts(step)

            # Check if we have a good result
            if returncode > 0:
                conclusion = "failure"
                break

        if not conclusion and total_errors == 0:
            conclusion = "success"
        else:
            logger.error(f"Job failed with {total_errors} errors.")
            conclusion = "failure"

        self.conclude(conclusion)

    def conclude(self, conclusion: str) -> None:
        self.primitive.jobs.job_run_update(
            self.job_id, status="request_completed", conclusion=conclusion
        )

        logger.info(f"Completed {self.job_slug} job")
        logger.remove(self.logger_handle)

    def swap_logs(self, label: str):
        # Remove Handle
        if self.logger_handle:
            logger.remove(self.logger_handle)
        
        # Custom format for UTC time
        logger_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS!UTC}</green> | "
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )

        self.logger_handle = logger.add(
            Path(self.logs_dir / f"{label}_{{time}}.primitive.log"),
            rotation=self.max_log_size,
            format=logger_format
        )

    def provision(self) -> Optional[Dict]:
        match self.job["provision"]:
            case "python":
                requirements_glob = self.source_dir.rglob("requirements.txt")

                requirements_path = next(requirements_glob, None)

                if not requirements_path:
                    logger.error("Unable to locate requirements.txt")
                    return None

                prov = ProvisionPython(self.source_dir, requirements_path)
                return prov.create_env()

    def collect_artifacts(self, step: JobStep) -> None:
        # Search each artifact type
        for artifact in step["artifacts"]:
            files = find_files_for_extension(self.source_dir, artifact["extension"])

            for file in files:
                # Find path relative to source_dir
                relative_path = PurePath(file).relative_to(self.source_dir)

                # Construct destination to preserve directory structure
                destination = Path(self.artifacts_dir / relative_path)

                # Create directories if they don't exist
                destination.parent.mkdir(parents=True, exist_ok=True)

                # Move file
                file.rename(destination)
