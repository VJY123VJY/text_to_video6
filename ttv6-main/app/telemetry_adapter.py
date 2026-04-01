import logging
import json
from datetime import datetime
import os

class TelemetryAdapter:
    def __init__(self, log_file="artifacts/telemetry.log"):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.log_file = log_file
        
        # Configure logging
        self.logger = logging.getLogger("TTV_Telemetry")
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.INFO)
        self.logger.addHandler(fh)
    
    def emit_event(self, event_type: str, execution_id: str, metadata: dict = None):
        if metadata is None:
            metadata = {}
            
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "execution_id": execution_id,
            "metadata": metadata
        }
        
        log_line = json.dumps(event)
        self.logger.info(log_line)
        print(f"[TELEMETRY] {event_type} | {execution_id}")
