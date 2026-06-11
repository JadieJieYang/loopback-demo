-- ============================================================
-- TABLE: da_approval_metrics
-- Owner: Data Analytics Team (DA)
-- Description: Analytical table that calculates approval rates
--              by product line, channel, and time period.
--              Built on top of raw_applications from Tech team.
-- ============================================================

CREATE TABLE da_approval_metrics AS
SELECT
    application_dt,
    product_type,                                   -- Joined from raw_applications
                                                    -- ROOT CAUSE: When product_type is NULL upstream,
                                                    -- this join drops the record entirely,
                                                    -- causing approve_rate to appear artificially low.
    channel,
    state,
    COUNT(app_id)                   AS total_apps,
    COUNT(CASE WHEN approve_flag = 1
               THEN app_id END)     AS approved_apps,

    -- approve_flag logic:
    -- An application is approved (1) when ALL of the following are true:
    --   1. credit_score > 700
    --   2. annual_income > 50000
    --   3. product_type IS NOT NULL        <-- fails when upstream feed is broken
    --   4. raw_status = 'APPROVED'
    -- Otherwise approve_flag = 0
    CASE
        WHEN credit_score > 700
         AND annual_income > 50000
         AND product_type IS NOT NULL
         AND raw_status = 'APPROVED'
        THEN 1
        ELSE 0
    END                             AS approve_flag,

    ROUND(
        COUNT(CASE WHEN approve_flag = 1 THEN app_id END) * 100.0
        / NULLIF(COUNT(app_id), 0),
    2)                              AS approve_rate_pct,

    CURRENT_TIMESTAMP               AS last_refreshed_at

FROM raw_applications
WHERE application_dt >= DATEADD(day, -90, CURRENT_DATE)
  AND product_type IS NOT NULL      -- WARNING: This filter silently excludes
                                    -- NULL product_type records instead of flagging them.
                                    -- This is what causes the 40% drop in BA's dashboard
                                    -- when upstream feed is broken.
GROUP BY
    application_dt,
    product_type,
    channel,
    state;

-- ============================================================
-- KNOWN ISSUE (2026-06-02 to 2026-06-08)
-- ============================================================
-- upstream raw_applications.product_type is NULL for 2,847 records
-- This table silently filters them out via WHERE product_type IS NOT NULL
-- Result: approve_rate_pct drops from ~65% to ~38% in BA dashboard
-- Fix needed: Data Engineering must backfill product_type for affected app_ids
-- ============================================================
