import os

import typer

from sw_ut_report.__init__ import __version__
from sw_ut_report.parse_txt_file import SummaryRequirementsStatus, generate_test_cases
from sw_ut_report.parse_xml_file import format_xml_to_dict
from sw_ut_report.utils import (
    extract_tag_date_and_clean_filename,
    generate_single_markdown,
    read_file_content,
)

cli = typer.Typer()


def input_folder_option() -> typer.Option:
    return typer.Option(
        ...,
        "--input-folder",
        help="Path to the folder containing the txt and xml files",
    )


def ci_commit_tag_option() -> typer.Option:
    return typer.Option(
        None,
        "--ci-commit-tag",
        help="Pipeline GitLab variable $CI_COMMIT_TAG",
    )


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
    input_folder: str = input_folder_option(),
    ci_commit_tag: str = ci_commit_tag_option(),
):
    if ctx.invoked_subcommand is None:
        generate_report(input_folder, ci_commit_tag)


@cli.command()
def generate_report(
    input_folder: str = input_folder_option(),
    ci_commit_tag: str = ci_commit_tag_option(),
):
    typer.echo("Test results generation started")

    reports = []
    summary_requirements = SummaryRequirementsStatus()

    try:
        file_list = os.listdir(input_folder)
    except FileNotFoundError:
        typer.echo(f"Path '{input_folder}' does not exist.")
        raise typer.Exit(code=1)
    except PermissionError:
        typer.echo(f"Permission denied for the folder '{input_folder}'.")
        raise typer.Exit(code=1)

    for filename in file_list:
        input_file = os.path.join(input_folder, filename)
        _, file_extension = os.path.splitext(filename)

        tag, date, clean_filename = extract_tag_date_and_clean_filename(filename)
        match file_extension.lower():
            case ".txt":
                test_cases, summary_requirements = generate_test_cases(
                    read_file_content(input_file), summary_requirements
                )
                reports.append(
                    {
                        "type": "txt",
                        "filename": clean_filename,
                        "tag": tag,
                        "date": date,
                        "test_cases": test_cases,
                    }
                )

            case ".xml":
                suites_data, summary_requirements = format_xml_to_dict(
                    input_file, summary_requirements
                )
                reports.append(
                    {
                        "type": "xml",
                        "filename": clean_filename,
                        "tag": tag,
                        "date": date,
                        "content": suites_data,
                    }
                )

            case _:
                if os.path.isdir(input_file):
                    typer.echo(f"Skipping folder: {filename}")
                    continue
                else:
                    print(f"Skipping unsupported file format: {filename}")
                    continue

    summary_requirements.sort_summary()
    generate_single_markdown(reports, summary_requirements.summary, ci_commit_tag)
    typer.echo("Markdown report generated.")
