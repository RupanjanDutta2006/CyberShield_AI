import logging
from typing import Any, Dict, List, Optional
from backend.config import settings
from backend.schemas.scan import MessageIndicator
from backend.services.ai_engine import (
    AnalyzeMessageRequest,
    AnalyzeMessageResponse,
    CategoryEnum,
    IndicatorExtractor,
    MessageTypeEnum,
    RiskLevelEnum,
    ScamMessageAnalyzer,
)

logger = logging.getLogger("cybershield.message_analyzer")


class MessageAnalyzerService:
    """
    Analyzes suspicious messages (Email bodies, SMS, job offers, social engineering snippets).
    Employs Member 2's resilient AI engine featuring 3-tier failover
    (Groq -> Gemini -> OpenAI) with offline heuristic safety net and evidence grounding.
    """

    _analyzer: Optional[ScamMessageAnalyzer] = None

    @classmethod
    def get_analyzer(cls) -> ScamMessageAnalyzer:
        if cls._analyzer is None:
            cls._analyzer = ScamMessageAnalyzer()
        return cls._analyzer

    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extract deduplicated URLs from message text using safe regex."""
        return IndicatorExtractor.extract_urls(text)

    @classmethod
    async def analyze_message(cls, content: str) -> Dict[str, Any]:
        """
        Main analysis method invoked by API routes.
        Runs full analysis with LLM failover, prompt injection defense, and grounding.
        """
        analyzer = cls.get_analyzer()
        request = AnalyzeMessageRequest(message=content, message_type=MessageTypeEnum.OTHER)

        try:
            m2_response, engine_name = await analyzer.analyze(request)
        except Exception as exc:
            logger.error("Analysis raised unexpected exception: %s. Using safe fallback.", str(exc))
            extracted_data = IndicatorExtractor.extract_all(content)
            from backend.services.ai_engine.schemas import ExtractedIndicators
            m2_response, engine_name = analyzer._fallback_analysis(
                request=request,
                extracted=ExtractedIndicators(**extracted_data),
                injection_indicators=analyzer.detect_prompt_injections(content),
                fallback_reason=f"Exception recovery: {str(exc)}",
            )

        return cls._adapt_to_master_schema(m2_response, engine_name, content)

    @classmethod
    def _adapt_to_master_schema(
        cls,
        m2_resp: AnalyzeMessageResponse,
        engine_name: str,
        raw_content: str,
    ) -> Dict[str, Any]:
        """
        Maps Member 2's AnalyzeMessageResponse into the dictionary format
        required by CyberShield-AI's ScanDetailResponse and database models.
        """
        # 1. Map Risk Level & Calculate Quantitative Risk Score (0-100)
        conf = m2_resp.confidence
        risk_enum = m2_resp.risk_level

        if risk_enum == RiskLevelEnum.HIGH_RISK:
            if conf >= 0.85 or any("theft" in ind.indicator.lower() or "suspension" in ind.indicator.lower() for ind in m2_resp.observed_indicators):
                risk_level = "Critical"
                risk_score = min(98, 85 + int(conf * 13))
            else:
                risk_level = "High"
                risk_score = min(84, 72 + int(conf * 12))
        elif risk_enum == RiskLevelEnum.SUSPICIOUS:
            risk_level = "Medium"
            risk_score = min(69, 45 + int(conf * 24))
        elif risk_enum == RiskLevelEnum.LOW_RISK:
            risk_level = "Low"
            risk_score = max(5, int((1.0 - conf) * 20))
        else:
            risk_level = "Low"
            risk_score = 25

        # 2. Map Indicators to Master MessageIndicator list
        indicators: List[MessageIndicator] = []
        for ind in m2_resp.observed_indicators:
            name_lower = ind.indicator.lower()
            if any(k in name_lower for k in ["otp", "password", "credential", "arrest", "pin", "wire transfer", "prompt"]):
                severity = "Critical"
            elif any(k in name_lower for k in ["fee", "kyc", "urgency", "guaranteed", "suspension", "block"]):
                severity = "High"
            else:
                severity = "Medium"

            indicators.append(
                MessageIndicator(
                    category=ind.indicator,
                    severity=severity,
                    description=f'"{ind.evidence}" — {ind.reason}',
                )
            )

        if not indicators and risk_level in ["Critical", "High"]:
            indicators.append(
                MessageIndicator(
                    category="Threat Intent",
                    severity="High",
                    description=m2_resp.explanation,
                )
            )

        # 3. Build Forensic Evidence List
        evidence: List[str] = []
        for ind in m2_resp.observed_indicators:
            evidence.append(f'{ind.indicator}: "{ind.evidence}" ({ind.reason})')

        extracted = m2_resp.extracted_indicators
        if extracted.urls:
            evidence.append(f"Contains {len(extracted.urls)} embedded hyperlink(s): {', '.join(extracted.urls[:3])}")
        if extracted.phone_numbers:
            evidence.append(f"Contains contact telephone number(s): {', '.join(extracted.phone_numbers[:3])}")
        if extracted.emails:
            evidence.append(f"Contains contact email address(es): {', '.join(extracted.emails[:3])}")
        if extracted.domains:
            evidence.append(f"Referenced domain(s): {', '.join(extracted.domains[:3])}")

        evidence.append(f"Analysis synthesis: {m2_resp.explanation}")

        # 4. Summary
        summary = m2_resp.explanation
        if len(summary) > 300:
            summary = summary[:297] + "..."

        # 5. Recommendations
        recommendations = list(m2_resp.recommendations)
        if not recommendations:
            recommendations = [
                "Exercise caution with unsolicited messages.",
                "Verify the sender through an official, independent channel.",
            ]

        return {
            "engine": engine_name,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "summary": summary,
            "indicators": indicators,
            "evidence": evidence,
            "recommendations": recommendations,
            "extracted_urls": extracted.urls,
            "extracted_indicators": extracted.model_dump(),
            "detected_category": m2_resp.category.value,
            "confidence": m2_resp.confidence,
        }
