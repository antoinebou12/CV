#!/usr/bin/env python3
"""
CV Build Script - Compile LaTeX CV using Docker

This script builds LaTeX CVs using Docker with support for multiple languages.
Uses Typer for CLI, Rich for beautiful terminal output, and tqdm for progress bars.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.status import Status
from rich.table import Table
from tqdm import tqdm

# Initialize Rich console with Windows-safe encoding
console = Console(force_terminal=True, legacy_windows=False)

# Initialize Typer app
app = typer.Typer(
    name="build-cv",
    help="Build LaTeX CV using Docker with language support",
    add_completion=False,
)


def check_docker() -> bool:
    """Check if Docker is installed and running."""
    try:
        # Check if docker command exists
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        # Check if Docker daemon is running (don't fail on warnings)
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            check=False,  # Don't fail on warnings
        )
        # If we got any output, Docker is working
        return result.returncode == 0 or "Client:" in result.stdout or "Server:" in result.stdout
    except FileNotFoundError:
        return False
    except Exception:
        return False


def get_cv_path(lang: str) -> Path:
    """Get the CV directory path for the given language."""
    return Path(f"cv-{lang}")


def build_image(lang: str, rebuild: bool = False, verbose: bool = False) -> bool:
    """Build Docker image for the specified language."""
    image_tag = f"cv-builder-{lang}"
    cv_path = get_cv_path(lang)

    # Check if image exists
    if not rebuild:
        try:
            result = subprocess.run(
                ["docker", "images", "-q", image_tag],
                capture_output=True,
                text=True,
                check=True,
            )
            if result.stdout.strip():
                console.print(f"[green]OK[/green] Docker image {image_tag} already exists")
                return True
        except subprocess.CalledProcessError:
            pass

    # Build the image
    console.print(f"[yellow]Building Docker image for {lang}...[/yellow]")
    build_cmd = [
        "docker",
        "build",
        "--build-arg",
        f"LANG={lang}",
        "-f",
        "Dockerfile.cv",
        "-t",
        image_tag,
        ".",
    ]

    try:
        # Use Rich status for build progress
        with Status(f"Building {image_tag}...", console=console):
            result = subprocess.run(
                build_cmd,
                capture_output=True,
                text=True,
                check=False,
            )

        if result.returncode == 0:
            console.print(f"[green]OK[/green] Successfully built {image_tag}")
            return True
        else:
            console.print(f"[red]FAIL[/red] Failed to build {image_tag}")
            if verbose:
                console.print(Panel(result.stderr, title="Build Error", border_style="red"))
            return False
    except Exception as e:
        console.print(f"[red]ERROR[/red] Error building image: {e}")
        return False


def compile_cv(
    lang: str,
    output: Optional[str] = None,
    verbose: bool = False,
) -> bool:
    """Compile the CV using Docker container."""
    image_tag = f"cv-builder-{lang}"
    cv_path = get_cv_path(lang)
    output_path = Path(output) if output else cv_path / "resume.pdf"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Run the container
    console.print(f"[yellow]Compiling CV for {lang}...[/yellow]")

    # Use volume mount to get the PDF out
    run_cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{cv_path.absolute()}:/cv/output",
        image_tag,
    ]

    try:
        with Status(f"Running compilation...", console=console):
            result = subprocess.run(
                run_cmd,
                capture_output=True,
                text=True,
                check=False,
            )

        if result.returncode == 0:
            # Check if PDF was created
            pdf_path = cv_path / "resume.pdf"
            if pdf_path.exists():
                # Move to desired output location if different
                if output and output_path != pdf_path:
                    import shutil

                    shutil.move(str(pdf_path), str(output_path))
                    console.print(f"[green]OK[/green] PDF created at {output_path}")
                else:
                    console.print(f"[green]OK[/green] PDF created at {pdf_path}")
                return True
            else:
                console.print(
                    f"[red]FAIL[/red] Compilation succeeded but PDF not found at {pdf_path}"
                )
                return False
        else:
            console.print(f"[red]FAIL[/red] Compilation failed")
            if verbose:
                console.print(Panel(result.stderr, title="Error Output", border_style="red"))
            return False
    except Exception as e:
        console.print(f"[red]ERROR[/red] Error during compilation: {e}")
        return False


def cleanup(lang: str) -> None:
    """Clean up auxiliary LaTeX files."""
    cv_path = get_cv_path(lang)
    aux_extensions = [".aux", ".log", ".out", ".bbl", ".blg", ".fdb_latexmk", ".fls"]

    cleaned = []
    for ext in aux_extensions:
        for file in cv_path.glob(f"*{ext}"):
            file.unlink()
            cleaned.append(file.name)

    if cleaned:
        console.print(f"[green]OK[/green] Cleaned {len(cleaned)} auxiliary files")
    else:
        console.print("[dim]No auxiliary files to clean[/dim]")


@app.command()
def build(
    language: str = typer.Option(
        "en",
        "--language",
        "-l",
        help="Language to build (en or fr)",
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Custom output path for PDF",
    ),
    rebuild: bool = typer.Option(
        False,
        "--rebuild",
        help="Force rebuild Docker image",
    ),
    clean: bool = typer.Option(
        False,
        "--clean",
        help="Clean auxiliary files after compilation",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Verbose output",
    ),
    move_to_root: bool = typer.Option(
        False,
        "--move-to-root",
        help="Move PDF to root as cv-{lang}.pdf",
    ),
):
    """Build LaTeX CV using Docker."""
    # Validate language
    if language not in ["en", "fr"]:
        console.print(f"[red]ERROR[/red] Invalid language: {language}. Must be 'en' or 'fr'")
        raise typer.Exit(1)

    # Display build information
    table = Table(title="Build Configuration", show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Language", language)
    table.add_row("CV Path", str(get_cv_path(language)))
    table.add_row("Rebuild Image", "Yes" if rebuild else "No")
    table.add_row("Clean Aux Files", "Yes" if clean else "No")
    console.print(table)
    console.print()

    # Check Docker
    with Status("Checking Docker...", console=console):
        if not check_docker():
            console.print(
                "[red]FAIL[/red] Docker is not installed or not running. Please install Docker and ensure it's running."
            )
            raise typer.Exit(1)
    console.print("[green]OK[/green] Docker is available")

    # Validate CV directory exists
    cv_path = get_cv_path(language)
    if not cv_path.exists():
        console.print(f"[red]ERROR[/red] CV directory not found: {cv_path}")
        raise typer.Exit(1)

    if not (cv_path / "resume.tex").exists():
        console.print(f"[red]ERROR[/red] resume.tex not found in {cv_path}")
        raise typer.Exit(1)

    # Build Docker image
    if not build_image(language, rebuild, verbose):
        console.print("[red]FAIL[/red] Failed to build Docker image")
        raise typer.Exit(1)

    # Compile CV
    if move_to_root:
        output = f"cv-{language}.pdf"
    elif not output:
        output = str(cv_path / "resume.pdf")

    if not compile_cv(language, output, verbose):
        console.print("[red]FAIL[/red] Failed to compile CV")
        raise typer.Exit(1)

    # Cleanup if requested
    if clean:
        cleanup(language)

    # Success message
    console.print()
    console.print(
        Panel(
            f"[green]OK CV compiled successfully![/green]\n\n"
            f"Language: {language}\n"
            f"Output: {output}",
            title="Success",
            border_style="green",
        )
    )


if __name__ == "__main__":
    app()
