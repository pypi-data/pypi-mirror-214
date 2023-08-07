PCS_SERVICE_NAME = "analytics/optimization"
QA_TOKEN_URL = "https://accounts-qa1.msci.com/oauth/token"
OMPS_AUDIENCE = "https://portfoliostore/api"
OMPS_FILE_PREFIX = "omps"

SDK_DIR = "msci_sdk"
TOKEN_FILE_NAME = "token.txt"

# QA environment details
PCS_QA = {
    # internal
    # "pcs_host": "qa-mos-otw.msciapps.com",
    # external
    "pcs_host": "test-api2.msci.com",
    "pcs_service_name": PCS_SERVICE_NAME,
    "pcs_version": "v1.3",
    "pcs_audience": "pcs-qa",
    "pcs_token_url": QA_TOKEN_URL
}

# QA environment details
PCS_DEV = {
    "pcs_host": "dev-mos-otw.msciapps.com",
    "pcs_service_name": PCS_SERVICE_NAME,
    "pcs_version": "v1.3",
    "pcs_audience": "pcs-qa",
    "pcs_token_url": QA_TOKEN_URL
}

# PROD environment details
PCS_PROD = {
    "pcs_host": "api2.msci.com",
    "pcs_service_name": PCS_SERVICE_NAME,
    "pcs_version": "v1.3",
    "pcs_audience": "https://pcs",
    "pcs_token_url": "https://accounts.msci.com/oauth/token"
}

# OMPS service
OMPS_QA = {
    # internal
    # "omps_base_url": "https://omps.portfolio-store-qa.k8s.msciapps.com/portfolio-service/api/v3.0",
    # external
    "omps_base_url": "https://test-api2.msci.com/analytics/portfolio-service/v3.0",
    "omps_token_url": QA_TOKEN_URL,
    "omps_audience": OMPS_AUDIENCE}

OMPS_DEV = {
    "omps_base_url": "https://test-api2.msci.com/analytics/portfolio-service/v3.0",
    "omps_token_url": QA_TOKEN_URL,
    "omps_audience": OMPS_AUDIENCE}

OMPS_PROD = {
    "omps_base_url": "https://api2.msci.com/analytics/portfolio-service/v3.0",
    "omps_token_url": "https://accounts.msci.com/oauth/token",
    "omps_audience": OMPS_AUDIENCE}

# Messages
NO_PREVIOUS_JOB_MESSAGE = 'No previous job available'
NO_TAX_OUTPUT_MESSAGE = 'No Tax Output to display'

# Error
PORTFOLIO_ID_AS_OF_DATE_ERROR = 'portfolio_id and as_of_date must be provided!'
