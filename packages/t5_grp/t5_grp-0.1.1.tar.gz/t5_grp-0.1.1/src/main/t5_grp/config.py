"""Configuration settings for the CI/CD pipeline visualization tool."""

# Asset related configurations
ASSET_FILES = ["main.css", "main.js", "favicon.ico"]
TEMPLATE_DIR_NAME = "templates"

# Template related configurations
TEMPLATE_FILE = "pipeline_template.html"

# Directory structure
PROJECT_ROOT = "t5_grp"
ASSETS_FOLDER = "assets"
TEMPLATES_FOLDER = "templates"
MAIN_FOLDER = "main"

# File paths will be joined with os.path.join in the code
ASSET_PATH_PREFIX = f"{PROJECT_ROOT}/{ASSETS_FOLDER}"


# Test configurations
TEST_OUTPUT_FILENAME = "test_output.html"
TEST_PIPELINE_NAME = "P1"

# Test file paths
TEST_FILES_DIR = "test_files"
TEST_YAML_FILE = "valid.yaml"
TEMP_HTML_FILE = "temp_output.html"

# Test data
TEST_STAGES = ["build", "test", "doc", "deploy"]
TEST_ARTIFACTS = {
    "build": ["build/classes/*", "build/reports/*"],
    "test": ["final.jar"],
    "deploy": ["distribution.tgz", "md5.sum"],
}

# HTML Element Classes
CSS_CLASSES = {
    "PIPELINE_DESCRIPTION": "pipeline-description",
    "PIPELINE_CONTAINER": "pipeline-container",
    "STAGES_CONTAINER": "stages-container",
    "STAGE": "stage",
    "STAGE_TITLE": "stage-title",
    "STAGE_CONTENT": "stage-content",
    "EMPTY_STAGE": "empty-stage",
    "JOB": "job",
    "JOB_NAME": "job-name",
    "JOB_STATUS": "job-status",
    "ARTIFACTS_BOX": "artifacts-box",
    "ARTIFACTS_TITLE": "artifacts-title",
    "ARTIFACTS_LIST": "artifacts-list",
    "ARROWS": "arrows",
}

# HTML Element IDs
ELEMENT_IDS = {"PIPELINE_TITLE": "pipeline-title"}

# HTML Tags
HTML_TAGS = {"LIST_ITEM": "li", "PATH": "path"}

# XPath Templates
XPATH_TEMPLATES = {
    "STAGE_TITLE": "//div[contains(@class, '{}')]",
    "STAGE_WITH_TEXT": "[contains(text(), '{}')]",
    "JOB_PREFIX": "job_",
    "DEPENDENCY_ARROW": "//path[@data-source='{}' and @data-target='{}']",
    "ARTIFACTS_TITLE": "//div[contains(@class, '{}')]",
    "ARTIFACTS_WITH_TEXT": "[contains(text(), '{} Artifacts')]",
    "ARTIFACTS_LIST": "/following-sibling::ul[@class='{}']/li",
}
