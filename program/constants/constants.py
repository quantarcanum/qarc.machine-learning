from decouple import config

ENV = "DEV"
#MODE = "PROD"

DATATRANSFER_API_ENDPOINT_DEV = "localhost bla bla"
DATATRANSFER_API_ENDPOINT_PROD = "quantarcanum.x/api"
DATATRANSFER_API_ENDPOINT = DATATRANSFER_API_ENDPOINT_PROD if ENV == "PROD" else DATATRANSFER_API_ENDPOINT_DEV

MONGO_CONNECTION_STRING_DEV = config("MONGO_CONNECTION_STRING_DEV")
MONGO_CONNECTION_STRING_PROD = config("MONGO_CONNECTION_STRING_PROD")
MONGO_CONNECTION_STRING = MONGO_CONNECTION_STRING_PROD if ENV == "PROD" else MONGO_CONNECTION_STRING_DEV

MONGO_QUANTARCANUM_DB = "QarcTickAndAggregatedDatastore"
MONGO_BAR_COLLECTION = "GuerrillaTrendRevBarCollection"