"""CyberShield AI — Application Configuration

Loads settings from environment variables and provides a centralized,
strongly-typed configuration object for all backend services.
"""

from functools import lru_cache
import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load optional .env file from project root or backend directory
load_dotenv()


class Settings(BaseModel):
    """Application settings and configuration parameters."""

    app_name: str = "CyberShield AI API"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    environment: str = Field(
        default_factory=lambda: os.getenv("ENVIRONMENT", "development")
    )
    host: str = Field(default_factory=lambda: os.getenv("HOST", "127.0.0.1"))
    port: int = Field(default_factory=lambda: int(os.getenv("PORT", "8000")))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # CORS configuration
    cors_origins: List[str] = Field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
            ).split(",")
            if origin.strip()
        ]
    )

    # Scanner & Safety Limits (Member 1)
    scan_timeout_seconds: int = Field(
        default_factory=lambda: int(os.getenv("SCAN_TIMEOUT_SECONDS", "10"))
    )
    max_redirect_hops: int = Field(
        default_factory=lambda: int(os.getenv("MAX_REDIRECT_HOPS", "5"))
    )
    max_response_bytes: int = Field(
        default_factory=lambda: int(os.getenv("MAX_RESPONSE_BYTES", "1048576"))
    )

    # Threat Intelligence (Member 4)
    urlhaus_api_key: str = Field(
        default_factory=lambda: os.getenv("URLHAUS_API_KEY", "")
    )
    safe_browsing_api_key: str = Field(
        default_factory=lambda: os.getenv("SAFE_BROWSING_API_KEY", "")
    )

    # AI Scam Analysis (Member 2)
    ai_api_key: str = Field(default_factory=lambda: os.getenv("AI_API_KEY", ""))
    ai_model_name: str = Field(
        default_factory=lambda: os.getenv("AI_MODEL_NAME", "gemini-1.5-flash")
    )

    # Blockchain Registry (Member 3)
    blockchain_rpc_url: str = Field(
        default_factory=lambda: os.getenv("BLOCKCHAIN_RPC_URL", "http://127.0.0.1:8545")
    )
    registry_contract_address: str = Field(
        default_factory=lambda: os.getenv("REGISTRY_CONTRACT_ADDRESS", "")
    )
    blockchain_private_key: str = Field(
        default_factory=lambda: os.getenv("BLOCKCHAIN_PRIVATE_KEY", "") or os.getenv("DEPLOYER_PRIVATE_KEY", "")
    )
    blockchain_network: str = Field(
        default_factory=lambda: os.getenv("BLOCKCHAIN_NETWORK", "Hardhat Local (EVM 31337)")
    )

    # Persistence (Member 4)
    database_url: str = Field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./cybershield.db")
    )

    # API Security & Authentication (Member 1 / Member 4)
    api_auth_key: str = Field(
        default_factory=lambda: os.getenv("API_AUTH_KEY", "cybershield-auth-key-2026")
    )


@lru_cache()
def get_settings() -> Settings:
    """Return cached instance of application settings."""
    return Settings()

