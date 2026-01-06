#!/usr/bin/env python3
"""
CV Build Script - Compile LaTeX CV using Docker

This script builds LaTeX CVs using Docker with support for multiple languages.
Uses Typer for CLI, Rich for beautiful terminal output, and tqdm for progress bars.
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.status import Status
from rich.table import Table
from tqdm import tqdm

# Global CI mode flag
CI_MODE = False

# Initialize Rich console with Windows-safe encoding
console = Console(force_terminal=True, legacy_windows=False)

# Initialize Typer app
app = typer.Typer(
    name="build-cv",
    help="Build LaTeX CV using Docker with language support",
    add_completion=False,
)


def log(message: str, level: str = "info") -> None:
    """Log a message, using plain text in CI mode or Rich formatting otherwise."""
    global CI_MODE
    if CI_MODE:
        # Plain text output for CI
        prefix = {
            "info": "",
            "ok": "✓ ",
            "error": "ERROR: ",
            "fail": "FAIL: ",
            "warn": "WARNING: ",
        }.get(level, "")
        print(f"{prefix}{message}")
    else:
        # Rich formatting for interactive use
        colors = {
            "info": "",
            "ok": "[green]OK[/green]",
            "error": "[red]ERROR[/red]",
            "fail": "[red]FAIL[/red]",
            "warn": "[yellow]WARNING[/yellow]",
        }
        if level == "info":
            console.print(message)
        else:
            console.print(f"{colors.get(level, '')} {message}")


def check_docker() -> bool:
    """Check if Docker is installed and running."""
    try:
        # Check if docker command exists
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        # Check if Docker daemon is running (don't fail on warnings)
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            check=False,  # Don't fail on warnings
            timeout=10,
        )
        # If we got any output, Docker is working
        return result.returncode == 0 or "Client:" in result.stdout or "Server:" in result.stdout
    except FileNotFoundError:
        return False
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def get_cv_path(lang: str) -> Path:
    """Get the CV directory path for the given language."""
    return Path(f"cv-{lang}")


def build_image(lang: str, rebuild: bool = False, verbose: bool = False) -> bool:
    """Build Docker image for the specified language."""
    global CI_MODE
    image_tag = f"cv-builder-{lang}"
    cv_path = get_cv_path(lang)

    # Verify Dockerfile exists
    dockerfile = Path("Dockerfile.cv")
    if not dockerfile.exists():
        log(f"Dockerfile.cv not found in current directory", "error")
        return False

    # Verify CV directory exists before building
    if not cv_path.exists():
        log(f"CV directory not found: {cv_path}", "error")
        return False

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
                log(f"Docker image {image_tag} already exists", "ok")
                return True
        except subprocess.CalledProcessError:
            pass

    # Build the image
    if CI_MODE:
        log(f"Building Docker image for {lang}...", "info")
    else:
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
        if CI_MODE:
            # Plain output for CI
            result = subprocess.run(
                build_cmd,
                capture_output=not verbose,  # Show output in verbose mode
                text=True,
                check=False,
                timeout=1800,  # 30 minute timeout for Docker build
            )
        else:
            # Use Rich status for build progress
            with Status(f"Building {image_tag}...", console=console):
                result = subprocess.run(
                    build_cmd,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=1800,  # 30 minute timeout for Docker build
                )

        if result.returncode == 0:
            log(f"Successfully built {image_tag}", "ok")
            if verbose and not CI_MODE:
                # Show last few lines of build output
                output_lines = result.stdout.split('\n')
                if len(output_lines) > 10:
                    console.print("[dim]Last 10 lines of build output:[/dim]")
                    for line in output_lines[-10:]:
                        if line.strip():
                            console.print(f"[dim]  {line}[/dim]")
            return True
        else:
            log(f"Failed to build {image_tag} (exit code: {result.returncode})", "fail")
            if verbose:
                error_output = result.stderr if result.stderr else result.stdout
                if error_output:
                    if CI_MODE:
                        print("Build Error:")
                        print(error_output)
                    else:
                        console.print(Panel(error_output, title="Build Error", border_style="red"))
                else:
                    if not CI_MODE:
                        console.print("[dim]No error output available[/dim]")
            return False
    except subprocess.TimeoutExpired:
        log("Docker build timed out after 30 minutes", "fail")
        return False
    except Exception as e:
        log(f"Error building image: {e}", "error")
        if verbose:
            import traceback
            if CI_MODE:
                print("Traceback:")
                print(traceback.format_exc())
            else:
                console.print(Panel(traceback.format_exc(), title="Traceback", border_style="red"))
        return False


def compile_cv(
    lang: str,
    output: Optional[str] = None,
    verbose: bool = False,
) -> bool:
    """Compile the CV using Docker container."""
    global CI_MODE
    image_tag = f"cv-builder-{lang}"
    cv_path = get_cv_path(lang)
    output_path = Path(output) if output else cv_path / "resume.pdf"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Run the container
    if CI_MODE:
        log(f"Compiling CV for {lang}...", "info")
    else:
        console.print(f"[yellow]Compiling CV for {lang}...[/yellow]")

    # Use volume mount to get the PDF out
    # Handle Windows vs Unix paths
    cv_abs_path = cv_path.absolute()
    if sys.platform == "win32":
        # Windows: convert to Docker-friendly path
        volume_mount = f"{cv_abs_path}:/cv/output"
    else:
        # Unix: use as-is
        volume_mount = f"{cv_abs_path}:/cv/output"

    run_cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        volume_mount,
        image_tag,
    ]

    try:
        if CI_MODE:
            result = subprocess.run(
                run_cmd,
                capture_output=not verbose,  # Show output in verbose mode
                text=True,
                check=False,
                timeout=600,  # 10 minute timeout
            )
        else:
            with Status(f"Running compilation...", console=console):
                result = subprocess.run(
                    run_cmd,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=600,  # 10 minute timeout
                )

        if result.returncode == 0:
            # Check if PDF was created
            pdf_path = cv_path / "resume.pdf"
            if pdf_path.exists():
                # Verify PDF is not empty
                pdf_size = pdf_path.stat().st_size
                if pdf_size == 0:
                    log(f"PDF created but is empty at {pdf_path}", "fail")
                    return False
                
                # Move to desired output location if different
                if output and output_path != pdf_path:
                    import shutil
                    shutil.move(str(pdf_path), str(output_path))
                    log(f"PDF created at {output_path} ({pdf_size} bytes)", "ok")
                else:
                    log(f"PDF created at {pdf_path} ({pdf_size} bytes)", "ok")
                return True
            else:
                log(f"Compilation succeeded but PDF not found at {pdf_path}", "fail")
                if verbose:
                    if CI_MODE:
                        print("Checking directory contents:")
                        for f in cv_path.iterdir():
                            print(f"  - {f.name}")
                    else:
                        console.print(f"[dim]Checking directory contents:[/dim]")
                        for f in cv_path.iterdir():
                            console.print(f"[dim]  - {f.name}[/dim]")
                return False
        else:
            log(f"Compilation failed (exit code: {result.returncode})", "fail")
            if verbose or result.returncode != 0:
                error_output = result.stderr if result.stderr else result.stdout
                if error_output:
                    if CI_MODE:
                        print("Error Output:")
                        print(error_output)
                    else:
                        console.print(Panel(error_output, title="Error Output", border_style="red"))
                else:
                    if not CI_MODE:
                        console.print("[dim]No error output available[/dim]")
            return False
    except subprocess.TimeoutExpired:
        log("Compilation timed out after 10 minutes", "fail")
        return False
    except Exception as e:
        log(f"Error during compilation: {e}", "error")
        if verbose:
            import traceback
            if CI_MODE:
                print("Traceback:")
                print(traceback.format_exc())
            else:
                console.print(Panel(traceback.format_exc(), title="Traceback", border_style="red"))
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
        log(f"Cleaned {len(cleaned)} auxiliary files", "ok")
    else:
        if not CI_MODE:
            console.print("[dim]No auxiliary files to clean[/dim]")


def build_single_cv(
    language: str,
    output: Optional[str],
    rebuild: bool,
    clean: bool,
    verbose: bool,
    move_to_root: bool,
) -> bool:
    """Build a single CV for the specified language."""
    # Validate language
    if language not in ["en", "fr"]:
        log(f"Invalid language: {language}. Must be 'en' or 'fr'", "error")
        return False

    # Validate CV directory exists
    cv_path = get_cv_path(language)
    if not cv_path.exists():
        log(f"CV directory not found: {cv_path}", "error")
        return False

    if not (cv_path / "resume.tex").exists():
        log(f"resume.tex not found in {cv_path}", "error")
        return False

    # Build Docker image
    if not build_image(language, rebuild, verbose):
        log(f"Failed to build Docker image for {language}", "fail")
        return False

    # Compile CV
    if move_to_root:
        lang_output = f"cv-{language}.pdf"
    elif not output:
        lang_output = str(cv_path / "resume.pdf")
    else:
        # If output is specified for --all, append language suffix
        lang_output = output.replace(".pdf", f"-{language}.pdf")

    if not compile_cv(language, lang_output, verbose):
        log(f"Failed to compile CV for {language}", "fail")
        return False

    # Cleanup if requested
    if clean:
        cleanup(language)

    return True


@app.command()
def build(
    language: str = typer.Option(
        "en",
        "--language",
        "-l",
        help="Language to build (en or fr). Use --all to build both.",
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
    all_languages: bool = typer.Option(
        False,
        "--all",
        help="Build both English and French CVs",
    ),
    ci: bool = typer.Option(
        False,
        "--ci",
        help="CI/Pipeline mode: plain text output, no Rich formatting",
    ),
):
    """Build LaTeX CV using Docker."""
    global CI_MODE
    CI_MODE = ci
    # If --all is specified, build both languages
    if all_languages:
        if not CI_MODE:
            console.print()
            console.print(Panel("[bold cyan]Building both English and French CVs[/bold cyan]", border_style="cyan"))
            console.print()
            
            # Display build information
            table = Table(title="Build Configuration", show_header=True, header_style="bold magenta")
            table.add_column("Setting", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Languages", "en, fr")
            table.add_row("Rebuild Image", "Yes" if rebuild else "No")
            table.add_row("Clean Aux Files", "Yes" if clean else "No")
            console.print(table)
            console.print()
        else:
            print("Building both English and French CVs")
            print(f"Languages: en, fr")
            print(f"Rebuild Image: {'Yes' if rebuild else 'No'}")
            print(f"Clean Aux Files: {'Yes' if clean else 'No'}")
            print()

        # Check Docker
        if CI_MODE:
            if not check_docker():
                log("Docker is not installed or not running. Please install Docker and ensure it's running.", "fail")
                raise typer.Exit(1)
            log("Docker is available", "ok")
            print()
        else:
            with Status("Checking Docker...", console=console):
                if not check_docker():
                    console.print(
                        "[red]FAIL[/red] Docker is not installed or not running. Please install Docker and ensure it's running."
                    )
                    raise typer.Exit(1)
            console.print("[green]OK[/green] Docker is available")
            console.print()

        # Build both languages
        results = {}
        for lang in ["en", "fr"]:
            if not CI_MODE:
                console.print(Panel(f"[bold]Building {lang.upper()} CV[/bold]", border_style="blue"))
            else:
                print(f"Building {lang.upper()} CV")
            success = build_single_cv(lang, output, rebuild, clean, verbose, move_to_root)
            results[lang] = success
            if not CI_MODE:
                console.print()

        # Summary
        if not CI_MODE:
            console.print()
            summary_table = Table(title="Build Summary", show_header=True, header_style="bold magenta")
            summary_table.add_column("Language", style="cyan")
            summary_table.add_column("Status", style="green")
            summary_table.add_column("Output", style="yellow")
            
            for lang in ["en", "fr"]:
                cv_path = get_cv_path(lang)
                if move_to_root:
                    output_path = f"cv-{lang}.pdf"
                else:
                    output_path = str(cv_path / "resume.pdf")
                
                if results[lang]:
                    summary_table.add_row(lang.upper(), "[green]OK[/green]", output_path)
                else:
                    summary_table.add_row(lang.upper(), "[red]FAIL[/red]", "N/A")
            
            console.print(summary_table)
            console.print()
        else:
            print("\nBuild Summary:")
            for lang in ["en", "fr"]:
                cv_path = get_cv_path(lang)
                if move_to_root:
                    output_path = f"cv-{lang}.pdf"
                else:
                    output_path = str(cv_path / "resume.pdf")
                
                status = "OK" if results[lang] else "FAIL"
                print(f"  {lang.upper()}: {status} - {output_path}")
            print()

        # Final status
        if all(results.values()):
            if CI_MODE:
                log("Both CVs compiled successfully!", "ok")
            else:
                console.print(
                    Panel(
                        "[green]OK Both CVs compiled successfully![/green]",
                        title="Success",
                        border_style="green",
                    )
                )
        else:
            failed = [lang for lang, success in results.items() if not success]
            if CI_MODE:
                log(f"Failed to build: {', '.join(failed).upper()}", "fail")
            else:
                console.print(
                    Panel(
                        f"[red]FAIL[/red] Failed to build: {', '.join(failed).upper()}",
                        title="Error",
                        border_style="red",
                    )
                )
            raise typer.Exit(1)
        
        return

    # Single language build (original logic)
    # Validate language
    if language not in ["en", "fr"]:
        log(f"Invalid language: {language}. Must be 'en' or 'fr'", "error")
        raise typer.Exit(1)

    # Display build information
    if not CI_MODE:
        table = Table(title="Build Configuration", show_header=True, header_style="bold magenta")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Language", language)
        table.add_row("CV Path", str(get_cv_path(language)))
        table.add_row("Rebuild Image", "Yes" if rebuild else "No")
        table.add_row("Clean Aux Files", "Yes" if clean else "No")
        console.print(table)
        console.print()
    else:
        print("Build Configuration:")
        print(f"  Language: {language}")
        print(f"  CV Path: {get_cv_path(language)}")
        print(f"  Rebuild Image: {'Yes' if rebuild else 'No'}")
        print(f"  Clean Aux Files: {'Yes' if clean else 'No'}")
        print()

    # Check Docker
    if CI_MODE:
        if not check_docker():
            log("Docker is not installed or not running. Please install Docker and ensure it's running.", "fail")
            raise typer.Exit(1)
        log("Docker is available", "ok")
    else:
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
        log(f"CV directory not found: {cv_path}", "error")
        raise typer.Exit(1)

    if not (cv_path / "resume.tex").exists():
        log(f"resume.tex not found in {cv_path}", "error")
        raise typer.Exit(1)

    # Use the single CV build function
    if not build_single_cv(language, output, rebuild, clean, verbose, move_to_root):
        raise typer.Exit(1)

    # Success message
    cv_path = get_cv_path(language)
    if move_to_root:
        final_output = f"cv-{language}.pdf"
    elif not output:
        final_output = str(cv_path / "resume.pdf")
    else:
        final_output = output

    if CI_MODE:
        log(f"CV compiled successfully! Language: {language}, Output: {final_output}", "ok")
    else:
        console.print()
        console.print(
            Panel(
                f"[green]OK CV compiled successfully![/green]\n\n"
                f"Language: {language}\n"
                f"Output: {final_output}",
                title="Success",
                border_style="green",
            )
        )


if __name__ == "__main__":
    app()
