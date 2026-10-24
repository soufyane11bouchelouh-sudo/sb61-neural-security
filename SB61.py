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
    title="SB61 Enterprise Unified Neural Security System",
    version="5.0.0",
    description="النظام الأمن العصبي الموحد - دمج طبقات الحماية الحقيقية مع الهيكل المعماري المعرفي."
)

SYSTEM_ENV = os.getenv("ENVIRONMENT", "production")
SECRET_SYSTEM_KEY = os.getenv("SECRET_KEY", secrets.token_hex(64)).encode('utf-8')
SKULL_CORE_TOKEN = os.getenv("SKULL_CORE_TOKEN", "SB61-SKULL-CORE-SECURE")

NEURAL_MEMORY_BLACKLIST = set()
REQUEST_COUNTER = defaultdict(list)
SUSPICION_MATRIX = defaultdict(int)

class UnifiedPayloadAnnihilator:
    FATAL_PATTERNS = [
        r"(?i)(\bunion\b|\ball\b|\bselect\b|\binsert\b|\bdelete\b|\bexec\b|(\bdrop\s+database\b))",
        r"(?i)(\bimport\b|\bos\b|\bsystem\b|\bsubprocess\b|\beval\b|\bexec\b)",
        r"(?i)(<script.*?>|javascript:|onload=|onerror=|\bdocument\.cookie\b)",
        r"(?i)(\bwhere\b|\bgt\b|\ble\b|\bregex\b|\bfunction\b|\baccumulator\b)"
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
    timestamp = str(time.time()).encode('utf-8')
    payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
    signature = hmac.new(SECRET_SYSTEM_KEY, payload + timestamp, hashlib.sha512).hexdigest()
    return {
        "system_status": version_tag,
        "data": data,
        "signature": signature,
        "timestamp": timestamp.decode('utf-8')
    }

def pharaoh_authorization_check(authorization: str = Header(...)):
    if not authorization.startswith("Bearer SB61-"):
        raise HTTPException(status_code=401, detail="Pharaoh Control: Unauthorized Corporate Access.")
    if authorization.startswith("Bearer SB61-SKULL-ADMIN"):
        return "SKULL_SUPREME_ADMIN"
    elif authorization.startswith("Bearer SB61-SECURE"):
        return "AUTHORIZED_ADMIN"
    raise HTTPException(status_code=401, detail="Pharaoh Control: Invalid security tier token.")

def skull_neural_shield_gate(x_skull_token: str = Header(...), user_agent: str = Header(...)):
    if x_skull_token != SKULL_CORE_TOKEN:
        raise HTTPException(status_code=403, detail="Skull Shield Violation: Invalid Core Token.")
    if "SB61-Client" not in user_agent and "Mozilla" not in user_agent and "Postman" not in user_agent:
        raise HTTPException(status_code=403, detail="Skull Shield Violation: Unverified User-Agent Signature.")
    return True

@app.middleware("http")
async def neural_firewall_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    if client_ip in NEURAL_MEMORY_BLACKLIST:
        raise HTTPException(status_code=403, detail="Neural Blacklist: Access Denied.")
        
    now = time.time()
    REQUEST_COUNTER[client_ip] = [t for t in REQUEST_COUNTER[client_ip] if now - t < 60]
    REQUEST_COUNTER[client_ip].append(now)
    
    if len(REQUEST_COUNTER[client_ip]) > 60:
        NEURAL_MEMORY_BLACKLIST.add(client_ip)
        logger.warning(f"IP {client_ip} added to Neural Blacklist due to Rate Limit Violation.")
        raise HTTPException(status_code=429, detail="Neural Firewall: Rate limit exceeded.")
        
    response = await call_next(request)
    return response

@app.post("/sb61/api/v1/skull-secure-process")
async def skull_tier_process(
    payload: dict,
    auth_tier: str = Depends(pharaoh_authorization_check),
    shield_passed: bool = Depends(skull_neural_shield_gate)
):
    if UnifiedPayloadAnnihilator.deep_inspect(payload):
        raise HTTPException(status_code=400, detail="Skull Shield Threat Detected: Malicious Payload Vector Identified.")
        
    response_content = {
        "message": "تم معالجة الطلب المؤسسي السيادي بنجاح تحت حماية درع Skull الخارق.",
        "security_level": "SKULL_SUPREME",
        "auth_role": auth_tier
    }
    return aaron_secure_response(response_content, "PROTECTED_BY_SKULL_SHIELD_v5")

@app.post("/sb61/api/v1/deep-secure-process")
async def deep_tier_process(
    payload: dict,
    auth_tier: str = Depends(pharaoh_authorization_check)
):
    if UnifiedPayloadAnnihilator.deep_inspect(payload):
        raise HTTPException(status_code=400, detail="Deep Inspection Alert: Dangerous Payload Rejected.")
        
    response_content = {
        "message": "تمت معالجة الطلب بنجاح عبر طبقة الفحص العميق.",
        "security_level": "DEEP_INSPECTION",
        "auth_role": auth_tier
    }
    return aaron_secure_response(response_content, "PROTECTED_BY_DEEP_SHIELD_v5")

@app.post("/sb61/api/v1/standard-secure-process")
async def standard_tier_process(payload: dict):
    if UnifiedPayloadAnnihilator.deep_inspect(payload):
        raise HTTPException(status_code=400, detail="Standard Guard Alert: Invalid Payload Structure.")
        
    response_content = {
        "message": "تمت معالجة الطلب بنجاح عبر البوابة القياسية المتوازنة."
    }
    return aaron_secure_response(response_content, "PROTECTED_BY_STANDARD_v5")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
