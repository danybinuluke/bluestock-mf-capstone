# Page Layout Specifications

This document outlines the detailed visual specifications for each page of the Bluestock Mutual Fund Analytics Platform.

---

## PAGE 1: INDUSTRY OVERVIEW

**Title:** Industry Overview

**Required Filters (Slicers):**
*   Year
*   Fund House

### KPI Cards
1.  **Total AUM**
    *   *Metric:* `[Total AUM]`
    *   *Target Line/Value:* ₹81 Lakh Crore
2.  **SIP Inflows**
    *   *Metric:* `[Total SIP Inflow]`
    *   *Target Line/Value:* ₹31,002 Cr
3.  **Total Folios**
    *   *Metric:* `[Total Folios]`
    *   *Target Line/Value:* 26.12 Cr
4.  **Total Schemes**
    *   *Metric:* `[Total Schemes]`
    *   *Target Line/Value:* 1908

### Charts
*   **A. Industry AUM Trend (2022–2025)**
    *   *Visual Type:* Line Chart
    *   *X-Axis:* Year/Month (`dim_date`)
    *   *Y-Axis:* Total AUM
*   **B. AUM by Fund House**
    *   *Visual Type:* Bar Chart
    *   *Y-Axis:* Fund House
    *   *X-Axis:* Total AUM
    *   *Formatting Requirement:* Highlight "SBI Mutual Fund" bar with a distinct color (e.g., Emerald Green) while others remain standard Fintech Blue.
*   **C. Fund Category Distribution**
    *   *Visual Type:* Treemap
    *   *Category:* Category (`dim_fund`)
    *   *Values:* Total AUM (or Total Schemes)
*   **D. Risk Category Distribution**
    *   *Visual Type:* Donut Chart
    *   *Legend:* Risk Category (`dim_fund`)
    *   *Values:* Total AUM

---

## PAGE 2: FUND PERFORMANCE

**Title:** Fund Performance & Risk

**Required Slicers:**
*   Fund House
*   Category
*   Plan (e.g., Direct, Regular)

### Visuals
*   **A. Risk vs Return Scatter Plot**
    *   *Visual Type:* Scatter Plot
    *   *X-Axis:* 3-Year Return
    *   *Y-Axis:* Std Dev
    *   *Bubble Size:* AUM
    *   *Color / Legend:* Risk Category
*   **B. Fund Scorecard Table**
    *   *Visual Type:* Table (Sortable)
    *   *Columns:* Scheme, Sharpe, Sortino, Alpha, Beta, Score
*   **C. NAV vs Benchmark Comparison**
    *   *Visual Type:* Line Chart
    *   *X-Axis:* Date (`dim_date`)
    *   *Y-Axis:* NAV (Normalized) / Cumulative Return
    *   *Legend lines:* Specific Fund, Nifty 50, Nifty 100
*   **D. Alpha vs Beta Matrix**
    *   *Visual Type:* Scatter Plot
    *   *X-Axis:* Beta
    *   *Y-Axis:* Alpha
    *   *Details:* Scheme Name

---

## PAGE 3: INVESTOR ANALYTICS

**Title:** Investor Analytics

**Required Slicers:**
*   State
*   Age Group
*   City Tier

### Visuals
*   **A. Transaction Amount by State**
    *   *Visual Type:* Horizontal Bar Chart
    *   *Y-Axis:* State
    *   *X-Axis:* Total Transaction Amount
*   **B. Transaction Type Split**
    *   *Visual Type:* Donut Chart
    *   *Legend:* Transaction Type (SIP vs Lumpsum vs Redemption)
    *   *Values:* Amount
*   **C. Age Group vs Average SIP Amount**
    *   *Visual Type:* Column / Bar Chart
    *   *X-Axis:* Age Group
    *   *Y-Axis:* Average SIP Amount
*   **D. Monthly Transaction Volume**
    *   *Visual Type:* Line Chart
    *   *X-Axis:* Month/Year (`dim_date`)
    *   *Y-Axis:* Count of Transactions
*   **E. City Tier Distribution**
    *   *Visual Type:* Donut Chart
    *   *Legend:* City Tier (Tier 1, Tier 2, Tier 3)
    *   *Values:* Investor Count / Total Amount

---

## PAGE 4: SIP & MARKET TRENDS

**Title:** SIP & Market Trends

**Required Filters (Slicers):**
*   Year
*   Category

### Visuals
*   **A. SIP Inflow vs Market Performance (2022-2025)**
    *   *Visual Type:* Line and Clustered Column Chart (Dual Axis)
    *   *X-Axis:* Date (`dim_date`)
    *   *Column / Primary Y-Axis:* SIP Inflow
    *   *Line / Secondary Y-Axis:* Nifty 50 Index Value
*   **B. Category Inflow Heatmap**
    *   *Visual Type:* Matrix
    *   *Rows:* Fund Category
    *   *Columns:* Quarter/Month
    *   *Values:* SIP Inflow (with Background Color Conditional Formatting based on value)
*   **C. Top 5 Categories by Net Inflow**
    *   *Visual Type:* Bar Chart
    *   *Y-Axis:* Top 5 Categories
    *   *X-Axis:* Net Inflow (Inflows - Redemptions)
*   **D. Benchmark Comparison**
    *   *Visual Type:* Line Chart
    *   *X-Axis:* Date
    *   *Y-Axis:* Average Return
    *   *Legend:* Benchmark Index vs Average Category Return
