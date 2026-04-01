# ML Pipeline Integration Guide

## 1. Integrating ML Pipelines into API Services without Modifying Core
To integrate a core ML architecture into an active API service like FastAPI, we adopt the **Adapter-Wrapper Pattern**. The core principle is that the foundational ML codebase serves exclusively as a library or a submodule entirely decoupled from operational, API, or infrastructure logic.
- **Dependency Isolation**: Insert the unmodified ML repository as a submodule. Instead of modifying its files, dynamically append the module path (`sys.path.insert`) inside the wrapper.
- **Service Layering**: Define an intermediate interface (e.g., `pipeline_wrapper.py`) that abstracts exactly what the API expects. This prevents internal method signature changes in the ML repo from breaking the high-level API.
- **Immutability of Source**: Ensures any upstream improvements in the foundational ML repository can be merged cleanly via standard Git operations without creating complex branch conflicts.

## 2. Maintaining Fallback-Safe Integration Architecture
A fallback-safe (fail-closed) architecture ensures that system failures are gracefully handled without catastrophic propagation.
- **External Wrap Execution**: Never hook directly into side-effects of an ML system (e.g., direct S3 uploads from within ML code). Execute generation locally to `/tmp/`, evaluate if it was generated completely, and only then dispatch to adapters.
- **Fail-Closed Strategy**: Every functional block (validation, inference, storage) is isolated. If inference crashes due to Out-Of-Memory (OOM) or invalid tensors, the API immediately halts execution, logs context, and responds with a `500 Server Error`, rejecting any malformed artifact progression.
- **Health Checks & State Tracking**: Maintain initialization flags (`model_loaded`) independent of generating processes to avoid cascading request failures if the GPU restarts.

## 3. Ensuring Deterministic Telemetry in ML Systems
Telemetry acts as an unforgeable trace of operations mapping the lifecycle of an ML execution. 
- **Unique Trace IDs**: Assign a UUID string from the exact point the web server accepts the request (Edge point). 
- **Lifecycle Bound Events**: Guarantee a strict state machine of events logging: `request_received` -> `validation_passed` -> `generation_started` -> `generation_completed` -> `artifact_written`.
- **Structured JSON Logging**: Ensure all logged events are dumped consistently in JSON to enable robust ingestion pipelines (e.g., Elasticsearch or Datadog) to parse timestamp, execution ID, and operational metadata predictably.
- **No Missing Links**: Incorporate `try...except...finally` blocks strictly dispatching `generation_failed` on error, ensuring no orphaned request telemetry.
