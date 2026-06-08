# Dashboard Blueprint

This document outlines the high-level architecture, interactivity mechanisms, and export requirements for the Bluestock Mutual Fund Analytics Platform Power BI Dashboard.

## Interactivity

### 1. Drill-through
*   **Target:** `Fund Detail View` (a hidden page in the report)
*   **Source:** The **Fund Scorecard Table** on the `Fund Performance` page.
*   **Behavior:** Users right-click on a specific scheme in the Fund Scorecard Table and select "Drill through > Fund Detail View" to see granular metrics, historical NAV trends, and portfolio composition for that specific fund.

### 2. Tooltips
*   **Implementation:** Custom report page tooltips should be utilized to provide more context without cluttering the main visuals.
*   **Target Visuals:** All charts across the dashboard.
*   **Content:**
    *   **Bar/Line Charts:** Show precise values, Month-over-Month (MoM) % change, and related metrics.
    *   **Scatter Plots:** Display the Scheme Name, Fund House, exact Risk Category, X/Y coordinate values, and Bubble Size (AUM).

### 3. Cross-filtering
*   **Behavior:** By default, visual interactions should be set to "Cross-filter" rather than "Highlight" to clearly isolate data segments.
*   **Example:** Clicking on the "SBI Mutual Fund" bar in the *AUM by Fund House* chart will filter all other visuals on the `Industry Overview` page to show metrics specifically for SBI Mutual Fund.

### 4. Sync Slicers
*   **Target Slicers:** `Year`, `Fund House`, and `Category`.
*   **Behavior:** Enable Sync Slicers across applicable pages (e.g., `Industry Overview`, `Fund Performance`, and `SIP & Market Trends`) so that user filter selections persist seamlessly as they navigate through the dashboard.

### 5. Navigation Buttons
*   **Implementation:** Implement a customized navigation pane (usually on the left side or top header).
*   **Elements:** Use distinct icons and text labels for:
    *   Industry Overview
    *   Fund Performance
    *   Investor Analytics
    *   SIP & Market Trends
*   **States:** Configure Default, Hover, and Selected states to provide visual feedback to the user.

---

## Export Requirements

To support executive reporting and presentations, the dashboard must be configured to support seamless export functionality.

### 1. Export Dashboard to PDF
*   Ensure that page sizes are standardized (16:9 ratio, typically 1280x720 pixels).
*   Ensure background colors and text contrasts are optimized for readability in print/PDF formats.
*   All pages should be exportable using the native "Export to PDF" feature in Power BI Service/Desktop.

### 2. Export Pages to PNG
*   Stakeholders require high-quality snapshot images of the views for slide decks. The dashboard pages must cleanly export to the following PNG file names:
    *   `Industry_Overview.png`
    *   `Fund_Performance.png`
    *   `Investor_Analytics.png`
    *   `SIP_Market_Trends.png`
*   **Constraint Checklist for PNG Export:**
    *   Ensure no scrollbars are active on vital visuals before snapshot.
    *   Ensure all slicers are set to default/desired states.
    *   Remove any active tooltip hovers.
