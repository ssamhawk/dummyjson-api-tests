import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def ensure_dirs(dir_path: Path):
    """Create directory (with parents) if it does not exist."""
    dir_path.mkdir(parents=True, exist_ok=True)


def write_env_props(results_dir: Path):
    """Write Allure environment.properties with helpful metadata."""
    env_path = results_dir / "environment.properties"
    lines = [
        "PROJECT_NAME=DummyJSON API Tests",
        f"BASE_URL=https://dummyjson.com",
        f"PYTHON_VERSION={sys.version.split()[0]}",
        f"TEST_RUN_TIME={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Run pytest and build Allure report.")
    parser.add_argument("targets", nargs="*", help="Pytest targets (dir/file/test). Example: dummyjson/tests/api/test_products.py")
    parser.add_argument("--open", action="store_true", help="Open generated Allure report in browser")
    parser.add_argument("--clean", action="store_true", help="Clean previous allure results before run")
    args, pytest_args = parser.parse_known_args()

    # Project root
    project_root = Path(__file__).parent.parent
    now = datetime.now()
    date_part = now.strftime("%Y-%m-%d")
    time_part = now.strftime("%H-%M-%S")

    # Report directories
    report_dir = project_root / "allure-report" / date_part / time_part
    results_dir = project_root / "allure-results" / date_part / time_part

    if args.clean:
        shutil.rmtree(project_root / "allure-results", ignore_errors=True)
        shutil.rmtree(project_root / "allure-report", ignore_errors=True)

    ensure_dirs(results_dir)
    write_env_props(results_dir)

    # Build pytest command
    pytest_cmd = [
        "pytest",
        f"--alluredir={results_dir}",
        "-v",
        *args.targets,
        *pytest_args,
    ]

    print(f"Running pytest with Allure: {' '.join(pytest_cmd)}")
    result = subprocess.run(pytest_cmd, cwd=project_root)

    if result.returncode != 0:
        print(f"\nTests failed with exit code {result.returncode}")

    # Generate Allure report
    print(f"\nGenerating Allure report...")
    ensure_dirs(report_dir)
    allure_gen = subprocess.run(["allure", "generate", str(results_dir), "-o", str(report_dir), "--clean"], cwd=project_root)

    if allure_gen.returncode != 0:
        print(f"Failed to generate Allure report. Make sure 'allure' CLI is installed.")
        sys.exit(allure_gen.returncode)

    print(f"\nAllure report generated at: {report_dir}")

    # Open report if requested
    if args.open:
        print(f"Opening Allure report in browser...")
        subprocess.run(["allure", "open", str(report_dir)], cwd=project_root)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
