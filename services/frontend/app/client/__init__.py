import os

from .orchestrator import OrchestratorClient

host = os.getenv("ORCHESTRATOR_SERVICE_HOST", "localhost")
port = int(os.getenv("ORCHESTRATOR_SERVICE_PORT", "9600"))

orchestrator_client = OrchestratorClient(host, port)
