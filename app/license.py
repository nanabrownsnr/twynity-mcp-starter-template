import asyncio
import sys
import uuid
from logging import getLogger

import httpx
from jose import jwt

from app.config import settings

LICENSE_SERVER_URL = settings.LICENSE_SERVER_BASE_URL.rstrip("/")
JWKS_ENDPOINT = settings.LICENSE_SERVER_JWKS_ENDPOINT.lstrip("/")
ACTIVATION_ENDPOINT = settings.LICENSE_SERVER_ACTIVATION_ENDPOINT.lstrip("/")
JWKS_URL = f"{LICENSE_SERVER_URL}/{JWKS_ENDPOINT}"
LICENSE_ACTIVATION_URL = f"{LICENSE_SERVER_URL}/{ACTIVATION_ENDPOINT}"


logger = getLogger(__name__)



def get_device_id() -> str:
    """Return MAC address as a 12-character hex string (device fingerprint)."""
    mac = uuid.getnode()
    return f"{mac:012x}"

async def get_jwks() -> list[dict]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(JWKS_URL)
        resp.raise_for_status()
        return resp.json()["keys"]

def get_public_key(jwks: list[dict], kid: str) -> dict:
    for jwk in jwks:
        if jwk["kid"] == kid:
            return jwk
    raise Exception("Key not found")

async def decode_license_token(token: str) -> dict:
    """Fetch JWKS and decode + verify the signed activation token."""
    jwks = await get_jwks()
    header = jwt.get_unverified_header(token)
    key = get_public_key(jwks, header["kid"])
    logger.info(f"Using key kid={header['kid']}")
    return jwt.decode(token, key, algorithms=[header["alg"]])

async def get_license_activation_token(license_key: str, device_id: str, service_id: str) -> str | None:
    """Request a signed activation token from the License Server.
    Args:
    license_key: The license key for this deployment.
    device_id:
    MAC-based device fingerprint.
    service_id: The SERVICE_ID from config (must match issuer config).
    Returns:
    Signed JWT string, or None if the server rejected the request.
    """
    activation_data = {
        "device_id": device_id,
        "license_key": license_key,
        "service_id": service_id,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(LICENSE_ACTIVATION_URL, json=activation_data)
        if response.status_code == 200:
            return response.json()["activation_token"]
        return None


async def validate_license(license_key: str, service_id: str, device_id: str) -> bool:
    """Activate and validate the license.
    Returns True only when the activation token is valid and
    its service_id + device_id match the local values.
    """
    activation_token = await get_license_activation_token(license_key, device_id, service_id)
    if not activation_token:
        return False
    try:
        data = await decode_license_token(activation_token)
        if data["service_id"] != service_id:
            return False
        if data["device_id"] != device_id:
            return False
    except Exception as e:
        logger.error(f"Invalid activation token: {e}")
        return False
    return True


def shutdown():
    """Terminate the process — uvicorn exits cleanly on sys.exit(1)."""
    sys.exit(1)



async def license_watcher(interval_seconds: float = 86400, max_failures: int = 14):
    """Background task: periodically validate the license.
    Runs forever. On each iteration:
    - Pass -> reset failure_count, log success.
    - Fail -> increment failure_count, warn.
    - failure_count >= max_failures -> log error, call shutdown().
    The 14-failure / 24-hour default gives ~2 weeks of grace
    when the License Server is temporarily unreachable.
    """
    failure_count = 0
    while True:
        try:
            valid = await validate_license(settings.LICENSE_KEY, settings.SERVICE_ID, get_device_id())
            if valid:
                failure_count = 0
                logger.info("License check passed.")
            else:
                failure_count += 1
                logger.warning(f"License check failed ({failure_count}/{max_failures}).")
                if failure_count >= max_failures:
                    logger.error("Max failures reached. Shutting down...")
                    shutdown()
                    break
        except Exception as e:
            failure_count += 1
            logger.error(f"License server unreachable: {e}. ({failure_count}/{max_failures})")
            if failure_count >= max_failures:
                logger.error("Max failures reached. Shutting down...")
                shutdown()
                break
        await asyncio.sleep(interval_seconds)
