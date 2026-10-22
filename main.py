import os
import time
import hmac
import hashlib
import secrets
import re
import json
import logging
from collections import defaultdict
from typing import Any
from fastapi import FastAPI, Header, HTTPException, Depends, Request
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [SB61_CORE] - %(levelname)s - %(message)s")
logger = logging.getLogger("SB61NeuralSystem")

app = FastAPI(
    title="SB_61 Enterprise Unified Neural Security System",
    version="5.0.0",
    description="النظام الأمني العصبي الموحد المؤسسي - حماية فائقة بـ 3 طبقات أمان متقدمة"
)

SYSTEM_ENV = os.getenv("ENVIRONMENT", "production")
SECRET_SYSTEM_KEY = os.getenv("SECRET_KEY", secrets.token_hex(64)).encode('utf-8')
SKULL_CORE_TOKEN = os.getenv("SKULL_CORE_TOKEN", "SB61-SKULL-CORE-SECURE")

NEURAL_MEMORY_BLACKLIST = set()
REQUEST_COUNTER = defaultdict(list)
SUSPICION_MATRIX = defaultdict(int)

class UnifiedPayloadAnnihilator:
    FATAL_PATTERNS = [
        r"(?i)(\bunion\b\s+all\s+\bselect\b|\bselect\b.*?[:\s]+\bfrom\b.*?--|\bexec\s*\(|\bdrop\s+database\b)",
        r"(?i)(\bimport\s+os\b|\bos.system\b|\bsubprocess\b|\bexec\s*\(|\beval\s*\()",
        r"(?i)(<script.*?>|javascript:|onload\s=|onerror\s*=|document.cookie)",
        r"(?i)($where|\$gt|\$ne|\$regex|\$function|\$accumulator)"
    ]

    @classmethod
    def deep_inspect(cls, node: Any) -> bool:
        if isinstance(node, str):
            for pattern in cls.FATAL_PATTERNS:
                if re.search(pattern, node):
                    return True
        elif isinstance(node, dict):
            for k, v in node.items():
                if cls.deep_inspect(k) or cls.deep_inspect(v):
                    return True
        elif isinstance(node, list):
            for item in node:
                if cls.deep_inspect(item):
                    return True
        return False

def aaron_secure_response(data: dict, version_tag: str = "secured_by_sb61"):
    timestamp = str(time.time()).encode()
    payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
    signature = hmac.new(SECRET_SYSTEM_KEY, payload + timestamp, hashlib.sha512).hexdigest()
    return {
        "system_status": version_tag,
        "data": data,
        "signature": signature,
        "timestamp": timestamp.decode()
    }

def pharaoh_authorization_check(authorization: str = Header(...)):
    if not authorization.startswith("Bearer SB61-"):
        raise HTTPException(status_code=401, detail="[Pharaoh Control]: Unauthorized Corporate Access.")
    if authorization.startswith("Bearer SB61-SKULL-ADMIN-"):
        return "SKULL_SUPREME_ADMIN"
    elif authorization.startswith("Bearer SB61-SECURE-"):
        return "AUTHORIZED_ADMIN"
    raise HTTPException(status_code=401, detail="[Pharaoh Control]: Invalid security tier token.")

async def skull_gateway_dependency(request: Request, x_skull_token: str = Header(None), user_agent: str = Header(None)):
    client_ip = request.client.host if request.client else "unknown"
    if client_ip in NEURAL_MEMORY_BLACKLIST:
        raise HTTPException(status_code=403, detail="[Skull Shield]: IP Terminated & Banned.")
    if not x_skull_token or x_skull_token != SKULL_CORE_TOKEN:
        NEURAL_MEMORY_BLACKLIST.add(client_ip)
        raise HTTPException(status_code=401, detail="[Skull Shield]: Missing core neural token.")
    if not user_agent or any(bot in user_agent.lower() for bot in ["bot", "crawler", "spider", "sqlmap", "nmap"]):
        NEURAL_MEMORY_BLACKLIST.add(client_ip)
        raise HTTPException(status_code=403, detail="[Skull Shield]: Malicious scanner identified.")
    return True

@app.post("/sb61/api/v1/skull-secure-process")
async def endpoint_skull_tier(payload_data: dict, gate = Depends(skull_gateway_dependency), admin = Depends(pharaoh_authorization_check)):
    audit_log = f"Supreme Admin [{admin}] executed transaction via Skull Shield Tier."
    return aaron_secure_response({"message": "تمت معالجة الطلب بنجاح داخل تجويف درع الجمجمة.", "audit_trail": audit_log}, "PROTECTED_BY_SKULL_SHIELD_v5")

async def deep_sensory_dependency(request: Request, user_agent: str = Header(None)):
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()
    if client_ip in NEURAL_MEMORY_BLACKLIST:
        raise HTTPException(status_code=403, detail="[Yam Isolation]: Access Denied.")
    
    timestamps = REQUEST_COUNTER[client_ip]
    REQUEST_COUNTER[client_ip] = [t for t in timestamps if current_time - t < 60]
    if len(REQUEST_COUNTER[client_ip]) >= 60:
        SUSPICION_MATRIX[client_ip] += 2
        raise HTTPException(status_code=429, detail="[Yam Isolation]: Rate limit exceeded.")
    REQUEST_COUNTER[client_ip].append(current_time)
    
    try:
        body_bytes = await request.body()
        if body_bytes and UnifiedPayloadAnnihilator.deep_inspect(json.loads(body_bytes)):
            SUSPICION_MATRIX[client_ip] += 5
            raise HTTPException(status_code=400, detail="[Deep Threat Scanner]: Malicious vector detected.")
    except json.JSONDecodeError:
        pass

    if SUSPICION_MATRIX[client_ip] >= 5:
        NEURAL_MEMORY_BLACKLIST.add(client_ip)
        raise HTTPException(status_code=403, detail="[Yam Isolation]: Threshold reached. IP isolated.")
    return True

@app.post("/sb61/api/v1/deep-secure-process")
async def endpoint_deep_tier(payload_data: dict, gate = Depends(deep_sensory_dependency), admin = Depends(pharaoh_authorization_check)):
    audit_log = f"Admin [{admin}] executed transaction via Deep Sensory Tier."
    return aaron_secure_response({"message": "تم معالجة الطلب بنجاح عبر الفحص العميق.", "audit_trail": audit_log}, "PROTECTED_BY_DEEP_SENSORY_v5")

def standard_gateway(user_agent: str = Header(...)):
    if "Bot" in user_agent or "Malicious" in user_agent:
        raise HTTPException(status_code=403, detail="[Yam Isolation]: Access Denied.")
    return True

@app.post("/sb61/api/v1/standard-secure-process")
def endpoint_standard_tier(payload_data: dict, gate = Depends(standard_gateway), admin = Depends(pharaoh_authorization_check)):
    audit_log = f"User [{admin}] executed transaction via Standard Tier."
    return aaron_secure_response({"message": "تم معالجة الطلب المؤسسي بنجاح عبر البوابة الأساسية.", "audit_trail": audit_log}, "PROTECTED_BY_STANDARD_v5")

@app.get("/health")
def health_check():
    return {"status": "healthy", "system": "SB_61 Neural Security Engine", "environment": SYSTEM_ENV}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
