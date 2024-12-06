import os
import tempfile
import unittest
from t5_grp.visualization.diagram_generator import (
    generate_html,
    extract_pipeline_data,
    add_job_info,
    process_stages,
    calculate_job_priority,
    topological_sort,
    create_dependency_graph,
)
from t5_grp.config import ASSETS_FOLDER, ASSET_FILES, TEST_OUTPUT_FILENAME


class TestDiagramGenerator(unittest.TestCase):
    """Test suite for the diagram_generator module."""

    def setUp(self):
        """Set up test fixtures"""
        self.pip_info = {
            "stages": [{"name": "test_stage", "jobs": [], "artifacts": []}],
            "jobs": {},
            "dependencies": [],
        }
        self.stage_artifacts = {}
        self.all_artifacts = set()

    def test_process_stages(self):
        """Test stage processing functionality"""
        test_data = {"stages": ["build", "test", "deploy"]}
        result = process_stages(test_data)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "build")
        self.assertEqual(result[1]["name"], "test")
        self.assertEqual(result[2]["name"], "deploy")
        for stage in result:
            self.assertEqual(stage["jobs"], [])
            self.assertEqual(stage["artifacts"], [])

    def test_dependency_management(self):
        """Test dependency graph creation and topological sorting"""
        test_jobs = {
            "build": {"needs": []},
            "test": {"needs": ["build"]},
            "deploy": {"needs": ["test"]},
        }

        # Test dependency graph creation
        graph = create_dependency_graph(test_jobs)
        self.assertEqual(graph["build"], ["test"])
        self.assertEqual(graph["test"], ["deploy"])
        self.assertEqual(graph["deploy"], [])

        # Test topological sorting
        sorted_jobs = topological_sort(test_jobs)
        self.assertEqual(sorted_jobs, ["build", "test", "deploy"])

        # Test circular dependency detection
        circular_jobs = {"job1": {"needs": ["job2"]}, "job2": {"needs": ["job1"]}}
        with self.assertRaises(ValueError):
            topological_sort(circular_jobs)

    def test_job_priority_calculation(self):
        """Test job priority calculation and dependencies"""
        job1 = {"name": "job1", "stage": "test_stage"}
        job2 = {"name": "job2", "stage": "test_stage"}
        job3 = {"name": "job3", "stage": "test_stage", "needs": ["job2"]}

        add_job_info(
            self.pip_info,
            job1,
            "job1",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )
        add_job_info(
            self.pip_info,
            job2,
            "job2",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )
        add_job_info(
            self.pip_info,
            job3,
            "job3",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )
        for job_name in self.pip_info["jobs"]:
            needs = self.pip_info["jobs"][job_name]["needs"]
            self.pip_info["jobs"][job_name]["dependency_count"] = (
                calculate_job_priority(job_name, self.pip_info, needs)
            )

        self.assertEqual(self.pip_info["jobs"]["job1"]["dependency_count"], 0)
        self.assertEqual(self.pip_info["jobs"]["job2"]["dependency_count"], 1)
        self.assertEqual(self.pip_info["jobs"]["job3"]["dependency_count"], 3)

    def test_artifact_processing(self):
        """Test artifact processing functionality"""
        job_with_artifacts = {
            "name": "job_artifacts",
            "stage": "test_stage",
            "artifacts": {"paths": ["test.txt", "report.pdf"]},
        }
        add_job_info(
            self.pip_info,
            job_with_artifacts,
            "job_artifacts",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )

        self.assertEqual(self.stage_artifacts["test_stage"], {"test.txt", "report.pdf"})
        self.assertTrue({"test.txt", "report.pdf"}.issubset(self.all_artifacts))

    def test_pipeline_data_extraction(self):
        """Test complete pipeline data extraction"""
        test_data = {
            "pipeline": {"name": "Test Pipeline"},
            "stages": ["build", "test"],
            "jobs": [
                {
                    "name": "build_job",
                    "stage": "build",
                    "artifacts": {"paths": ["build.txt"]},
                },
                {"name": "test_job", "stage": "test", "needs": ["build_job"]},
            ],
        }

        result = extract_pipeline_data(test_data)

        self.assertEqual(result["name"], "Test Pipeline")
        self.assertEqual(len(result["stages"]), 2)
        self.assertEqual(len(result["jobs"]), 2)
        self.assertEqual(result["jobs"]["test_job"]["needs"], ["build_job"])
        self.assertIn("build.txt", result["artifacts"]["build"])
        self.assertIn("build.txt", result["all_artifacts"])
        self.assertTrue(
            result["jobs"]["build_job"]["position"]
            < result["jobs"]["test_job"]["position"]
        )

    def test_html_generation(self):
        """Test HTML generation with different configurations"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_yaml_path = os.path.join(temp_dir, "test.yaml")
            with open(test_yaml_path, "w") as f:
                f.write("pipeline:\n  name: Test Pipeline")

            test_data = {
                "pipeline": {
                    "name": "Test Pipeline",
                    "stages": ["build", "test"],
                    "jobs": [
                        {"name": "job1", "stage": "build"},
                        {"name": "job2", "stage": "test", "needs": ["job1"]},
                    ],
                },
                "__file__": test_yaml_path,
            }
            output_path = os.path.join(temp_dir, TEST_OUTPUT_FILENAME)

            # Test default theme
            generate_html(test_data, output_path)
            self._verify_html_output(output_path, "light", 60)

            # Test dark theme
            generate_html(test_data, output_path, theme="dark")
            self._verify_html_output(output_path, "dark", 60)

    def _verify_html_output(self, output_path: str, theme: str, stage_gap: int):
        """Helper method to verify HTML output"""
        self.assertTrue(os.path.exists(output_path))
        assets_dir = os.path.join(os.path.dirname(output_path), ASSETS_FOLDER)
        self.assertTrue(os.path.exists(assets_dir))

        for asset in ASSET_FILES:
            self.assertTrue(os.path.exists(os.path.join(assets_dir, asset)))

        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Test Pipeline", content)
            self.assertIn('href="assets/main.css"', content)
            self.assertIn('src="assets/main.js"', content)


if __name__ == "__main__":
    unittest.main()
