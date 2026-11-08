# CyberShield AI — Database Setup & Administration Guide

CyberShield AI uses **SQLAlchemy 2.0** as its Object Relational Mapper (ORM), with native support for **PostgreSQL** in production and automated seamless fallback to **SQLite** for zero-dependency local development and testing.

---

## 1. Quick Start: Local Development (Default)

CyberShield AI comes configured out of the box to run immediately without requiring a standalone database server.
If `DATABASE_URL` is omitted or set to SQLite, the backend automatically initializes an embedded database:
```env
DATABASE_URL=sqlite:///./cybershield.db
```
Tables and schema are automatically generated on application startup.

---

## 2. Production PostgreSQL Setup

### Step A: Install PostgreSQL
Ensure PostgreSQL 14+ is installed and running on your system, or provision a managed instance via [Neon](https://neon.tech), [Supabase](https://supabase.com), or AWS RDS.

### Step B: Create Database & User
In `psql` or pgAdmin:
```sql
CREATE DATABASE cybershield;
CREATE USER cybershield_user WITH ENCRYPTED PASSWORD 'StrongPassword123!';
GRANT ALL PRIVILEGES ON DATABASE cybershield TO cybershield_user;
```

### Step C: Configure Connection String
In `.env`:
```env
DATABASE_URL=postgresql://cybershield_user:StrongPassword123!@localhost:5432/cybershield
```

### Step D: Initialize Schema
You can either let CyberShield initialize tables automatically on start, or apply the production schema directly:
```bash
psql -U cybershield_user -d cybershield -f database/schema.sql
```

---

## 3. Database Schema Overview

```mermaid
erDiagram
    SCANS ||--o{ INTELLIGENCE_RESULTS : "produces"
    SCANS ||--|| RISK_REPORTS : "generates"
    SCANS ||--o{ SCAN_EVENTS : "logs"

    SCANS {
        string id PK
        string scan_type
        text target
        string status
        string risk_level
        int risk_score
        timestamp created_at
    }

    INTELLIGENCE_RESULTS {
        string id PK
        string scan_id FK
        string provider
        string indicator_type
        text indicator_value
        string status
        boolean matched
        boolean verified
        text reference
        text details
        timestamp first_seen
        timestamp last_seen
    }

    RISK_REPORTS {
        string id PK
        string scan_id FK
        text summary
        text evidence
        text recommendations
        string report_hash
        string verification_status
        text blockchain_tx
        timestamp created_at
    }

    SCAN_EVENTS {
        string id PK
        string scan_id FK
        string event_type
        text description
        timestamp created_at
    }
```

---

## 4. Maintenance & Backups

To back up the PostgreSQL database:
```bash
pg_dump -U cybershield_user -F c -b -v -f cybershield_backup.dump cybershield
```

To restore:
```bash
pg_restore -U cybershield_user -d cybershield -v cybershield_backup.dump
```
