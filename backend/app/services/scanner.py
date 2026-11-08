import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict
from sqlalchemy.orm import Session

from backend.models.scan import Scan, IntelligenceResult, RiskReport, ScanEvent
from backend.schemas.scan import ScanDetailResponse, ScanEventSchema, RiskReportSchema
from backend.services.blockchain_verifier import ReportVerifier
from threat_intel.normalization import URLNormalizer
from threat_intel.providers.urlhaus import URLhausProvider
from threat_intel.providers.phishtank import PhishTankProvider
from threat_intel.services.reputation import ReputationAssessor
from threat_intel.services.normalizer import IndicatorNormalizer

logger = logging.getLogger("cybershield.scanner")


class ScannerService:
    @staticmethod
    async def scan_url(raw_target: str, db: Session) -> ScanDetailResponse:
        # 1. Normalize and Validate Target
        meta = URLNormalizer.normalize_target(raw_target)
        normalized_url = meta["normalized_url"]

        # 2. Create Initial Scan Entry
        scan = Scan(
            scan_type="url",
            target=raw_target,
            status="in_progress",
            risk_level="Unknown",
            risk_score=0
        )
        db.add(scan)
        db.flush()

        # Add initial audit events
        event1 = ScanEvent(
            scan_id=scan.id,
            event_type="normalization",
            description=f"Target validated and normalized to '{normalized_url}'."
        )
        db.add(event1)
        db.commit()

        # 3. Query Threat Intel Providers in parallel
        urlhaus = URLhausProvider()
        phishtank = PhishTankProvider()

        results = await asyncio.gather(
            urlhaus.query_url(normalized_url),
            phishtank.query_url(normalized_url),
            return_exceptions=True
        )

        indicators = []
        for r in results:
            if isinstance(r, Exception):
                logger.error(f"Provider query exception: {r}")
            else:
                indicators.append(r)

        # 4. Save Intelligence Results to Database
        db_indicators = []
        for ind in indicators:
            db_res = IntelligenceResult(
                scan_id=scan.id,
                provider=ind.provider,
                indicator_type=ind.indicator_type,
                indicator_value=ind.indicator_value,
                status=ind.status,
                matched=ind.matched,
                verified=ind.verified,
                reference=ind.reference,
                details=json.dumps(ind.details),
                first_seen=ind.first_seen,
                last_seen=ind.last_seen
            )
            db.add(db_res)
            db_indicators.append(db_res)

        db.add(ScanEvent(
            scan_id=scan.id,
            event_type="provider_query",
            description=f"Queried {len(indicators)} intelligence feeds ({', '.join(ind.provider for ind in indicators)})."
        ))
        db.flush()

        # 5. Aggregate Multi-Factor Risk Assessment
        assessment = ReputationAssessor.evaluate(meta, indicators)

        # 6. Generate Cryptographic Report Hash
        report_canonical_dict = ReportVerifier.build_canonical_payload(
            scan_id=scan.id,
            target=raw_target,
            risk_level=assessment.risk_level,
            risk_score=assessment.risk_score,
            summary=assessment.summary,
            evidence=assessment.evidence,
            recommendations=assessment.recommendations
        )

        report_hash = ReportVerifier.calculate_hash(report_canonical_dict)
        verification_status, tx_hash = await ReportVerifier.anchor_on_blockchain(report_hash)

        # 7. Store Risk Report
        report = RiskReport(
            scan_id=scan.id,
            summary=assessment.summary,
            evidence=json.dumps(assessment.evidence),
            recommendations=json.dumps(assessment.recommendations),
            report_hash=report_hash,
            verification_status=verification_status,
            blockchain_tx=tx_hash
        )
        db.add(report)

        # 8. Finalize Scan Record
        scan.status = "completed"
        scan.risk_level = assessment.risk_level
        scan.risk_score = assessment.risk_score

        db.add(ScanEvent(
            scan_id=scan.id,
            event_type="report_generation",
            description=f"Generated report with SHA-256 hash proof: {report_hash[:16]}..."
        ))
        db.commit()
        db.refresh(scan)
        db.refresh(report)

        # Return full response
        return ScanDetailResponse(
            scan_id=scan.id,
            scan_type=scan.scan_type,
            target=scan.target,
            normalized_target=normalized_url,
            domain=meta["domain"],
            hostname=meta["hostname"],
            status=scan.status,
            risk_level=scan.risk_level,
            risk_score=scan.risk_score,
            created_at=scan.created_at,
            providers_checked=IndicatorNormalizer.list_to_schema(indicators),
            report=RiskReportSchema(
                report_id=report.id,
                summary=report.summary,
                evidence=assessment.evidence,
                recommendations=assessment.recommendations,
                report_hash=report.report_hash,
                verification_status=report.verification_status,
                blockchain_tx=report.blockchain_tx,
                created_at=report.created_at
            ),
            events=[
                ScanEventSchema(
                    event_type=e.event_type,
                    description=e.description,
                    created_at=e.created_at
                ) for e in scan.events
            ]
        )
