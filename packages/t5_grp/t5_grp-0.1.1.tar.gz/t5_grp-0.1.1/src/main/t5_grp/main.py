import os
import shutil


from .visualization import diagram_generator
import argparse
from .parser import yaml_parser


def main(
    yaml_file_path,
    output_path="output.html",
    theme="light",
    stage_gap=60,
    cleanup=False,
):
    """
    Parses the given YAML file and generates an HTML visualization.

    Args:
        yaml_file_path (str): Path to the YAML file containing the CI/CD configuration.
        output_path (str): Path where the visualization will be generated.
        theme (str): Theme for visualization (light/dark).
        stage_gap (int): Gap between stages in pixels.
    """
    try:
        data = yaml_parser.parse_yaml(yaml_file_path)
        if data is None:
            print("Failed to parse YAML file or validation error occurred.")
            print(f" @{os.path.basename(yaml_file_path)} ")
            return

        data["__file__"] = yaml_file_path

        diagram_generator.generate_html(
            data, output_path=output_path, theme=theme, stage_gap=stage_gap
        )
        if cleanup:
            # Clean up generated files
            output_dir = os.path.dirname(os.path.abspath(output_path))
            # 1. Clean up main output file
            os.remove(output_path)
            # 2. Clean up YAML HTML file
            yaml_html_filename = (
                f"{os.path.splitext(os.path.basename(yaml_file_path))[0]}_yaml.html"
            )
            yaml_html_path = os.path.join(output_dir, yaml_html_filename)
            if os.path.exists(yaml_html_path):
                os.remove(yaml_html_path)
            # 3. Clean up copied assets folder
            assets_dir = os.path.join(output_dir, "assets")
            if os.path.exists(assets_dir):
                shutil.rmtree(assets_dir)
            print("Cleaned up generated files.")
        else:
            print(
                f"Generated output.html successfully at: {os.path.abspath(output_path)}"
            )

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("yaml_file", help="Path to CI/CD config YAML file")

    parser.add_argument(
        "-o",
        "--output",
        default="output.html",
        help="Output file path (default: output.html)",
    )

    parser.add_argument(
        "-t",
        "--theme",
        choices=["light", "dark"],
        default="light",
        help="Select visualization theme (light/dark)",
    )

    parser.add_argument(
        "--stage-gap",
        type=int,
        default=60,
        help="Gap between stages in pixels (default: 60)",
    )

    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Delete generated files after creation",
    )

    args = parser.parse_args()
    main(
        args.yaml_file,
        output_path=args.output,
        theme=args.theme,
        stage_gap=args.stage_gap,
        cleanup=args.cleanup,
    )


if __name__ == "__main__":
    cli()
