import os
import unittest
from src.main.t5_grp.parser.yaml_parser import parse_yaml


class TestYamlParser(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def test_valid_yaml(self):
        """Tests parsing of a valid YAML file"""
        file_path = os.path.join(self.base_dir, "../test_files/valid.yaml")
        result = parse_yaml(file_path)

        self.assertIsNotNone(result)
        self.assertIn("jobs", result)

        # line test
        for job in result["jobs"]:
            self.assertIn("__line_info", job)
            self.assertIn("start_line", job["__line_info"])
            self.assertGreater(job["__line_info"]["start_line"], 0)

    def test_job_line_numbers(self):
        """Tests specific job line numbers in valid.yaml"""
        file_path = os.path.join(self.base_dir, "../test_files/valid.yaml")
        result = parse_yaml(file_path)

        # validate static_analysis line
        static_analysis = next(
            job for job in result["jobs"] if job["name"] == "static_analysis"
        )
        self.assertEqual(static_analysis["__line_info"]["start_line"], 21)

        # validate compile line
        compile_job = next(job for job in result["jobs"] if job["name"] == "compile")
        self.assertEqual(compile_job["__line_info"]["start_line"], 11)

    def test_job_order(self):
        """Tests that jobs maintain correct order and line information"""
        file_path = os.path.join(self.base_dir, "../test_files/valid.yaml")
        result = parse_yaml(file_path)

        job_names = [job["name"] for job in result["jobs"]]
        expected_order = [
            "compile",
            "static_analysis",
            "unit_test",
            "generate_docs",
            "publish",
        ]

        self.assertEqual(job_names, expected_order)

    def test_invalid_yaml(self):
        """Tests handling of invalid YAML files"""
        file_path = os.path.join(self.base_dir, "../test_files/invalid.yaml")
        result = parse_yaml(file_path)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
