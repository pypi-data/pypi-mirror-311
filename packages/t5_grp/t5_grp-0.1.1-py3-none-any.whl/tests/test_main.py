import os
import tempfile
import unittest
from unittest.mock import patch
from t5_grp.main import main
from t5_grp.visualization.diagram_generator import generate_yaml_html


class TestMainFunction(unittest.TestCase):

    @patch("t5_grp.parser.yaml_parser.parse_yaml")
    @patch("t5_grp.visualization.diagram_generator.generate_html")
    def test_main_without_cleanup(self, mock_generate_html, mock_parse_yaml):
        # Mock return value
        mock_parse_yaml.return_value = {
            "pipeline": {"name": "P1"},
            "__file__": "test.yaml",
        }

        test_yaml_path = "test.yaml"
        test_output_path = "output.html"
        test_theme = "light"
        test_stage_gap = 60

        with open(test_yaml_path, "w") as f:
            f.write("pipeline:\n  name: P1")

        try:
            main(
                test_yaml_path,
                output_path=test_output_path,
                theme=test_theme,
                stage_gap=test_stage_gap,
                cleanup=False,
            )

            mock_parse_yaml.assert_called_once_with(test_yaml_path)
            mock_generate_html.assert_called_once_with(
                {"pipeline": {"name": "P1"}, "__file__": "test.yaml"},
                output_path=test_output_path,
                theme=test_theme,
                stage_gap=test_stage_gap,
            )

        finally:
            if os.path.exists(test_yaml_path):
                os.remove(test_yaml_path)

    @patch("t5_grp.parser.yaml_parser.parse_yaml")
    @patch("t5_grp.visualization.diagram_generator.generate_html")
    def test_main_with_cleanup(self, mock_generate_html, mock_parse_yaml):
        mock_parse_yaml.return_value = {
            "pipeline": {"name": "P1"},
            "__file__": "test.yaml",
        }

        test_yaml_path = "test.yaml"
        test_output_path = "output.html"
        test_theme = "light"
        test_stage_gap = 60

        with open(test_yaml_path, "w") as f:
            f.write("pipeline:\n  name: P1")

        try:
            # Create dummy files to simulate generated files
            with open(test_output_path, "w") as f:
                f.write("dummy content")

            yaml_html_path = f"{os.path.splitext(test_yaml_path)[0]}_yaml.html"
            with open(yaml_html_path, "w") as f:
                f.write("dummy content")

            os.makedirs("assets", exist_ok=True)

            main(
                test_yaml_path,
                output_path=test_output_path,
                theme=test_theme,
                stage_gap=test_stage_gap,
                cleanup=True,
            )

            # Verify files were cleaned up
            self.assertFalse(os.path.exists(test_output_path))
            self.assertFalse(os.path.exists(yaml_html_path))
            self.assertFalse(os.path.exists("assets"))

        finally:
            # Cleanup any remaining test files
            if os.path.exists(test_yaml_path):
                os.remove(test_yaml_path)
            if os.path.exists(test_output_path):
                os.remove(test_output_path)
            if os.path.exists(yaml_html_path):
                os.remove(yaml_html_path)
            if os.path.exists("assets"):
                import shutil

                shutil.rmtree("assets")

    def test_yaml_html_generation(self):
        """Test YAML HTML file generation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test YAML file
            test_yaml_content = "pipeline:\n  name: Test Pipeline"
            test_yaml_path = os.path.join(temp_dir, "test.yaml")
            with open(test_yaml_path, "w") as f:
                f.write(test_yaml_content)

            # Generate HTML from YAML
            html_filename = generate_yaml_html(test_yaml_path, temp_dir)
            html_path = os.path.join(temp_dir, html_filename)

            # Verify the generated HTML file
            self.assertTrue(os.path.exists(html_path))
            self.assertEqual(html_filename, "test_yaml.html")

            # Check content of generated HTML
            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("test.yaml", content)  # Check title
                # Check for Pygments-highlighted content markers
                self.assertIn('<div class="highlight">', content)
                self.assertIn('<span class="nt">pipeline</span>', content)
                self.assertIn("Test Pipeline", content)


if __name__ == "__main__":
    unittest.main()
