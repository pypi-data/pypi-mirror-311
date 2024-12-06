from selenium.webdriver.common.by import By
from typing import Tuple, Optional
import logging

LocatorType = Tuple[str, str]


class PipelinePageLocators(object):
    """Locators for pipeline visualization page elements"""

    # Header elements
    PIPELINE_NAME = (By.ID, "pipeline-title")
    PIPELINE_DESCRIPTION = (By.CLASS_NAME, "pipeline-description")

    # Pipeline structure elements
    PIPELINE_CONTAINER = (By.CLASS_NAME, "pipeline-container")
    STAGES_CONTAINER = (By.CLASS_NAME, "stages-container")

    # Stage elements
    STAGE = (By.CLASS_NAME, "stage")
    STAGE_TITLE = (By.CLASS_NAME, "stage-title")
    STAGE_CONTENT = (By.CLASS_NAME, "stage-content")
    EMPTY_STAGE = (By.CLASS_NAME, "empty-stage")

    # Job elements
    JOB = (By.CLASS_NAME, "job")
    JOB_NAME = (By.CLASS_NAME, "job-name")
    JOB_STATUS = (By.CLASS_NAME, "job-status")

    # Artifact elements
    ARTIFACTS_BOX = (By.CLASS_NAME, "artifacts-box")
    ARTIFACTS_TITLE = (By.CLASS_NAME, "artifacts-title")
    ARTIFACTS_LIST = (By.CLASS_NAME, "artifacts-list")
    ARTIFACT_ITEM = (By.TAG_NAME, "li")

    # Dependency elements
    ARROWS_CONTAINER = (By.CLASS_NAME, "arrows")
    DEPENDENCY_ARROW = (By.TAG_NAME, "path")

    @classmethod
    def stage_by_name(cls, stage_name: str) -> Optional[LocatorType]:
        """Get stage locator by name"""
        try:
            safe_name = stage_name.replace('"', '\\"').replace("'", "\\'")
            return (
                By.XPATH,
                f"//div[contains(@class, 'stage-title')]"
                f"[contains(text(), '{safe_name}')]",
            )
        except Exception as e:
            logging.error(f"Failed to create stage locator: {str(e)}")
            return None

    @classmethod
    def job_by_id(cls, job_id: str) -> Optional[LocatorType]:
        """Get job locator by ID"""
        try:
            if not job_id.strip():
                raise ValueError("Job ID cannot be empty")
            return By.ID, f"job_{job_id}"
        except Exception as e:
            logging.error(f"Failed to create job locator: {str(e)}")
            return None

    @classmethod
    def get_dependency_arrow_locator(
        cls, from_id: str, to_id: str
    ) -> Optional[LocatorType]:
        """Get dependency arrow locator between jobs"""
        try:
            return (
                By.XPATH,
                f"//path[@data-source='job_{from_id}' and @data-target='job_{to_id}']",
            )
        except Exception as e:
            logging.error(f"Failed to create dependency locator: {str(e)}")
            return None

    @classmethod
    def stage_artifacts(cls, stage_name: str) -> Optional[LocatorType]:
        """Get stage artifacts locator"""
        try:
            safe_name = stage_name.replace('"', '\\"').replace("'", "\\'")
            return (
                By.XPATH,
                f"//div[contains(@class, 'artifacts-title')]"
                f"[contains(text(), '{safe_name} Artifacts')]"
                f"/following-sibling::ul[@class='artifacts-list']/li",
            )
        except Exception as e:
            logging.error(f"Failed to create artifacts locator: {str(e)}")
            return None

    @classmethod
    def validate_locator(cls, locator: Optional[LocatorType]) -> bool:
        """Validate if locator is properly formed"""
        if not locator or not isinstance(locator, tuple) or len(locator) != 2:
            return False
        return isinstance(locator[0], str) and isinstance(locator[1], str)
