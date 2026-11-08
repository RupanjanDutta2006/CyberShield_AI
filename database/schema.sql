-- =============================================================================
-- CyberShield AI — PostgreSQL Database Schema
-- Production Relational Schema for Cyber Threat Intelligence & Detection
-- =============================================================================

-- Ensure UUID extension is available if running PostgreSQL natively
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table 1: Scans
-- Stores each scanning request (URL, Domain, Message)
CREATE TABLE IF NOT EXISTS scans (
    id VARCHAR(36) PRIMARY KEY,
    scan_type VARCHAR(32) NOT NULL, -- 'url', 'domain', 'message'
    target TEXT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'completed', -- 'completed', 'in_progress', 'failed'
    risk_level VARCHAR(32) NOT NULL DEFAULT 'Unknown', -- 'Critical', 'High', 'Medium', 'Low', 'Unknown'
    risk_score INTEGER DEFAULT 0, -- Calibrated score 0-100
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_scans_created_at ON scans(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_scans_risk_level ON scans(risk_level);
CREATE INDEX IF NOT EXISTS idx_scans_scan_type ON scans(scan_type);

-- Table 2: Intelligence Results
-- Stores granular responses received from each Threat Intelligence Provider
CREATE TABLE IF NOT EXISTS intelligence_results (
    id VARCHAR(36) PRIMARY KEY,
    scan_id VARCHAR(36) NOT NULL,
    provider VARCHAR(64) NOT NULL, -- 'URLhaus', 'PhishTank', 'Local Heuristics', 'AI Analyzer'
    indicator_type VARCHAR(64) NOT NULL, -- 'url', 'domain', 'keyword', 'phishing_pattern'
    indicator_value TEXT NOT NULL,
    status VARCHAR(32) NOT NULL, -- 'match_found', 'clean', 'not_configured', 'unavailable', 'error'
    matched BOOLEAN DEFAULT FALSE,
    verified BOOLEAN DEFAULT FALSE,
    reference TEXT,
    details TEXT, -- JSON-serialized dictionary of provider response fields
    first_seen TIMESTAMP WITH TIME ZONE,
    last_seen TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_intel_scan_id ON intelligence_results(scan_id);
CREATE INDEX IF NOT EXISTS idx_intel_provider ON intelligence_results(provider);
CREATE INDEX IF NOT EXISTS idx_intel_matched ON intelligence_results(matched);

-- Table 3: Risk Reports
-- Stores the final aggregated risk report, evidence list, recommendations, and cryptographic hash
CREATE TABLE IF NOT EXISTS risk_reports (
    id VARCHAR(36) PRIMARY KEY,
    scan_id VARCHAR(36) NOT NULL UNIQUE,
    summary TEXT NOT NULL,
    evidence TEXT NOT NULL, -- JSON-serialized array of evidence items
    recommendations TEXT NOT NULL, -- JSON-serialized array of remediation steps
    report_hash VARCHAR(64) NOT NULL, -- SHA-256 canonical hash of report
    verification_status VARCHAR(32) NOT NULL DEFAULT 'locally_hashed', -- 'locally_hashed', 'blockchain_pending', 'blockchain_verified', 'verification_failed'
    blockchain_tx TEXT, -- Transaction hash if anchored on-chain
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_reports_scan_id ON risk_reports(scan_id);
CREATE INDEX IF NOT EXISTS idx_reports_report_hash ON risk_reports(report_hash);
CREATE INDEX IF NOT EXISTS idx_reports_verification_status ON risk_reports(verification_status);

-- Table 4: Scan Events
-- Real-time audit log of scanning milestones for transparency and auditability
CREATE TABLE IF NOT EXISTS scan_events (
    id VARCHAR(36) PRIMARY KEY,
    scan_id VARCHAR(36) NOT NULL,
    event_type VARCHAR(64) NOT NULL, -- 'validation', 'normalization', 'provider_query', 'aggregation', 'hashing'
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_events_scan_id ON scan_events(scan_id);
