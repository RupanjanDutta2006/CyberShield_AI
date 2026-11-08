"""CyberShield AI — API v1 Router

Registers core endpoints for API version 1.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.schemas.url_scan import (
    URLScanRequest,
    URLPreFlightResult,
    DNSInvestigationResult,
    RedirectAnalysisResult,
    TLSAnalysisResult,
    SecurityHeaderAnalysisResult,
    TechnicalInvestigationResult,
)
from app.schemas.ai_analysis import MessageAnalysisRequest, MessageAnalysisResponse
from app.schemas.blockchain import (
    ReportRegistrationRequest,
    ReportRegistrationResponse,
    ReportVerificationRequest,
    ReportVerificationResponse,
)
from app.schemas.threat_report import UnifiedThreatReport
from app.schemas.common import AnalysisStatus, ScanType
from app.services.url_investigation.service import investigate_url_preflight
from app.services.dns import investigate_dns
from app.services.redirects import trace_redirects
from app.services.tls_analysis import inspect_tls_certificate
from app.services.security_headers import fetch_and_analyze_security_headers
from app.services.technical_investigation import investigate_technical_website
from app.services.ai_analysis import analyze_scam_message
from app.services.threat_intelligence import lookup_threat_intelligence
from app.services.report_generator import assemble_unified_threat_report
from app.services.blockchain import (
    compute_canonical_report_hash,
    register_threat_report_on_chain,
    verify_threat_report_integrity,
)
from app.database import (
    get_db,
    save_threat_report,
    get_threat_report_by_id,
    list_threat_reports,
    get_total_report_count,
)
from app.core.security import require_api_auth

router = APIRouter()


class HealthCheckResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(default="healthy", description="Service health status")
    app_name: str = Field(default="CyberShield AI API", description="Application name")
    version: str = Field(default="1.0.0", description="API version")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Current UTC timestamp"
    )


class HistoryResponse(BaseModel):
    """Paginated report history response."""
    total: int = Field(..., description="Total persisted reports matching query")
    limit: int = Field(..., description="Page limit applied")
    offset: int = Field(..., description="Page offset applied")
    items: List[UnifiedThreatReport] = Field(default_factory=list, description="Report items")


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="API v1 Health Check",
    tags=["System"]
)
def api_v1_health() -> HealthCheckResponse:
    """Lightweight API v1 health check verifying service responsiveness.
    Does not depend on external AI, threat intel, or blockchain RPC services.
    """
    return HealthCheckResponse()


@router.post(
    "/scan-url",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    summary="Investigate URL / Domain (Early Security Gate Protected)",
    tags=["Investigation"]
)
def scan_url(request: URLScanRequest) -> Dict[str, Any]:
    """Endpoint stub for full live URL investigation.
    
    SECURITY GATE: In accordance with project Security Gate rules, live outbound
    URL scanning remains disabled until the multi-hop redirect and TLS inspection
    pipeline (Stage 3) is implemented and independently verified.
    
    For safe offline/preflight validation without outbound network requests,
    use POST /api/v1/url/preflight.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Outbound live URL scanning is intentionally gated and disabled under Security Gate rules. "
            "Full live URL scanning has not been approved for activation. "
            "Safe offline URL intake and SSRF preflight validation is available at /api/v1/url/preflight, "
            "and granular technical investigation is available at /api/v1/investigate/*."
        )
    )


@router.post(
    "/url/preflight",
    response_model=URLPreFlightResult,
    status_code=status.HTTP_200_OK,
    summary="URL Intake Preflight Investigation (Safe Local Validation)",
    tags=["Investigation"]
)
def url_preflight(request: URLScanRequest) -> URLPreFlightResult:
    """Execute safe pre-flight URL investigation (Batch 2: Parts 05–08).
    
    Performs intake validation, canonical normalization, SSRF/destination safety validation,
    and deterministic heuristic pattern analysis strictly locally without performing
    any outbound HTTP requests or web scraping.
    """
    return investigate_url_preflight(request.url)


# =============================================================================
# Stage 3 Technical Investigation Endpoints (Parts 09–12)
# =============================================================================

@router.post(
    "/investigate/dns",
    response_model=DNSInvestigationResult,
    status_code=status.HTTP_200_OK,
    summary="DNS & Domain Investigation (Part 09)",
    tags=["Technical Investigation"]
)
def investigate_dns_endpoint(request: URLScanRequest) -> DNSInvestigationResult:
    """Execute safe DNS and infrastructure investigation."""
    return investigate_dns(request.url)


@router.post(
    "/investigate/redirects",
    response_model=RedirectAnalysisResult,
    status_code=status.HTTP_200_OK,
    summary="Safe Redirect Chain Analysis (Part 10)",
    tags=["Technical Investigation"]
)
def investigate_redirects_endpoint(request: URLScanRequest) -> RedirectAnalysisResult:
    """Trace HTTP redirect chains with per-hop SSRF validation and verified-IP pinning."""
    return trace_redirects(request.url)


@router.post(
    "/investigate/tls",
    response_model=TLSAnalysisResult,
    status_code=status.HTTP_200_OK,
    summary="TLS & Certificate Trust Analysis (Part 11)",
    tags=["Technical Investigation"]
)
def investigate_tls_endpoint(request: URLScanRequest) -> TLSAnalysisResult:
    """Inspect HTTPS certificate validity, hostname matching, and cipher parameters."""
    return inspect_tls_certificate(request.url)


@router.post(
    "/investigate/headers",
    response_model=SecurityHeaderAnalysisResult,
    status_code=status.HTTP_200_OK,
    summary="HTTP Security Headers Analysis (Part 12)",
    tags=["Technical Investigation"]
)
def investigate_headers_endpoint(request: URLScanRequest) -> SecurityHeaderAnalysisResult:
    """Passively evaluate defensive HTTP security headers."""
    return fetch_and_analyze_security_headers(request.url)


@router.post(
    "/investigate/technical",
    response_model=TechnicalInvestigationResult,
    status_code=status.HTTP_200_OK,
    summary="Comprehensive Technical Website Investigation (Parts 09–12)",
    tags=["Technical Investigation"]
)
def investigate_technical_endpoint(request: URLScanRequest) -> TechnicalInvestigationResult:
    """Execute full Stage 3 technical pipeline coordinating DNS, redirects, TLS, and headers."""
    return investigate_technical_website(request.url)



@router.post(
    "/analyze-message",
    response_model=MessageAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze Scam Message (Part 18)",
    tags=["AI Analysis"]
)
def analyze_message_endpoint(request: MessageAnalysisRequest) -> MessageAnalysisResponse:
    """Analyze untrusted email, SMS, or notification text for social engineering cues."""
    return analyze_scam_message(request)


@router.get(
    "/scans/{scan_id}",
    response_model=UnifiedThreatReport,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Threat Report by ID (Part 17 / 19)",
    tags=["Investigation"],
    dependencies=[Depends(require_api_auth)],
)
def get_scan(scan_id: str, db: Session = Depends(get_db)) -> UnifiedThreatReport:
    """Retrieve an off-chain persisted Unified Threat Report by scan_id."""
    report = get_threat_report_by_id(db, scan_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Threat report with scan_id '{scan_id}' not found in database."
        )
    return report


@router.get(
    "/history",
    response_model=HistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Paginated Scan History (Part 17 / 19)",
    tags=["Persistence"],
    dependencies=[Depends(require_api_auth)],
)
def get_history(
    limit: int = Query(default=20, ge=1, le=100, description="Page size limit"),
    offset: int = Query(default=0, ge=0, description="Page offset"),
    classification: Optional[str] = Query(default=None, description="Filter by risk classification"),
    db: Session = Depends(get_db),
) -> HistoryResponse:
    """Retrieve paginated list of historically investigated threat reports."""
    reports = list_threat_reports(db, limit=limit, offset=offset, classification=classification)
    total = get_total_report_count(db, classification=classification)
    return HistoryResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=reports,
    )


@router.post(
    "/reports",
    response_model=UnifiedThreatReport,
    status_code=status.HTTP_200_OK,
    summary="Persist Threat Report Off-Chain (Part 17 / 19)",
    tags=["Persistence"],
    dependencies=[Depends(require_api_auth)],
)
def persist_report_endpoint(
    report: UnifiedThreatReport,
    db: Session = Depends(get_db),
) -> UnifiedThreatReport:
    """Persist a complete UnifiedThreatReport off-chain in the relational database."""
    try:
        canonical_hash = compute_canonical_report_hash(report)
        save_threat_report(db, report, canonical_hash=canonical_hash)
        persisted = get_threat_report_by_id(db, report.scan_id)
        return persisted or report
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database persistence failure: {exc}",
        )


@router.post(
    "/reports/investigate",
    response_model=UnifiedThreatReport,
    status_code=status.HTTP_200_OK,
    summary="Execute Full Coordinated Threat Investigation (Part 17 / 18 / 19)",
    tags=["Investigation"],
    dependencies=[Depends(require_api_auth)],
)
def investigate_and_generate_report(
    request: URLScanRequest,
    db: Session = Depends(get_db),
) -> UnifiedThreatReport:
    """Execute full safe coordinated investigation: preflight, technical, threat intel, and persist report."""
    # 1. URL Preflight & SSRF Safety
    preflight = investigate_url_preflight(request.url)

    # 2. If preflight indicates unsafe destination or invalid syntax, omit outbound network
    if not preflight.is_eligible_for_scan or not preflight.validation.is_valid:
        report = assemble_unified_threat_report(
            target=request.url,
            target_type=ScanType.URL,
            preflight=preflight,
            custom_limitations=["Outbound technical investigation omitted due to SSRF safety block or invalid syntax."],
        )
        try:
            canonical_hash = compute_canonical_report_hash(report)
            save_threat_report(db, report, canonical_hash=canonical_hash)
        except Exception as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database persistence failure: {exc}",
            )
        return report

    # 3. Technical Investigation (DNS, Redirects, TLS, Headers)
    technical = investigate_technical_website(request.url)

    # 4. Threat Intelligence Aggregation
    threat_intel = lookup_threat_intelligence(request.url)

    # 5. Assemble Master Report
    report = assemble_unified_threat_report(
        target=request.url,
        target_type=ScanType.URL,
        preflight=preflight,
        technical_investigation=technical,
        threat_intel=threat_intel,
    )

    # 6. Compute Canonical Hash and Persist
    try:
        canonical_hash = compute_canonical_report_hash(report)
        save_threat_report(db, report, canonical_hash=canonical_hash)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database persistence failure: {exc}",
        )

    return report


@router.post(
    "/reports/register",
    response_model=ReportRegistrationResponse,
    status_code=status.HTTP_200_OK,
    summary="Register Report Hash On-Chain (Part 19)",
    tags=["Blockchain"],
    dependencies=[Depends(require_api_auth)],
)
def register_report_endpoint(
    request: ReportRegistrationRequest,
    db: Session = Depends(get_db),
) -> ReportRegistrationResponse:
    """Commit canonical threat report hash to decentralized registry ledger."""
    try:
        return register_threat_report_on_chain(request, db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.post(
    "/reports/verify",
    response_model=ReportVerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify Report Integrity Against Blockchain (Part 19)",
    tags=["Blockchain"]
)
def verify_report_endpoint(
    request: ReportVerificationRequest,
    db: Session = Depends(get_db),
) -> ReportVerificationResponse:
    """Verify cryptographic integrity and tamper status of a report against the blockchain."""
    return verify_threat_report_integrity(request, db)

