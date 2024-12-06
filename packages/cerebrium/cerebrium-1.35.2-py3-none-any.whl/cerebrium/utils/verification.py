import os
import tempfile
import sys

from cerebrium.utils.logging import cerebrium_log


def run_pyflakes(
    dir: str = "",
    files: list[str] = [],
    print_warnings: bool = True,
) -> tuple[list[str], list[str]]:
    try:
        import pyflakes.api
        from pyflakes.reporter import Reporter
    except ImportError:
        cerebrium_log(
            prefix="Error: Pyflakes is not installed.",
            message="To use the linting functionality, please install pyflakes by running `pip install pyflakes`.",
            level="ERROR",
        )
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp:
        warnings_log_file = os.path.join(tmp, "warnings.log")
        errors_log_file = os.path.join(tmp, "errors.log")

        with (
            open(errors_log_file, "w") as warnings_log,
            open(warnings_log_file, "w") as errors_log,
        ):
            reporter = Reporter(warningStream=warnings_log, errorStream=errors_log)
            if dir:
                pyflakes.api.checkRecursive([dir], reporter=reporter)
            elif files:
                for filename in files:
                    if os.path.splitext(filename)[1] != ".py":
                        continue
                    code = open(filename, "r").read()
                    pyflakes.api.check(code, filename, reporter=reporter)

        with open(warnings_log_file, "r") as f:
            warnings = f.readlines()

        with open(errors_log_file, "r") as f:
            errors = f.readlines()

    filtered_errors: list[str] = []
    for e in errors:
        if e.count("imported but unused") > 0:
            warnings.append(e)
        else:
            filtered_errors.append(e)

    if warnings and print_warnings:
        warnings_to_print = "".join(warnings)
        cerebrium_log(
            prefix="Warning: Found the following warnings in your files.",
            message=f"\n{warnings_to_print}",
            level="WARNING",
        )

    if filtered_errors:
        errors_to_print = "".join(filtered_errors)
        cerebrium_log(
            prefix="Error: Found the following syntax errors in your files:",
            message=f"{errors_to_print}"
            "Please fix the errors and try again. \nIf you would like to ignore these errors and deploy anyway, use the `--disable-syntax-check` flag.",
            level="ERROR",
        )
    return errors, warnings
