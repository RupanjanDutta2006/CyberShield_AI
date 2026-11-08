"""CyberShield AI — AI Scam & Message Analysis Schemas

Shared contract for Member 2 (AI Developer & Scam Intelligence Engineer).
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class ObservedIndicator(BaseModel):
    """An individual social-engineering indicator identified in message content."""
    indicator: str = Field(..., description="Name/category of the observed indicator")
    evidence: str = Field(..., description="Quoted or summarized evidence from the input")
    reason: str = Field(..., description="Why this indicator is considered suspicious")


class ExtractedIndicators(BaseModel):
    """Digital artifacts extracted from submitted text."""
    urls: List[str] = Field(default_factory=list, description="Extracted URLs")
    domains: List[str] = Field(default_factory=list, description="Extracted domain names")
    emails: List[str] = Field(default_factory=list, description="Extracted email addresses")
    phone_numbers: List[str] = Field(default_factory=list, description="Extracted phone numbers")


class MessageAnalysisRequest(BaseModel):
    """Client request model for analyzing scam messages, emails, or SMS."""
    message_text: str = Field(
        ...,
        min_length=5,
        max_length=10000,
        description="Untrusted email, SMS, or notification text to analyze",
        examples=["URGENT: Your bank account is suspended. Verify your OTP at https://secure-bank-login.test immediately."]
    )
    sender_hint: Optional[str] = Field(
        default=None,
        max_length=256,
        description="Optional sender address or caller ID if available"
    )


class MessageAnalysisResponse(BaseModel):
    """Structured response contract returned by the AI Scam Analysis module."""
    category: str = Field(
        ...,
        description="Detected scam category (e.g. possible_phishing, credential_harvesting, impersonation)"
    )
    risk_level: str = Field(
        ...,
        description="AI suggested risk tier (e.g. low_risk, suspicious, high_risk)"
    )
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0 (if calibrated)"
    )
    observed_indicators: List[ObservedIndicator] = Field(
        default_factory=list,
        description="Specific social engineering indicators identified"
    )
    extracted_indicators: ExtractedIndicators = Field(
        default_factory=ExtractedIndicators,
        description="Structured indicators extracted for potential downstream URL investigation"
    )
    explanation: str = Field(
        ...,
        description="Plain-language, non-technical explanation grounded strictly in evidence"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable protective steps for the user"
    )
    limitations: List[str] = Field(
        default_factory=list,
        description="Explicit boundaries (e.g. text alone does not verify sender identity)"
    )
    analysis_mode: str = Field(
        default="HEURISTIC_ONLY",
        description="Mode of analysis: 'REAL_AI', 'HEURISTIC_ONLY', 'UNAVAILABLE', or 'FAILED' (B5-F04)"
    )

