"""
Pipeline Diagram Generator
=========================

This module provides functionality to generate visual diagrams for CI/CD pipelines.
It converts pipeline configuration data into an HTML visualization with interactive
elements and dependency arrows.

The module follows a layered architecture:
1. Infrastructure Layer: Environment setup and asset management
2. Dependency Layer: Job dependency processing and sorting
3. Processing Layer: Job and stage data processing
4. Extraction Layer: Pipeline data extraction and transformation
5. Generation Layer: Final HTML visualization generation

Key Features:
- HTML generation from pipeline configuration
- Asset management and copying
- Job dependency sorting and visualization
- Artifact tracking across stages
"""

import os
import shutil
from collections import defaultdict, deque
from typing import Any, Dict, List, Set
from jinja2 import Environment, FileSystemLoader

from ..config import (
    ASSET_FILES,
    TEMPLATE_DIR_NAME,
    TEMPLATE_FILE,
    ASSETS_FOLDER,
)


def setup_jinja_environment() -> Environment:
    """Setup and configure Jinja2 environment for template rendering.

    Returns:
        Environment: Configured Jinja2 environment with template loader and autoescaping

    Note:
        - Uses FileSystemLoader to load templates from TEMPLATE_DIR_NAME
        - Enables autoescaping for security
    """
    return Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "..", TEMPLATE_DIR_NAME)
        ),
        autoescape=True,
    )


def copy_assets(output_dir: str) -> None:
    """Copy static assets to the output directory.

    Args:
        output_dir: Target directory path for assets

    Note:
        - Creates assets directory if it doesn't exist
        - Copies CSS, JS and other static files
        - Preserves file metadata using shutil.copy2
    """
    assets_src_dir = os.path.join(os.path.dirname(__file__), "..", ASSETS_FOLDER)
    assets_dst_dir = os.path.join(output_dir, ASSETS_FOLDER)
    os.makedirs(assets_dst_dir, exist_ok=True)

    for asset in ASSET_FILES:
        src = os.path.join(assets_src_dir, asset)
        dst = os.path.join(assets_dst_dir, asset)
        if os.path.exists(src):
            shutil.copy2(src, dst)


def sort_jobs_by_dependency(jobs: list) -> list:
    """Sort jobs based on dependency count within the same stage.

    Args:
        jobs: List of (job_name, job_info) tuples to sort

    Returns:
        List of sorted job tuples ordered by:
        1. Number of same-stage dependencies
        2. Being needed count (dependency_count)
        3. Original position

    Note:
        - Higher priority jobs appear first (reverse=True)
        - Only considers dependencies within the same stage
        - Uses job's dependency_count as secondary sort key
    """

    def get_dependency_weight(job):
        current_stage = job[1].get("stage")
        same_stage_needs = sum(
            1
            for need in job[1].get("needs", [])
            if any(
                other_job[1].get("stage") == current_stage
                for other_job in jobs
                if other_job[0] == need
            )
        )
        being_needed_count = job[1].get("dependency_count", 0)
        return (same_stage_needs, being_needed_count, job[1].get("position", 0))

    return sorted(jobs, key=lambda x: get_dependency_weight(x), reverse=True)


def create_dependency_graph(jobs: Dict[str, Any]) -> Dict[str, List[str]]:
    """Create adjacency list representation of job dependencies.

    Args:
        jobs: Dictionary of job information

    Returns:
        Dict mapping job names to lists of dependent job names

    Note:
        - Creates directed graph structure
        - Each key is a job that is needed by others
        - Values are lists of jobs that need the key job
    """
    graph = defaultdict(list)
    for job_name, job_info in jobs.items():
        for need in job_info.get("needs", []):
            graph[need].append(job_name)
    return graph


def topological_sort(jobs: Dict[str, Any]) -> List[str]:
    """Sort jobs topologically based on their dependencies.

    Args:
        jobs: Dictionary of job information

    Returns:
        List of job names in topologically sorted order

    Raises:
        ValueError: If circular dependencies are detected

    Note:
        - Uses Kahn's algorithm for topological sorting
        - Detects circular dependencies
        - Ensures dependent jobs come after their dependencies
    """
    graph = create_dependency_graph(jobs)
    in_degree = defaultdict(int)

    for job_name in jobs:
        for dependent in graph[job_name]:
            in_degree[dependent] += 1

    queue = deque([job for job in jobs if in_degree[job] == 0])
    sorted_jobs = []

    while queue:
        job = queue.popleft()
        sorted_jobs.append(job)

        for dependent in graph[job]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    if len(sorted_jobs) != len(jobs):
        raise ValueError("Circular dependencies detected in pipeline")

    return sorted_jobs


def calculate_job_priority(
    job_name: str, pip_info: Dict[str, Any], needs: List[str]
) -> int:
    """Calculate job priority based on dependencies.

    Args:
        job_name: Name of the job to calculate priority for
        pip_info: Pipeline information dictionary
        needs: List of job dependencies

    Returns:
        Priority level (0-3):
        - 0: No dependencies, not depended on
        - 1: No dependencies, is depended on
        - 2: Has dependencies, is depended on
        - 3: Has dependencies, not depended on

    Note:
        - Higher priority (lower number) given to jobs others depend on
        - Considers both incoming and outgoing dependencies
    """
    is_needed = any(
        job_name in job_info.get("needs", []) for job_info in pip_info["jobs"].values()
    )
    has_needs = bool(needs)

    if is_needed and has_needs:
        return 2
    elif is_needed:
        return 1
    elif has_needs:
        return 3
    return 0


def process_job_dependencies(
    pip_info: Dict[str, Any], job_name: str, stage_name: str, needs: List[str]
) -> None:
    """Process and record job dependencies.

    Args:
        pip_info: Pipeline information dictionary
        job_name: Name of the current job
        stage_name: Name of the current stage
        needs: List of job dependencies

    Note:
        - Adjusts job positions to maintain dependency order
        - Records dependency relationships for visualization
        - Handles cross-stage and same-stage dependencies
    """
    for need in needs:
        if need in pip_info["jobs"]:
            dep_job = pip_info["jobs"][need]
            if dep_job["position"] > pip_info["jobs"][job_name]["position"]:
                temp_pos = dep_job["position"]
                dep_job["position"] = pip_info["jobs"][job_name]["position"]
                pip_info["jobs"][job_name]["position"] = temp_pos

            pip_info["dependencies"].append(
                {
                    "from": f"job_{need}",
                    "to": f"job_{job_name}",
                    "fromStage": pip_info["jobs"][need]["stage"],
                    "toStage": stage_name,
                }
            )


def process_job_artifacts(
    pip_info: Dict[str, Any],
    job: Dict[str, Any],
    stage_name: str,
    stage_artifacts: Dict[str, Set[str]],
    all_artifacts: Set[str],
) -> None:
    """Process and record job artifacts.

    Args:
        pip_info: Pipeline information dictionary
        job: Job configuration dictionary
        stage_name: Name of the current stage
        stage_artifacts: Dictionary mapping stages to their artifacts
        all_artifacts: Set of all artifacts across all stages

    Note:
        - Collects artifact paths from job configuration
        - Updates stage-specific artifact collections
        - Maintains global artifact registry
    """
    if "artifacts" in job:
        paths = job["artifacts"].get("paths", [])
        if stage_name not in stage_artifacts:
            stage_artifacts[stage_name] = set()
        stage_artifacts[stage_name].update(paths)
        all_artifacts.update(paths)


def add_job_info(
    pip_info: Dict[str, Any],
    job: Dict[str, Any],
    job_name: str,
    stage_name: str,
    stage_artifacts: Dict[str, Set[str]],
    all_artifacts: Set[str],
) -> None:
    """Add job information to pipeline data structure.

    Args:
        pip_info: Pipeline information dictionary to update
        job: Job configuration dictionary containing job details
        job_name: Name of the job being processed
        stage_name: Name of the stage containing the job
        stage_artifacts: Dictionary tracking artifacts per stage
        all_artifacts: Set of all artifacts in pipeline

    Note:
        - Creates job entry with complete configuration
        - Updates stage job listings
        - Processes dependencies and artifacts
        - Calculates job priority based on dependencies
    """
    # Extract job needs (dependencies)
    needs = job.get("needs", [])
    # Create comprehensive job entry
    pip_info["jobs"][job_name] = {
        "stage": stage_name,
        "needs": needs,
        "allow_failure": job.get("allow_failure", False),
        "id": f"job_{job_name}",
        "position": len(pip_info["jobs"]),
        "artifacts": job.get("artifacts", {}).get("paths", []),
        "dependency_count": calculate_job_priority(job_name, pip_info, needs),
        "__line_info": job.get("__line_info", {"start_line": 0}),
    }
    # Add job to its stage
    for stage in pip_info["stages"]:
        if stage["name"] == stage_name:
            stage["jobs"].append((job_name, pip_info["jobs"][job_name]))
            break
    # Process job dependencies and artifacts
    process_job_dependencies(pip_info, job_name, stage_name, needs)
    process_job_artifacts(pip_info, job, stage_name, stage_artifacts, all_artifacts)


def process_stages(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract and process pipeline stages."""
    return [
        {"name": stage_name, "jobs": [], "artifacts": []}
        for stage_name in data.get("stages", [])
    ]


def extract_pipeline_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and structure pipeline data for visualization.

    Args:
        data: Raw pipeline configuration dictionary

    Returns:
        Processed pipeline data dictionary containing:
        - name: Pipeline name
        - stages: List of stage information
        - jobs: Dictionary of job configurations
        - dependencies: List of dependency relationships
        - artifacts: Dictionary of stage artifacts
        - all_artifacts: List of all pipeline artifacts

    Note:
        - Processes stages, jobs, and artifacts
        - Sorts jobs within stages by dependency
        - Performs topological sort for job positioning
        - Maintains artifact collections
    """
    # Initialize pipeline data structure
    pipeline_info = {
        "name": data["pipeline"]["name"],
        "stages": [],
        "jobs": {},
        "dependencies": [],
        "artifacts": {},
        "all_artifacts": [],
    }
    # Initialize artifact tracking
    stage_artifacts: Dict[str, Set[str]] = {}
    all_artifacts: Set[str] = set()
    # Process stages first
    pipeline_info["stages"] = process_stages(data)
    # Process all jobs
    for job in data.get("jobs", []):
        job_name = job.get("name")
        stage_name = job.get("stage")
        if job_name and stage_name:
            add_job_info(
                pipeline_info, job, job_name, stage_name, stage_artifacts, all_artifacts
            )
    # Sort jobs within each stage
    for stage in pipeline_info["stages"]:
        stage_jobs = [
            (name, job)
            for name, job in pipeline_info["jobs"].items()
            if job["stage"] == stage["name"]
        ]
        stage["jobs"] = sort_jobs_by_dependency(stage_jobs)
    # Update positions based on topological sort
    sorted_jobs = topological_sort(pipeline_info["jobs"])
    for pos, job_name in enumerate(sorted_jobs):
        pipeline_info["jobs"][job_name]["position"] = pos

    for job_name, job_info in pipeline_info["jobs"].items():
        needs = job_info["needs"]
        job_info["dependency_count"] = calculate_job_priority(
            job_name, pipeline_info, needs
        )
    # Finalize artifact collections
    for stage, artifacts in stage_artifacts.items():
        pipeline_info["artifacts"][stage] = sorted(list(artifacts))
    pipeline_info["all_artifacts"] = sorted(list(all_artifacts))

    return pipeline_info


def generate_html(
    data: Dict[str, Any],
    output_path: str = "output.html",
    theme: str = "light",
    stage_gap: int = 60,
) -> None:
    """Generate HTML visualization of pipeline configuration.

    Args:
        data: Pipeline configuration data
        output_path: Path where the HTML file will be generated
        theme: Visual theme (light/dark)
        stage_gap: Gap between stages in pixels

    Raises:
        ValueError: If output_path is not provided

    Note:
        - Extracts and processes pipeline data
        - Configures visualization parameters
        - Renders HTML template with pipeline data
        - Copies required assets to output directory
    """
    # Validate output path
    if not output_path:
        raise ValueError("output_path must be provided")
    # Process pipeline data and setup environment
    pipeline_data = extract_pipeline_data(data)
    env = setup_jinja_environment()
    template = env.get_template(TEMPLATE_FILE)
    # Configure visualization parameters
    config = {
        "theme": theme,
        "stage_gap": stage_gap,
        "job_height": 40,
        "job_width": 120,
    }
    # Generate YAML HTML file
    output_dir = os.path.dirname(os.path.abspath(output_path))
    yaml_html_filename = generate_yaml_html(data["__file__"], output_dir)
    # Render template with all required data
    html_output = template.render(
        pipeline=pipeline_data,
        asset_path=ASSETS_FOLDER,
        yaml_path=yaml_html_filename,
        theme=theme,
        config=config,
        dependencies=pipeline_data["dependencies"],
        jobs=pipeline_data["jobs"],
    )
    # Ensure output directory exists and copy assets
    output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    copy_assets(output_dir)
    # Write generated HTML to file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_output)


def generate_yaml_html(yaml_path: str, output_dir: str) -> str:
    """Generate HTML version of YAML file with syntax highlighting."""
    from pygments import highlight
    from pygments.lexers import YamlLexer
    from pygments.formatters import HtmlFormatter

    with open(yaml_path, "r") as f:
        yaml_content = f.read()

    # Generate syntax highlighted HTML
    highlighted_code = highlight(
        yaml_content,
        YamlLexer(),
        HtmlFormatter(
            linenos=True,
            lineanchors="line",
            linespans="line",
            anchorlinenos=True,
            wrapcode=True,
        ),
    )

    yaml_filename = os.path.basename(yaml_path)
    html_filename = f"{os.path.splitext(yaml_filename)[0]}_yaml.html"
    html_path = os.path.join(output_dir, html_filename)

    env = setup_jinja_environment()
    template = env.get_template("yaml_viewer_template.html")

    # Add Pygments CSS
    pygments_css = HtmlFormatter().get_style_defs(".highlight")

    html_output = template.render(
        filename=yaml_filename,
        highlighted_code=highlighted_code,
        pygments_css=pygments_css,
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    return html_filename
