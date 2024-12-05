# -*- coding: utf-8 -*-

"""

glsr_present.commandline

Command line functionality

Copyright (C) 2023-2024 Rainer Schwarzbach

This file is part of glsr-present.

glsr-present is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

glsr-present is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

import argparse
import json
import logging
import os
import pathlib
import shutil

# import sys

from typing import List, Optional, Tuple

import jinja2

from glsr_present import __version__


#
# Constants
#


RETURNCODE_OK = 0
RETURNCODE_ERROR = 1

BUILD_VARS = (
    "CI_PIPELINE_CREATED_AT",
    "CI_PIPELINE_ID",
    "CI_PIPELINE_URL",
    "CI_PROJECT_TITLE",
    "CI_PROJECT_URL",
    "CI_COMMIT_SHA",
)

DEFAULT_BUILTIN_TEMPLATE = "build-info.md.j2"
TEMPLATE_EXTENSION = "j2"


#
# classes
#


class Program:
    """Command line program"""

    name: str = "glsr-present"
    description: str = (
        "Provide build information and pretty-printed"
        " GitLab security reports in a CI pipeline"
    )

    def __init__(self, args: Optional[List[str]] = None) -> None:
        """Parse command line arguments and initialize the logger

        :param args: a list of command line arguments
        """
        self.__arguments = self._parse_args(args)
        if self.__arguments.loglevel < logging.INFO:
            message_format = "%(levelname)-8s | (%(funcName)s:%(lineno)s) %(message)s"
        else:
            message_format = "%(levelname)-8s | %(message)s"
        #
        logging.basicConfig(
            format=message_format,
            level=self.__arguments.loglevel,
        )

    @property
    def arguments(self) -> argparse.Namespace:
        """Property: command line arguments

        :returns: the parsed command line arguments
        """
        return self.__arguments

    def _parse_args(self, args: Optional[List[str]]) -> argparse.Namespace:
        """Parse command line arguments using argparse
        and return the arguments namespace.

        :param args: a list of command line arguments,
            or None to parse sys.argv
        :returns: the parsed command line arguments as returned
            by argparse.ArgumentParser().parse_args()
        """
        main_parser = argparse.ArgumentParser(
            prog=self.name,
            description=self.description,
        )
        main_parser.set_defaults(
            loglevel=logging.WARNING,
            output_directory=pathlib.Path("docs"),
            builtin_template=DEFAULT_BUILTIN_TEMPLATE,
            reports_path=pathlib.Path.cwd(),
        )
        main_parser.add_argument(
            "--version",
            action="version",
            version=__version__,
            help="print version and exit",
        )
        logging_group = main_parser.add_argument_group(
            "Logging options", "control log level (default is WARNING)"
        )
        verbosity_mutex = logging_group.add_mutually_exclusive_group()
        verbosity_mutex.add_argument(
            "-d",
            "--debug",
            action="store_const",
            const=logging.DEBUG,
            dest="loglevel",
            help="output all messages (log level DEBUG)",
        )
        verbosity_mutex.add_argument(
            "-v",
            "--verbose",
            action="store_const",
            const=logging.INFO,
            dest="loglevel",
            help="be more verbose (log level INFO)",
        )
        verbosity_mutex.add_argument(
            "-q",
            "--quiet",
            action="store_const",
            const=logging.ERROR,
            dest="loglevel",
            help="be more quiet (log level ERROR)",
        )
        templates_group = main_parser.add_argument_group(
            "Template option",
            "Select a builtin template or one from the file system"
            " for the overview page",
        )
        template_mutex = templates_group.add_mutually_exclusive_group()
        template_mutex.add_argument(
            "-b",
            "--builtin-template",
            metavar="TEMPLATE_NAME",
            help="use the built-in template %(metavar)s (default: %(default)s)",
        )
        template_mutex.add_argument(
            "-f",
            "--template-file",
            metavar="TEMPLATE_PATH",
            help="use the template from file %(metavar)s",
        )
        main_parser.add_argument(
            "-l",
            "--list-templates",
            action="store_true",
            help="list available templates and exit",
        )
        main_parser.add_argument(
            "-n",
            "--dry-run",
            action="store_true",
            help="no action (dry run): do not write any files",
        )
        main_parser.add_argument(
            "-o",
            "--output-directory",
            metavar="DESTINATION",
            type=pathlib.Path,
            help="write files to directory %(metavar)s (default: %(default)s)",
        )
        main_parser.add_argument(
            "-r",
            "--reports-path",
            metavar="DIRECTORY",
            type=pathlib.Path,
            help="read reports from %(metavar)s (default: %(default)s)",
        )
        main_parser.add_argument(
            "-s",
            "--skip-reports",
            action="store_true",
            help="skip reading reports, just provide build information",
        )
        return main_parser.parse_args(args)

    def _copy_file(
        self, source_path: pathlib.Path, target_directory: pathlib.Path
    ) -> None:
        """Copy a file if no dry run was requested"""
        if self.arguments.dry_run:
            logging.info(
                "Dry run: Would have copied %s to %s",
                source_path.name,
                target_directory,
            )
        else:
            logging.info("Copying %s to %s", source_path.name, target_directory)
            shutil.copy2(source_path, target_directory / source_path.name)
        #

    def _get_reports_data(
        self, reports_path: pathlib.Path, skip: bool = False
    ) -> List[Tuple[str, str, str]]:
        """Get report names, types and file names
        during copying them to the target directory
        """
        reports_data: List[Tuple[str, str, str]] = []
        if skip:
            return reports_data
        #
        report_source_path = reports_path.resolve()
        for source_file in report_source_path.glob("gl-*-report.json"):
            self._copy_file(source_file, self.arguments.output_directory)
            report_name = source_file.name[3:-12]
            if report_name in (
                "iac-sast",
                "container-scanning",
                "secret-detection",
            ):
                report_type = report_name
            elif "sast" in report_name:
                report_type = "sast"
            else:
                continue
            #
            reports_data.append((report_name, report_type, source_file.name))
        #
        return reports_data

    def _write_build_info(
        self,
        j2_template: jinja2.Template,
        reports_data: List[Tuple[str, str, str]],
    ) -> None:
        """Write build info JSON and markdown files"""
        build_info = {name.lower(): os.getenv(name, "") for name in BUILD_VARS}
        reports_files_data: List[Tuple[str, pathlib.Path, str]] = [
            (
                "JSON",
                self.arguments.output_directory / "build-info.json",
                json.dumps(build_info, indent=2),
            ),
            (
                "page",
                self.arguments.output_directory / str(j2_template.name)[:-3],
                j2_template.render(
                    build_info=build_info,
                    reports_data=reports_data,
                    version=__version__,
                ),
            ),
        ]
        if self.arguments.dry_run:
            separator_line = "-" * 60
            logging.info(separator_line)
            for subject, path, content in reports_files_data:
                logging.info("Dry run: would have written %s data", subject)
                logging.info("         to %s:", path)
                for line in content.splitlines():
                    logging.info(line)
                #
                logging.info(separator_line)
            #
            return
        #
        for subject, path, content in reports_files_data:
            logging.info("Writing %s data to %s", subject, path)
            with open(path, "w", encoding="utf-8") as output_file:
                output_file.write(content)
            #
        #

    def _copy_static_files(
        self,
        reports_data: List[Tuple[str, str, str]],
    ) -> None:
        """Copy static files to the target directory
        if required (= if there are any reports)
        """
        base_path = pathlib.Path(__file__).parent.resolve()
        if reports_data:
            source_path = base_path / "static"
            for source_file in source_path.glob("*"):
                self._copy_file(source_file, self.arguments.output_directory)
            #
        #
        if not self.arguments.dry_run:
            logging.info("Files in %s:", self.arguments.output_directory)
            for file_path in self.arguments.output_directory.glob("*"):
                logging.info(" - %s", file_path)
            #
        #

    def execute(self) -> int:
        """Execute the program
        :returns: the returncode for the script
        """
        loader: jinja2.BaseLoader
        if self.arguments.template_file:
            template_path = pathlib.Path(self.arguments.template_file)
            loader = jinja2.FileSystemLoader(template_path.parent)
            template_name = template_path.name
        else:
            loader = jinja2.PackageLoader("glsr_present")
            template_name = self.arguments.builtin_template
        #
        if not template_name.endswith(f".{TEMPLATE_EXTENSION}"):
            logging.error(
                "The template name must have the extension %r",
                TEMPLATE_EXTENSION,
            )
            return RETURNCODE_ERROR
        #
        j2_env = jinja2.Environment(
            loader=loader,
            autoescape=jinja2.select_autoescape(),
        )
        if self.arguments.list_templates:
            logging.info("Available templates:")
            for found_template in j2_env.list_templates([TEMPLATE_EXTENSION]):
                print(found_template)
            #
            return RETURNCODE_OK
        #
        try:
            j2_template = j2_env.get_template(template_name)
        except jinja2.exceptions.TemplateNotFound as error:
            logging.error("Template not found: %s", error)
            return RETURNCODE_ERROR
        #
        if not self.arguments.output_directory.is_dir():
            if self.arguments.output_directory.exists():
                details = "exists, but is not a directory"
            else:
                details = "does not exist"
            #
            logging.error(
                "The output destination %s %s",
                self.arguments.output_directory,
                details,
            )
            return RETURNCODE_ERROR
        #
        reports_data = self._get_reports_data(
            self.arguments.reports_path, skip=self.arguments.skip_reports
        )
        self._write_build_info(j2_template, reports_data)
        self._copy_static_files(reports_data)
        return RETURNCODE_OK


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
