from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import os

# Import the isolated components
from app.telemetry_adapter import TelemetryAdapter
from app.bucket_adapter import BucketAdapter
from app.pipeline_wrapper import TTVPipelineWrapper

# Initialize isolated dependencies
app = FastAPI(title="TTV Production Governed API Layer")
telemetry = TelemetryAdapter()
bucket = BucketAdapter()
pipeline = TTVPipelineWrapper()

# Assume startup context loads models safely
@app.on_event("startup")
async def startup_event():
    # Phase 3 mapping - Service load layer
    pipeline.load_model()
    print("Application Startup: Pipeline Initialized via Wrapper.")

# Schema validations (Governance constraints)
class GenerationRequest(BaseModel):
    prompt: str
    resolution: str = "1080p"
    force_failure: bool = False  # Used exclusively for the Failure Testing Phase 7

@app.post("/v1/generate")
async def generate_video(request: GenerationRequest):
    execution_id = str(uuid.uuid4())
    
    # Trace Start
    telemetry.emit_event("request_received", execution_id, {"prompt": request.prompt})
    
    # Phase 7 & Validation - Force failure to prevent bypass
    if not request.prompt or len(request.prompt.strip()) == 0:
        telemetry.emit_event("validation_failed", execution_id, {"error": "empty_prompt_rejected"})
        raise HTTPException(status_code=400, detail="A valid prompt is required for deterministic evaluation.")
        
    telemetry.emit_event("validation_passed", execution_id)
    
    # Execution
    local_output_path = f"/tmp/{execution_id}_output.mp4"
    if not os.path.exists("/tmp/"):
        os.makedirs("/tmp/", exist_ok=True) # Fallback if /tmp non standard Windows
        
    telemetry.emit_event("generation_started", execution_id)
    
    # Safe decoupled model generation execution logic replacing old mock structure
    success = pipeline.generate(request.prompt, local_output_path, force_failure=request.force_failure)
    
    # Ensure fail closed logic
    if not success:
        telemetry.emit_event("generation_failed", execution_id, {"reason": "inference_exception"})
        raise HTTPException(status_code=500, detail="Pipeline error executing real generation flow. (Fail-Closed).")

    telemetry.emit_event("generation_completed", execution_id)
    
    # Safe Storage Layer execution mapping
    final_artifact_path = bucket.store_artifact(execution_id, local_output_path)
    telemetry.emit_event("artifact_written", execution_id, {"artifact_path": final_artifact_path})
    
    return {
        "execution_id": execution_id,
        "status": "success",
        "artifact_path": final_artifact_path
    }
