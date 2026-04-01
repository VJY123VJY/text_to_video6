# 🎬 TTV Governed Pipeline System

A production-grade **Text-to-Video (TTV) pipeline system** with strict governance, deterministic execution, telemetry logging, and non-bypassable architecture.

---

## 🚀 Overview

This project integrates a real ML-based video generation pipeline into a **governed execution system** that ensures:

- ✅ No direct pipeline access  
- ✅ Controlled execution via wrapper  
- ✅ Full telemetry tracking  
- ✅ Deterministic validation  
- ✅ Fail-closed system behavior  

---

## 🧠 System Architecture

User Request  
↓  
API Layer (FastAPI)  
↓  
Validation Layer  
↓  
TTVPipelineWrapper (Governance Layer)  
↓  
Core TTV Pipeline (Shashank)  
↓  
Artifact Generation (.mp4)  
↓  
Telemetry Logging  

---

## 📂 Project Structure

project/  
│  
├── app/  
│   ├── main.py                # Entry point (FastAPI app)  
│   ├── routes/  
│   │   └── generate.py        # API endpoint  
│   ├── services/  
│   │   └── pipeline_service.py  
│   ├── wrapper/  
│   │   └── ttv_wrapper.py     # Governance wrapper  
│   ├── telemetry/  
│   │   └── logger.py          # Logging system  
│  
├── pipeline/  
│   └── shashank_ttv.py        # Core ML pipeline (unchanged)  
│  
├── artifacts/  
│   └── *.mp4                  # Generated videos  
│  
├── logs/  
│   └── telemetry.log          # Execution logs  
│  
├── REVIEW_PACKET.md           # Submission proof (mandatory)  
└── README.md  

---

## ⚙️ Features

- 🔒 **Governed Execution**
  - Pipeline can only run via `TTVPipelineWrapper`
  - Direct access is restricted

- 📊 **Telemetry Tracking**
  - request_received  
  - validation_started  
  - validation_passed / failed  
  - generation_started  
  - generation_completed / failed  
  - artifact_written  

- 🎥 **Real Artifact Generation**
  - Outputs `.mp4` files in `/artifacts`

- ❌ **Fail-Closed System**
  - Invalid requests are blocked early
  - No silent failures

- 🧪 **Failure Handling**
  - Missing fields  
  - Invalid inputs  
  - Pipeline errors  

---

## 🛠️ Installation

```bash
git clone <repo-url>
cd project
pip install -r requirements.txt
```

---

## ▶️ Run the System

```bash
uvicorn app.main:app --reload
```

---

## 📡 API Usage

### Endpoint:
POST /generate

### Request Example:
```json
{
  "prompt": "Krishna and Arjuna on battlefield",
  "quality": "high",
  "fps": 24,
  "resolution": "1080p"
}
```

### Response Example:
```json
{
  "status": "success",
  "execution_id": "exec_12345",
  "artifact_path": "artifacts/video_12345.mp4"
}
```

---

## 📜 Telemetry Logs Example

```
[INFO] request_received | execution_id=exec_12345
[INFO] validation_started | execution_id=exec_12345
[INFO] validation_passed | execution_id=exec_12345
[INFO] generation_started | execution_id=exec_12345
[INFO] generation_completed | execution_id=exec_12345
[INFO] artifact_written | path=artifacts/video_12345.mp4
```

---

## 🔐 Governance Rules

- ❌ Direct pipeline execution is NOT allowed  
- ✅ Only `TTVPipelineWrapper` can trigger generation  
- ❌ Any bypass attempt must fail  

---

## 🧪 Testing

### Valid Test
- Proper request → video generated  

### Failure Tests
- Missing prompt → validation failed  
- Invalid params → rejected  
- Forced pipeline error → execution failed  

---

## 📦 Output

- 🎥 `.mp4` video file  
- 📄 Telemetry logs  
- 🆔 Execution ID for tracking  

---

## 📌 Important

This project is built under strict review protocol:

- Claims are NOT accepted  
- Only logs + JSON + artifacts = proof  

---

## 👨‍💻 Contributors

- Soham Kotkar — Pipeline Validation  
- Ishan Shirode — Governance Validation  
- Siddhant Kale — DevOps Execution  
- Vinayak Tiwari — Testing Protocol  

---

## 📄 License

This project is for educational and evaluation purposes.
