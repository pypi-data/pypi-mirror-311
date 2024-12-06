from typing import Optional, Any
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from tests.page.locators import PipelinePageLocators, LocatorType


class ElementBase(object):
    """Base class for element operations"""

    def __init__(self, locator: LocatorType, timeout: int = 10) -> None:
        if not PipelinePageLocators.validate_locator(locator):
            raise ValueError(f"Invalid locator: {locator}")
        self.locator = locator
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def _wait_for_element(self, driver: WebDriver) -> Optional[WebElement]:
        try:
            return WebDriverWait(driver, self.timeout).until(
                EC.presence_of_element_located(self.locator)
            )
        except WebDriverException as e:
            self.logger.debug(f"Element not found: {self.locator[1]}, error: {str(e)}")
            return None


class BasePageElement(ElementBase):
    """Base element class using descriptor pattern"""

    def __get__(self, obj: Any, owner: type) -> Optional[WebElement]:
        if not obj:
            return None
        return self._wait_for_element(obj.driver)


class BaseElements(ElementBase):
    """Base class for multiple elements"""

    def __get__(self, obj: Any, owner: type) -> list[WebElement]:
        if not obj:
            return []
        try:
            elements = WebDriverWait(obj.driver, self.timeout).until(
                EC.presence_of_all_elements_located(self.locator)
            )
            return elements or []
        except WebDriverException as e:
            self.logger.debug(f"Elements not found: {self.locator[1]}, error: {str(e)}")
            return []


@dataclass
class StageData(object):
    """Data class for stage information"""

    name: str
    jobs: list["JobData"]
    artifacts: list[str]


@dataclass
class JobAttributes(object):
    """Raw job attributes from HTML"""

    id: str
    needs: Optional[str]
    allow_failure: Optional[str]
    style: Optional[str]
    text: str
    stage: str = ""


@dataclass
class JobData(object):
    """Processed job data"""

    id: str
    name: str
    needs: list[str]
    allow_failure: bool
    order: int
    stage: str


class ElementUtils(object):
    """Utility methods for element operations"""

    @staticmethod
    def safe_get_text(element: Optional[WebElement]) -> Optional[str]:
        """Safely get element text"""
        if not element:
            return None
        try:
            return element.text if element else None
        except Exception as e:
            logging.error(f"Failed to get element text: {str(e)}")
            return None

    @staticmethod
    def safe_get_attribute(element: WebElement, name: str) -> Optional[str]:
        """Safely get element attribute"""
        try:
            return element.get_attribute(name)
        except WebDriverException:
            return None

    @staticmethod
    def parse_job_order(style: Optional[str]) -> int:
        """Parse job order from style attribute"""
        if not style or "order:" not in style:
            return 0
        try:
            order_str = style.split("order:")[1].split(";")[0].strip()
            return int(order_str)
        except (IndexError, ValueError):
            return 0


class PipelineElement(object):
    """Pipeline element operations"""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self._init_descriptors()

    def _init_descriptors(self) -> None:
        self.pipeline_title = BasePageElement(PipelinePageLocators.PIPELINE_NAME)
        self.pipeline_desc = BasePageElement(PipelinePageLocators.PIPELINE_DESCRIPTION)

    def get_title(self) -> Optional[str]:
        try:
            title_element = self.pipeline_title.__get__(self, type(self))
            if not title_element or not title_element.text:
                return None
            return title_element.text.strip()
        except Exception as e:
            self.logger.error(f"Failed to get pipeline title: {str(e)}")
            return None


class StagesElement(object):
    """Stage element operations"""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.stages_container = BasePageElement(PipelinePageLocators.STAGES_CONTAINER)
        self.stage_titles = BaseElements(PipelinePageLocators.STAGE_TITLE)

    def get_stages(self) -> list[str]:
        try:
            stage_titles = self.stage_titles.__get__(self, type(self))
            return [title.text.strip() for title in stage_titles if title.text]
        except Exception as e:
            self.logger.error(f"Failed to get stages: {str(e)}")
            return []

    def get_stage_artifacts(self, stage_name: str) -> list[str]:
        try:
            xpath = (
                f"//div[contains(@class, 'stage-artifacts')]"
                f"[contains(@data-stage, '{stage_name}')]"
                f"//li"
            )
            artifacts_elements = self.driver.find_elements(By.XPATH, xpath)
            return [elem.text.strip() for elem in artifacts_elements if elem.text]
        except Exception as e:
            self.logger.error(
                f"Failed to get artifacts for stage {stage_name}: {str(e)}"
            )
            return []


class JobsElement(object):
    """Job element operations"""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def get_stage_jobs(self, stage_name: str) -> list[WebElement]:
        """Get all jobs in a specific stage"""
        try:
            return self.driver.find_elements(
                By.XPATH,
                f"//div[contains(@class, 'job') and @data-stage='{stage_name}']",
            )
        except Exception as e:
            self.logger.error(f"Failed to get jobs for stage {stage_name}: {str(e)}")
            return []

    def get_job_data(self, job_id: str) -> Optional[JobData]:
        """Get job data by ID"""
        result = None
        try:
            # 1. Get job element
            locator = PipelinePageLocators.job_by_id(job_id)
            if locator:
                job = self.driver.find_element(*locator)
                # 2. Extract attributes
                job_attrs = self._extract_job_attributes(job)
                if job_attrs:
                    # 3. Create job data
                    return self._create_job_data(job_attrs)
        except Exception as e:
            self.logger.error(f"Failed to get job data: {str(e)}")
        return result

    def _extract_job_attributes(self, job: WebElement) -> Optional[JobAttributes]:
        """Extract all attributes from job element"""
        try:
            return JobAttributes(
                id=ElementUtils.safe_get_attribute(job, "id") or "",
                needs=ElementUtils.safe_get_attribute(job, "data-needs"),
                allow_failure=ElementUtils.safe_get_attribute(
                    job, "data-allow-failure"
                ),
                style=ElementUtils.safe_get_attribute(job, "style"),
                text=ElementUtils.safe_get_text(job) or "",
                stage=ElementUtils.safe_get_attribute(job, "stage") or "",
            )
        except Exception as e:
            self.logger.error(f"Failed to extract job attributes: {str(e)}")
            return None

    def _create_job_data(self, attrs: JobAttributes) -> Optional[JobData]:
        """Create JobData from attributes"""
        try:
            # Get direct needs from data-needs attribute
            needs = attrs.needs.split(",") if attrs.needs else []
            needs = [need.strip() for need in needs]

            allow_failure = attrs.allow_failure == "true"
            order = ElementUtils.parse_job_order(attrs.style)
            return JobData(
                id=attrs.id.replace("job_", ""),
                name=attrs.text,
                needs=needs,
                allow_failure=allow_failure,
                order=order,
                stage=attrs.stage,
            )
        except Exception as e:
            self.logger.error(f"Error creating job data: {str(e)}")
            return None
