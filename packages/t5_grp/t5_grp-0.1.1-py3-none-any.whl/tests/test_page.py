import shutil
import tempfile
import unittest
import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

from t5_grp.parser.yaml_parser import parse_yaml
from t5_grp.visualization.diagram_generator import generate_html
from tests.page.page import PipelinePage

from src.main.t5_grp.config import (
    TEST_PIPELINE_NAME,
    PROJECT_ROOT,
    ASSETS_FOLDER,
    ASSET_FILES,
    TEST_FILES_DIR,
    TEST_YAML_FILE,
    MAIN_FOLDER,
    TEMP_HTML_FILE,
)


class PipelinePageTest(unittest.TestCase):
    """Test class for pipeline visualization page.
    Tests the functionality of pipeline structure, stages,
    jobs, and their relationships."""

    def setUp(self) -> None:
        """Set up test environment before each test.
        Initializes Chrome WebDriver in headless mode
        and loads the pipeline HTML page."""
        try:
            # Create temporary directory for test files
            self.temp_dir = tempfile.mkdtemp()

            # Parse test YAML file
            test_yaml_path = os.path.join(
                os.path.dirname(__file__), TEST_FILES_DIR, TEST_YAML_FILE
            )
            pipeline_data = parse_yaml(test_yaml_path)
            pipeline_data["__file__"] = test_yaml_path

            # Generate temporary HTML file
            self.temp_html = os.path.join(self.temp_dir, TEMP_HTML_FILE)
            generate_html(pipeline_data, output_path=self.temp_html)
            # Copy necessary resources (CSS and favicon) to temporary directory
            assets_src_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                MAIN_FOLDER,
                PROJECT_ROOT,
                ASSETS_FOLDER,
            )
            assets_dst_dir = os.path.join(self.temp_dir, PROJECT_ROOT, ASSETS_FOLDER)
            os.makedirs(assets_dst_dir, exist_ok=True)
            for asset in ASSET_FILES:
                src = os.path.join(assets_src_dir, asset)
                dst = os.path.join(assets_dst_dir, asset)
                if os.path.exists(src):
                    shutil.copy2(src, dst)

            # Configure Chrome options for running in CI/GitHub Actions environment:
            # --no-sandbox: Disable the sandbox for running in CI environment
            # --headless: Run Chrome in headless mode (without GUI)
            # --disable-dev-shm-usage: Overcome limited resource issues in CI containers
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(options=chrome_options)
            file_url = f"file://{os.path.abspath(self.temp_html)}"
            self.driver.get(file_url)
            self.pipeline_page = PipelinePage(self.driver)
        except WebDriverException as e:
            self.fail(f"Failed to setup test environment: {str(e)}")

    def test_pipeline_structure(self) -> None:
        """Test if pipeline structure is valid"""
        result = self.pipeline_page.verify_pipeline_structure()
        self.assertTrue(
            result.success, f"Pipeline structure verification failed: {result.message}"
        )

    def test_pipeline_name(self) -> None:
        """Test if pipeline name is correct"""
        name = self.pipeline_page.get_pipeline_name()
        self.assertIsNotNone(name, "Pipeline name should not be None")
        self.assertEqual(
            name, TEST_PIPELINE_NAME, f"Pipeline name should be '{TEST_PIPELINE_NAME}'"
        )

    def test_pipeline_stages(self) -> None:
        """Test if pipeline stages are correct"""
        expected_stages = ["build", "test", "doc", "deploy"]
        stages = self.pipeline_page.get_stages()
        self.assertEqual(
            stages,
            expected_stages,
            f"Expected stages {expected_stages}, but got {stages}",
        )

    def test_stage_artifacts(self) -> None:
        """Test stage artifacts"""
        test_cases = {
            "build": ["build/classes/*", "build/reports/*"],
            "test": ["final.jar"],
            "deploy": ["distribution.tgz", "md5.sum"],
        }

        for stage, expected in test_cases.items():
            with self.subTest(stage=stage):
                artifacts = self.pipeline_page.get_stage_artifacts(stage)
                self.assertEqual(
                    artifacts, expected, f"Stage {stage} artifacts mismatch"
                )

    def test_job_dependencies(self) -> None:
        """Test job dependencies in the pipeline.
        Verifies that:
        1. Jobs without dependencies are correctly identified
        2. Jobs with dependencies have correct dependency relationships
        3. Dependency chains are properly maintained
        """
        test_cases = {
            "compile": ["static_analysis"],
            "static_analysis": [],
            "unit_test": ["compile"],
            "generate_docs": ["unit_test"],
            "publish": ["generate_docs"],
        }

        no_deps_jobs = [job for job, deps in test_cases.items() if not deps]
        for job in no_deps_jobs:
            with self.subTest(job=job):
                deps = self.pipeline_page.get_job_dependencies(job)
                self.assertEqual(deps, [], f"Job {job} should have no dependencies")

        has_deps_jobs = [job for job, deps in test_cases.items() if deps]
        for job in has_deps_jobs:
            with self.subTest(job=job):
                deps = self.pipeline_page.get_job_dependencies(job)
                self.assertEqual(
                    sorted(deps),
                    sorted(test_cases[job]),
                    f"Job {job} dependencies mismatch: "
                    f"expected {test_cases[job]}, got {deps}",
                )

    def test_job_properties(self) -> None:
        """Test allow_failure property"""
        self.assertTrue(
            self.pipeline_page.is_job_allow_failure("static_analysis"),
            "static_analysis should allow failure",
        )
        self.assertFalse(
            self.pipeline_page.is_job_allow_failure("compile"),
            "compile should not allow failure",
        )

    def test_complete_pipeline_data(self) -> None:
        """Test complete pipeline data structure"""
        pipeline_data = self.pipeline_page.get_pipeline_data()
        self.assertIsNotNone(pipeline_data, "Pipeline data should not be None")

        # Verify basic structure
        self.assertEqual(pipeline_data.name, TEST_PIPELINE_NAME)
        self.assertEqual(len(pipeline_data.stages), 4)

        # Verify all artifacts
        expected_artifacts = [
            "build/classes/*",
            "build/reports/*",
            "distribution.tgz",
            "final.jar",
            "md5.sum",
        ]
        self.assertEqual(
            sorted(pipeline_data.all_artifacts), sorted(expected_artifacts)
        )

    def tearDown(self) -> None:
        """Clean up after each test"""
        try:
            if hasattr(self, "driver"):
                self.driver.quit()
        except Exception as e:
            print(f"Warning: Failed to quit WebDriver: {str(e)}")
        finally:
            try:
                # Clean up temporary directory and all its contents
                if hasattr(self, "temp_dir") and os.path.exists(self.temp_dir):
                    shutil.rmtree(self.temp_dir)

                # Clean up t5_grp directory in project root
                project_root = os.path.dirname(
                    os.path.dirname(os.path.dirname(__file__))
                )
                t5_grp_dir = os.path.join(project_root, PROJECT_ROOT)
                if os.path.exists(t5_grp_dir):
                    shutil.rmtree(t5_grp_dir)
            except Exception as e:
                print(f"Warning: Cleanup failed: {str(e)}")


if __name__ == "__main__":
    unittest.main()
