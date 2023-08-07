import copy
import logging
from importlib import import_module
from pathlib import Path
from typing import Optional

from termcolor import colored

from ..constants import CONFIG_DIR_NAME, DEFAULT_PROVIDER


def get_job_prefix(pipeline_name: str, job_name: str) -> Optional[str]:
    if job_name.startswith("."):
        return None
    return f"{pipeline_name}-"


def parse_groups(name, file, groups):
    if groups:
        groups = [group.strip() for group in groups.split(",")]

    if not groups:
        group_names = set()
        for job_name in file.jobs.keys():
            if job_name.startswith("."):
                continue
            group_name = job_name[len(f"{name}-") :]
            group_name = group_name.split("-")[0]
            group_names.add(group_name)
        groups = sorted(list(group_names))
    return groups


def bundle_command(parser, args):
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    print(colored("pipeline name:", color="yellow"), args.pipeline_name)

    provider = import_module(f".{DEFAULT_PROVIDER}", "cici.providers")

    ci_file_path = args.config_path / provider.CI_FILE

    if not Path(ci_file_path).exists():
        parser.error(f"file not found: {ci_file_path}")

    file = provider.load(ci_file_path)

    args.output_path = Path(args.output_path)
    args.groups = parse_groups(args.pipeline_name, file, args.groups)
    print(colored("bundle names:", color="yellow"), args.groups)

    for bundle_name in args.groups:
        pattern = f"{args.pipeline_name}-{bundle_name}"

        bundle = copy.deepcopy(file)
        bundle.jobs = {}

        for job_name, job in file.jobs.items():
            job_prefix = get_job_prefix(
                pipeline_name=args.pipeline_name,
                job_name=job_name,
            )
            if not job_prefix:
                continue
            assert job_name.startswith(job_prefix)
            if job_name.startswith(pattern):
                bundle.jobs[job_name] = job

        bundle_filename = args.output_path / f"{bundle_name}.yml"

        with open(bundle_filename, "w") as stream:
            provider.dump(bundle, stream)
        print(colored("created", "magenta"), bundle_filename.name)


def bundle_parser(subparsers):
    parser = subparsers.add_parser(
        "bundle", help="distill a CI file to a job and its dependencies"
    )
    parser.add_argument(
        "config_path",
        metavar="DIR",
        nargs="?",
        type=Path,
        default=(Path.cwd() / CONFIG_DIR_NAME).absolute(),
    )
    parser.add_argument("-g", "--groups", help="job group patterns")
    parser.add_argument(
        "-o",
        "--output",
        metavar="DIR",
        dest="output_path",
        type=Path,
        default=Path.cwd().absolute(),
    )
    parser.add_argument(
        "-n",
        "--name",
        metavar="DIR",
        dest="pipeline_name",
        default=str(Path.cwd().name),
        help="the name of the pipeline",
    )
    parser.set_defaults(func=bundle_command)
    return parser
