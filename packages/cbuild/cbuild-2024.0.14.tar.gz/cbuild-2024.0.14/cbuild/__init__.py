"""

# CBUILD

### An Easy To Use CLI Build Tool For C

This software was made to be made better.
Use it how you like, add to it, or remove from it.
Distribute it as you please, and feel free to delete this notice!

~ d34d0s :)
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, BarColumn, SpinnerColumn
import os
import argparse
import configparser
import platform
import shutil

console = Console()

version = {
    "year": 2024,
    "minor": 0,
    "patch": 14
}

def run_command(command):
    result = os.system(command)
    if result != 0:
        print(f"Command failed with exit code {result}")
        exit(result)

def parse_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return {
        'compiler': config['CBUILD'].get('compiler', 'gcc'),
        'source_dir': config['CBUILD'].get('source_dir', ''),
        'sources': config['CBUILD'].get('sources', '').split(','),
        'defines': config['CBUILD'].get('defines', '').split(','),
        'output_type': config['CBUILD'].get('output_type', 'exe'),
        'output_dir': config['CBUILD'].get('output_dir', 'build/'),
        'libraries': config['CBUILD'].get('libraries', '').split(','),
        'source_dirs': config['CBUILD'].get('source_dirs', '').split(','),
        'project_name': config['CBUILD'].get('project_name', 'MyProject'),
        'include_dirs': config['CBUILD'].get('include_dirs', '').split(','),
        'library_dirs': config['CBUILD'].get('library_dirs', '').split(',')
    }

def collect_source_files(source_dir):
    source_files = []
    for root, _, files in os.walk(source_dir.strip()):
        for file in files:
            if file.endswith('.c'):
                source_files.append(os.path.join(root, file))
    return source_files

def build_command(compiler, output_type, object_files_str, output_dir, project_name, link_flags, library_flags):
    if output_type == 'exe':
        return f"{compiler} {object_files_str} {library_flags} {link_flags} -o {output_dir}/{project_name}.exe"
    elif output_type == 'dll':
        return f"{compiler} -shared {object_files_str} {library_flags} {link_flags} -o {output_dir}/{project_name}.dll"
    elif output_type == 'static_lib':
        return f"ar rcs {output_dir}/{project_name}.a {object_files_str}"
    elif output_type in ['html', 'js', 'wasm']:
        return f"{compiler} {object_files_str} {library_flags} {link_flags} -o {output_dir}/{project_name}.{output_type}"
    else:
        raise ValueError(f"Unsupported output type: {output_type}")

def clean_intermediate_files(object_files):
    for file in object_files:
        try:
            os.remove(file)
        except OSError as e:
            print(f"Error deleting {file}: {e}")

def build_project(config):
    project_name = config['project_name']
    compiler = config['compiler']
    sources = config['sources']
    defines = config['defines']
    libraries = config['libraries']
    source_dir = config['source_dir']
    output_dir = config['output_dir']
    source_dirs = config['source_dirs']
    output_type = config['output_type']
    include_dirs = config['include_dirs']
    library_dirs = config['library_dirs']

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if source_dir:
        sources += collect_source_files(source_dir)
    
    if source_dirs:
        for d in source_dirs:
            sources += collect_source_files(d)

    console.print(Panel(f"[bold green]CBUILD[/] {version['year']}.{version['minor']}.{version['patch']}", expand=False))
    
    table = Table(title=f"Project Build Summary: {project_name}", show_lines=True)
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_row("Compiler", compiler)
    table.add_row("Target Directory", output_dir)
    table.add_row("Output Type", output_type)
    table.add_row("Source Files", f"{len(sources)} {"files" if len(sources) > 1 else "file"}")
    
    console.print(table)

    object_files = []
    with Progress(SpinnerColumn(), "[progress.description]{task.description}", BarColumn(), transient=True) as progress:
        for source in progress.track(sources, description="Compiling source files..."):
            source = source.strip()
            if source:
                object_file = os.path.join(output_dir, os.path.basename(source).replace('.c', '.o'))
                include_flags = " ".join([f"-I{dir.strip()}" for dir in include_dirs if dir.strip()])
                
                # Adjust define flags based on the compiler
                if "emcc" in compiler:
                    define_flags = " ".join([f"-s {define.strip()}" for define in defines if define.strip()])
                else:
                    define_flags = " ".join([f"-D{define.strip()}" for define in defines if define.strip()])
                
                run_command(f"{compiler} -c {source} {include_flags} {define_flags} -o {object_file}")
                object_files.append(object_file)

    link_flags = " ".join([f"-l{lib.strip()}" for lib in libraries if lib.strip()])
    library_flags = " ".join([f"-L{lib_dir.strip()}" for lib_dir in library_dirs if lib_dir.strip()])
    object_files_str = " ".join(object_files)

    final_command = build_command(compiler, output_type, object_files_str, output_dir, project_name, link_flags, library_flags)
    console.print(f"[bold yellow]Running final command:[/] {final_command}")
    run_command(final_command)

    clean_intermediate_files(object_files)
    
    console.print(Panel(f"[bold green]Build Successful[/] : [bold cyan]{project_name}[/] at [bold magenta]{output_dir}[/]"))

def main():
    parser = argparse.ArgumentParser(description="CBUILD - A Simple C Build Tool")
    parser.add_argument('config', help="Path to the .cbuild configuration file")
    args = parser.parse_args()

    config = parse_config(args.config)

    build_project(config)

if __name__ == "__main__":
    main()
