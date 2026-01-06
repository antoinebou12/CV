#!/usr/bin/env python3
"""
CV Build Script - Compile LaTeX CV using Docker

This script builds LaTeX CVs using Docker with support for multiple languages.
Uses Typer for CLI, Rich for beautiful terminal output, and tqdm for progress bars.
"""

import subprocess
import sys
import os
import re
import time
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

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


@dataclass
class LaTeXLogStats:
    """Statistics extracted from LaTeX log file."""
    errors: List[Dict[str, str]]
    warnings: List[Dict[str, str]]
    overfull_boxes: List[Dict[str, str]]
    underfull_boxes: List[Dict[str, str]]
    pages: int = 0
    has_fatal_error: bool = False


def parse_latex_log(log_path: Path) -> LaTeXLogStats:
    """
    Parse LaTeX log file to extract errors, warnings, and statistics.
    
    Args:
        log_path: Path to the .log file
        
    Returns:
        LaTeXLogStats object with parsed information
    """
    if not log_path.exists():
        return LaTeXLogStats([], [], [], [], 0, False)
    
    errors = []
    warnings = []
    overfull_boxes = []
    underfull_boxes = []
    pages = 0
    has_fatal_error = False
    
    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        # Patterns for different types of issues
        error_pattern = re.compile(r'^! (.+)$', re.MULTILINE)
        fatal_error_pattern = re.compile(r'^Fatal error occurred', re.MULTILINE | re.IGNORECASE)
        warning_pattern = re.compile(r'^LaTeX (Warning|Warning|Font Warning): (.+)$', re.MULTILINE)
        overfull_pattern = re.compile(r'Overfull \\hbox \(([\d.]+)pt too wide\) in (.+) at lines ([\d-]+)', re.MULTILINE)
        underfull_pattern = re.compile(r'Underfull \\hbox \(badness ([\d]+)\) in (.+) at lines ([\d-]+)', re.MULTILINE)
        pages_pattern = re.compile(r'Output written on .+ \((\d+) pages?\)', re.MULTILINE)
        
        # Find fatal errors
        if fatal_error_pattern.search(content):
            has_fatal_error = True
        
        # Find errors
        for match in error_pattern.finditer(content):
            error_line = match.start()
            # Get context around error
            start = max(0, error_line - 500)
            end = min(len(content), error_line + 500)
            context = content[start:end]
            # Extract line number if available
            line_match = re.search(r'l\.(\d+)', context)
            line_num = line_match.group(1) if line_match else "unknown"
            errors.append({
                'message': match.group(1),
                'line': line_num,
                'context': context[-200:] if len(context) > 200 else context
            })
        
        # Find warnings
        for match in warning_pattern.finditer(content):
            warnings.append({
                'type': match.group(1),
                'message': match.group(2),
                'line': 'unknown'
            })
        
        # Find overfull boxes
        for match in overfull_pattern.finditer(content):
            overfull_boxes.append({
                'width': match.group(1),
                'location': match.group(2),
                'lines': match.group(3)
            })
        
        # Find underfull boxes
        for match in underfull_pattern.finditer(content):
            underfull_boxes.append({
                'badness': match.group(1),
                'location': match.group(2),
                'lines': match.group(3)
            })
        
        # Find page count
        pages_match = pages_pattern.search(content)
        if pages_match:
            pages = int(pages_match.group(1))
        
    except Exception as e:
        if not CI_MODE:
            console.print(f"[yellow]Warning: Could not parse LaTeX log file: {e}[/yellow]")
    
    return LaTeXLogStats(
        errors=errors,
        warnings=warnings,
        overfull_boxes=overfull_boxes,
        underfull_boxes=underfull_boxes,
        pages=pages,
        has_fatal_error=has_fatal_error
    )

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


def check_latex_quality(
    lang: str,
    fail_on_warnings: bool = False,
    show_warnings: bool = False,
) -> Tuple[bool, LaTeXLogStats]:
    """
    Check LaTeX compilation quality by parsing the log file.
    
    Args:
        lang: Language code (en or fr)
        fail_on_warnings: If True, return False if warnings are found
        show_warnings: If True, always display warnings summary
        
    Returns:
        Tuple of (success: bool, stats: LaTeXLogStats)
    """
    cv_path = get_cv_path(lang)
    log_path = cv_path / "resume.log"
    
    stats = parse_latex_log(log_path)
    
    # Check for fatal errors
    if stats.has_fatal_error or stats.errors:
        return False, stats
    
    # Count total warnings (including overfull/underfull boxes)
    total_warnings = (
        len(stats.warnings) +
        len(stats.overfull_boxes) +
        len(stats.underfull_boxes)
    )
    
    # Show warnings if requested or if there are any
    if show_warnings or total_warnings > 0:
        if CI_MODE:
            if total_warnings > 0:
                print(f"\nLaTeX Compilation Quality Report for {lang.upper()}:")
                print(f"  Pages: {stats.pages}")
                if stats.errors:
                    print(f"  Errors: {len(stats.errors)}")
                    for err in stats.errors[:5]:  # Show first 5 errors
                        print(f"    - Line {err['line']}: {err['message'][:80]}")
                if stats.warnings:
                    print(f"  Warnings: {len(stats.warnings)}")
                if stats.overfull_boxes:
                    print(f"  Overfull boxes: {len(stats.overfull_boxes)}")
                    for box in stats.overfull_boxes[:3]:  # Show first 3
                        print(f"    - {box['width']}pt too wide at lines {box['lines']}")
                if stats.underfull_boxes:
                    print(f"  Underfull boxes: {len(stats.underfull_boxes)}")
        else:
            if total_warnings > 0:
                table = Table(title=f"LaTeX Quality Report ({lang.upper()})", show_header=True)
                table.add_column("Metric", style="cyan")
                table.add_column("Count", style="yellow")
                table.add_row("Pages", str(stats.pages))
                if stats.errors:
                    table.add_row("Errors", f"[red]{len(stats.errors)}[/red]")
                if stats.warnings:
                    table.add_row("Warnings", f"[yellow]{len(stats.warnings)}[/yellow]")
                if stats.overfull_boxes:
                    table.add_row("Overfull boxes", f"[yellow]{len(stats.overfull_boxes)}[/yellow]")
                if stats.underfull_boxes:
                    table.add_row("Underfull boxes", f"[yellow]{len(stats.underfull_boxes)}[/yellow]")
                console.print(table)
                
                # Show details for overfull boxes
                if stats.overfull_boxes and verbose:
                    console.print("\n[dim]Overfull boxes:[/dim]")
                    for box in stats.overfull_boxes[:5]:
                        console.print(f"[dim]  - {box['width']}pt too wide at lines {box['lines']} in {box['location']}[/dim]")
    
    # Fail if warnings are found and fail_on_warnings is True
    if fail_on_warnings and total_warnings > 0:
        return False, stats
    
    return True, stats


def compile_cv(
    lang: str,
    output: Optional[str] = None,
    verbose: bool = False,
    fail_on_warnings: bool = False,
    show_warnings: bool = False,
) -> Tuple[bool, Optional[LaTeXLogStats]]:
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
                    return False, None
                
                # Check LaTeX quality
                quality_ok, stats = check_latex_quality(lang, fail_on_warnings, show_warnings)
                if not quality_ok:
                    if fail_on_warnings:
                        log(f"LaTeX quality check failed for {lang}", "fail")
                        return False, stats
                    else:
                        log(f"LaTeX compilation completed with warnings for {lang}", "warn")
                
                # Move to desired output location if different
                if output and output_path != pdf_path:
                    import shutil
                    shutil.move(str(pdf_path), str(output_path))
                    log(f"PDF created at {output_path} ({pdf_size} bytes)", "ok")
                else:
                    log(f"PDF created at {pdf_path} ({pdf_size} bytes)", "ok")
                return True, stats
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
                # Try to get stats from log file even if PDF is missing
                _, stats = check_latex_quality(lang, False, verbose)
                return False, stats
        else:
            log(f"Compilation failed (exit code: {result.returncode})", "fail")
            # Try to parse log file for better error messages
            _, stats = check_latex_quality(lang, False, verbose)
            if stats.errors:
                if CI_MODE:
                    print("\nLaTeX Errors found:")
                    for err in stats.errors[:3]:
                        print(f"  Line {err['line']}: {err['message'][:100]}")
                else:
                    error_table = Table(title="LaTeX Errors", show_header=True, header_style="bold red")
                    error_table.add_column("Line", style="cyan")
                    error_table.add_column("Error", style="red")
                    for err in stats.errors[:5]:
                        error_table.add_row(err['line'], err['message'][:100])
                    console.print(error_table)
            
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
            return False, stats
    except subprocess.TimeoutExpired:
        log("Compilation timed out after 10 minutes", "fail")
        return False, None
    except Exception as e:
        log(f"Error during compilation: {e}", "error")
        if verbose:
            import traceback
            if CI_MODE:
                print("Traceback:")
                print(traceback.format_exc())
            else:
                console.print(Panel(traceback.format_exc(), title="Traceback", border_style="red"))
        return False, None


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
    fail_on_warnings: bool = False,
    show_warnings: bool = False,
) -> Tuple[bool, Optional[LaTeXLogStats]]:
    """Build a single CV for the specified language."""
    # Validate language
    if language not in ["en", "fr"]:
        log(f"Invalid language: {language}. Must be 'en' or 'fr'", "error")
        return False, None

    # Validate CV directory exists
    cv_path = get_cv_path(language)
    if not cv_path.exists():
        log(f"CV directory not found: {cv_path}", "error")
        return False, None

    if not (cv_path / "resume.tex").exists():
        log(f"resume.tex not found in {cv_path}", "error")
        return False, None

    # Build Docker image
    if not build_image(language, rebuild, verbose):
        log(f"Failed to build Docker image for {language}", "fail")
        return False, None

    # Compile CV
    if move_to_root:
        lang_output = f"cv-{language}.pdf"
    elif not output:
        lang_output = str(cv_path / "resume.pdf")
    else:
        # If output is specified for --all, append language suffix
        lang_output = output.replace(".pdf", f"-{language}.pdf")

    success, stats = compile_cv(language, lang_output, verbose, fail_on_warnings, show_warnings)
    if not success:
        log(f"Failed to compile CV for {language}", "fail")
        return False, stats

    # Cleanup if requested
    if clean:
        cleanup(language)

    return True, stats


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
    fail_on_warnings: bool = typer.Option(
        False,
        "--fail-on-warnings",
        help="Fail build if LaTeX warnings are detected",
    ),
    show_warnings: bool = typer.Option(
        False,
        "--show-warnings",
        help="Always show LaTeX warnings summary",
    ),
    parallel: bool = typer.Option(
        False,
        "--parallel",
        help="Build both languages in parallel when using --all",
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
        stats_dict = {}
        start_time = time.time()
        
        if parallel:
            # Parallel build
            if not CI_MODE:
                console.print("[cyan]Building both CVs in parallel...[/cyan]")
            else:
                print("Building both CVs in parallel...")
            
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = {
                    executor.submit(
                        build_single_cv,
                        lang, output, rebuild, clean, verbose, move_to_root,
                        fail_on_warnings, show_warnings
                    ): lang
                    for lang in ["en", "fr"]
                }
                
                for future in as_completed(futures):
                    lang = futures[future]
                    try:
                        success, stats = future.result()
                        results[lang] = success
                        stats_dict[lang] = stats
                        if not CI_MODE:
                            status = "[green]OK[/green]" if success else "[red]FAIL[/red]"
                            console.print(f"{lang.upper()}: {status}")
                    except Exception as e:
                        results[lang] = False
                        stats_dict[lang] = None
                        log(f"Error building {lang}: {e}", "error")
        else:
            # Sequential build
            for lang in ["en", "fr"]:
                if not CI_MODE:
                    console.print(Panel(f"[bold]Building {lang.upper()} CV[/bold]", border_style="blue"))
                else:
                    print(f"Building {lang.upper()} CV")
                success, stats = build_single_cv(lang, output, rebuild, clean, verbose, move_to_root, fail_on_warnings, show_warnings)
                results[lang] = success
                stats_dict[lang] = stats
                if not CI_MODE:
                    console.print()
        
        build_time = time.time() - start_time

        # Summary with statistics
        if not CI_MODE:
            console.print()
            summary_table = Table(title="Build Summary", show_header=True, header_style="bold magenta")
            summary_table.add_column("Language", style="cyan")
            summary_table.add_column("Status", style="green")
            summary_table.add_column("Pages", style="yellow")
            summary_table.add_column("Warnings", style="yellow")
            summary_table.add_column("Output", style="yellow")
            
            for lang in ["en", "fr"]:
                cv_path = get_cv_path(lang)
                if move_to_root:
                    output_path = f"cv-{lang}.pdf"
                else:
                    output_path = str(cv_path / "resume.pdf")
                
                stats = stats_dict.get(lang)
                if results[lang]:
                    pages = str(stats.pages) if stats else "?"
                    warnings = (
                        len(stats.warnings) + len(stats.overfull_boxes) + len(stats.underfull_boxes)
                        if stats else 0
                    )
                    warning_str = f"[yellow]{warnings}[/yellow]" if warnings > 0 else "0"
                    summary_table.add_row(lang.upper(), "[green]OK[/green]", pages, warning_str, output_path)
                else:
                    summary_table.add_row(lang.upper(), "[red]FAIL[/red]", "N/A", "N/A", "N/A")
            
            console.print(summary_table)
            console.print(f"[dim]Total build time: {build_time:.2f}s[/dim]")
            console.print()
        else:
            print("\nBuild Summary:")
            for lang in ["en", "fr"]:
                cv_path = get_cv_path(lang)
                if move_to_root:
                    output_path = f"cv-{lang}.pdf"
                else:
                    output_path = str(cv_path / "resume.pdf")
                
                stats = stats_dict.get(lang)
                status = "OK" if results[lang] else "FAIL"
                pages = stats.pages if stats else 0
                warnings = (
                    len(stats.warnings) + len(stats.overfull_boxes) + len(stats.underfull_boxes)
                    if stats else 0
                )
                print(f"  {lang.upper()}: {status} - {output_path} (Pages: {pages}, Warnings: {warnings})")
            print(f"Total build time: {build_time:.2f}s")
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
    start_time = time.time()
    success, stats = build_single_cv(language, output, rebuild, clean, verbose, move_to_root, fail_on_warnings, show_warnings)
    build_time = time.time() - start_time
    
    if not success:
        raise typer.Exit(1)
    
    # Show build statistics
    if stats:
        if not CI_MODE:
            stats_table = Table(title="Build Statistics", show_header=True, header_style="bold magenta")
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="green")
            stats_table.add_row("Pages", str(stats.pages))
            total_warnings = len(stats.warnings) + len(stats.overfull_boxes) + len(stats.underfull_boxes)
            stats_table.add_row("Warnings", f"[yellow]{total_warnings}[/yellow]" if total_warnings > 0 else "0")
            stats_table.add_row("Build Time", f"{build_time:.2f}s")
            console.print()
            console.print(stats_table)
        else:
            print(f"\nBuild Statistics:")
            print(f"  Pages: {stats.pages}")
            total_warnings = len(stats.warnings) + len(stats.overfull_boxes) + len(stats.underfull_boxes)
            print(f"  Warnings: {total_warnings}")
            print(f"  Build Time: {build_time:.2f}s")

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
