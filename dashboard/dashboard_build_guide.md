# Dashboard Build Guide

This implementation guide outlines the sequential steps required to build the Bluestock Mutual Fund Analytics Platform Power BI dashboard from the ground up, ensuring best practices and data integrity.

## 1. Import Process
1.  **Launch Power BI Desktop:** Create a new `.pbix` file.
2.  **Get Data:**
    *   Select `Get Data > SQLite` (using ODBC driver if querying `bluestock_mf.db` directly) OR select `Get Data > Text/CSV` if loading from the `data/processed/` directory.
    *   Import all necessary dimension and fact tables defined in `powerbi_data_model.md`.
3.  **Power Query Editor:**
    *   Promote headers, fix data types (ensure dates are `Date` type, monetary values are `Decimal/Fixed Decimal`).
    *   Rename query tables to match the naming convention (`dim_fund`, `fact_nav`, etc.).
    *   Apply any necessary pre-filtering (e.g., removing null AMFI codes if invalid).
    *   Click **Close & Apply**.

## 2. Relationship Creation
1.  Navigate to the **Model View** tab.
2.  Ensure `dim_date` is marked as a Date Table (Right-click table > Mark as date table > Select the date column).
3.  Build relationships strictly following the specifications in `powerbi_data_model.md`.
4.  Ensure all relationships between `dim_` tables and `fact_` tables are **One-to-Many (*:1)** with a **Single** cross-filter direction.
5.  Hide primary key columns in the fact tables from the report view (e.g., hide `amfi_code` in `fact_nav`) to force users to filter via dimension tables.

## 3. DAX Setup
1.  Create a dedicated table for measures to keep the data pane organized (Enter Data > Create blank table called `_Key Measures`).
2.  Navigate to the **Data View** or **Report View**.
3.  Copy and paste the DAX formulas provided in `dax_measures.md` into new measures under the `_Key Measures` table.
4.  Format the measures appropriately:
    *   Currency metrics: ₹ symbol, 0 or 2 decimal places.
    *   Ratios/Percentages: % symbol, 2 decimal places.
    *   Counts: Whole numbers with thousand separators.

## 4. Visual Creation Order
Build the dashboard following this sequence to ensure consistent layout and interactivity:
1.  **Base Layout:** Create the first page (`Industry Overview`). Add a background rectangle or import a custom background image if applicable. Add the Title header and the Navigation panel.
2.  **KPIs & Slicers:** Add the top KPI cards and the page slicers first. Ensure slicer interactions are set correctly (Format > Edit interactions).
3.  **Charts:** Build visual A, B, C, D as defined in `page_layout_specs.md`.
4.  **Duplication:** Duplicate the first page 3 times to create Pages 2, 3, and 4. This preserves the layout, navigation, and synced slicers.
5.  **Page Specifics:** Modify the visuals on the duplicated pages to match the specs for Fund Performance, Investor Analytics, and SIP Trends.
6.  **Tooltips:** Create a hidden page named `Tooltip_Base`, design the tooltip visuals, and assign this page as the tooltip source for the main charts.

## 5. Formatting Instructions
1.  **Theme Application:** Navigate to View > Themes > Browse for themes > select `powerbi_theme.json`.
2.  **Standardization:**
    *   Remove background from individual charts (let the page background show through).
    *   Ensure all chart titles are Left-Aligned, 14pt, Fintech Blue color.
    *   Turn off X and Y axis titles if the chart title is sufficiently descriptive.
    *   Standardize padding/margins for all visuals.

## 6. Final QA Checklist
- [ ] Do the KPI totals match the source data verification scripts?
- [ ] Does clicking on "SBI Mutual Fund" in the bar chart cross-filter the treemap and donut chart correctly?
- [ ] Does the `dim_date` date hierarchy work correctly in the line charts?
- [ ] Are Sync Slicers working when moving from Page 1 to Page 2?
- [ ] Is the "Drill-through" functionality working from the Fund Scorecard to the Detail View?
- [ ] Can the dashboard be exported cleanly to PDF without UI clipping?
