#!/usr/bin/env python3

import os
import argparse
from pathlib import Path
import logging

import chardet
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    Progress, SpinnerColumn, TextColumn, BarColumn,
    TaskProgressColumn, TimeRemainingColumn
)


class SourceCodeConverter:
    """
    A utility to convert source code files in a repository into a single text file, 
    respecting the .gitignore and excluding unnecessary files.
    """

    def __init__(self, max_file_size=100, log_level=logging.INFO):
        """
        Initialize the source code converter with configurable file size limits and logging.
        
        Args:
            max_file_size (int): Maximum size of files to process (in KB).
            log_level (int): Logging level (e.g., INFO, DEBUG).
        """
        logging.basicConfig(
            level=log_level,
            format="%(message)s",
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True)]
        )
        self.logger = logging.getLogger("SourceCodeConverter")
        self.max_file_size = max_file_size * 1024  # Convert KB to bytes
        self.exclude_dirs = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', 'dist', 'build'}
        self.gitignore_patterns = set()
        self.console = Console()

    def load_gitignore(self, repo_path):
        """
        Load .gitignore patterns from the repository if it exists.
        
        Args:
            repo_path (Path): Path to the repository's root.
        """
        gitignore_file = repo_path / ".gitignore"
        if gitignore_file.is_file():
            with open(gitignore_file, 'r') as f:
                for line in f:
                    stripped = line.strip()
                    if stripped and not stripped.startswith('#'):
                        self.gitignore_patterns.add(stripped)

    def is_ignored(self, file_path, repo_path):
        """
        Check if a file should be ignored based on .gitignore patterns.
        
        Args:
            file_path (Path): The full path to the file.
            repo_path (Path): The root path of the repository.

        Returns:
            bool: True if the file matches any .gitignore pattern, False otherwise.
        """
        rel_path = file_path.relative_to(repo_path)
        return any(rel_path.match(pattern) for pattern in self.gitignore_patterns)

    def is_text_file(self, file_path):
        """
        Determine if a file is a text file based on its content and size.
        
        Args:
            file_path (Path): The full path to the file.

        Returns:
            bool: True if the file is a text file, False otherwise.
        """
        try:
            if os.path.getsize(file_path) > self.max_file_size:
                return False
            with open(file_path, 'rb') as file:
                if b'\0' in file.read(1024):  # Check for null bytes in the first 1KB
                    return False
            return True
        except Exception as e:
            self.logger.warning(f"Error checking file {file_path}: {e}")
            return False

    def detect_encoding(self, file_path):
        """
        Detect the encoding of a file using the chardet library.
        
        Args:
            file_path (Path): The full path to the file.

        Returns:
            str: The detected encoding or 'utf-8' as a fallback.
        """
        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read(10000)  # Read the first 10KB of data
                result = chardet.detect(raw_data)
                return result['encoding'] or 'utf-8'
        except Exception:
            return 'utf-8'

    def read_source_file(self, file_path):
        """
        Read the contents of a source file with the appropriate encoding.
        
        Args:
            file_path (Path): The full path to the source file.

        Returns:
            str: The content of the file or an empty string on failure.
        """
        try:
            encoding = self.detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                return file.read()
        except Exception as e:
            self.logger.warning(f"Error reading {file_path}: {e}")
            return ""

    def convert_repository(self, repo_path, output_path):
        """
        Convert all eligible source files in the repository into a single output text file.
        
        Args:
            repo_path (Path): The root path of the repository to process.
            output_path (Path): The path to the output text file.
        """
        self.load_gitignore(repo_path)
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
            BarColumn(), TaskProgressColumn(), TimeRemainingColumn()
        ) as progress:
            overall_task = progress.add_task("[green]Processing Repository...", total=100)

            try:
                with open(output_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(f"# Repository: {repo_path}\n")
                    outfile.write("=" * 50 + "\n\n")

                    processed_files = 0
                    for root, dirs, files in os.walk(repo_path):
                        dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
                        for file in files:
                            file_path = Path(root) / file
                            if self.is_text_file(file_path) and not self.is_ignored(file_path, repo_path):
                                try:
                                    relative_path = file_path.relative_to(repo_path)
                                    outfile.write(f"### SOURCE FILE: {relative_path}\n")
                                    outfile.write("-" * 50 + "\n")
                                    content = self.read_source_file(file_path)
                                    outfile.write(content + "\n\n")
                                    processed_files += 1
                                except Exception as e:
                                    self.logger.error(f"Error processing {file_path}: {e}")
                    progress.update(overall_task, completed=100)

                self.console.print(f"[bold green]Conversion successful![/]")
                self.console.print(f"[bold]Processed Files:[/] {processed_files}")
                self.console.print(f"[bold]Output File:[/] {output_path}")
            except Exception as e:
                self.logger.error(f"Error during conversion: {e}")


def main():
    """
    CLI entry point for the source code converter.
    """
    parser = argparse.ArgumentParser(
        description="Source Code Converter with .gitignore support"
    )
    parser.add_argument('repo_path', type=Path, help='Path to the repository')
    parser.add_argument('--max-size', type=int, default=100, help='Maximum file size in KB')
    parser.add_argument('--output', type=Path, help='Custom output filename')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    output_file = args.output or Path(f"{args.repo_path.name}_output.txt")

    converter = SourceCodeConverter(max_file_size=args.max_size, log_level=log_level)
    converter.convert_repository(args.repo_path, output_file)


if __name__ == '__main__':
    main()
