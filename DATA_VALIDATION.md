# Data validation and recruiter readiness

Checked November 13, 2026 against main commit `2a0b6f0553ca72c638cab562ba314971039d37c9`. The findings below come from static inspection of `data.py`, the documentation, and a limited desktop check of the hosted app. They do not establish the cause of any upstream error.

## Dependency compatibility

The first November 13, 2026 pull-request run failed in Start Dash app after installing Plotly 7.1.0: `plotly.graph_objects` no longer had `Scattermapbox`. Browser tests were skipped in that run. This branch adds `plotly>=5.24.0,<7` to retain the existing map API while a migration is planned. Verify the replacement CI run; the constraint alone does not validate maps or data. Other dependencies still use lower bounds, so a tested lock or compatibility policy remains a follow-up.

## Findings requiring repair

| Finding | Current evidence | Acceptance check |
| --- | --- | --- |
| Polygon validity | All ten outer rings in `FIELDS` have only one latitude and therefore zero area. | Restore actual source polygons; check valid, nonempty geometries and positive area in an appropriate projected CRS. Do not invent replacement vertices. |
| Heat-stress units | Twenty monthly rows exceed the calendar-day count; July 2024 is labeled 240 days. | Recover the original daily observations, threshold, units, and spatial aggregation. If these are field-days or another quantity, label and aggregate them correctly; if they are days, recompute to the calendar bound. |
| Acreage | Embedded `area_acres` sums to 599.6; the case study says 579.6. | Reconcile against source polygons and metadata; do not substitute one unverified total for the other. |
| Crop counts | Embedded values give six soybean, three corn, and one grass/pasture record; the case study says five soybean fields. | Generate counts from the validated dataset and align text, filters, and charts. |
| Soil counts | Embedded values give five Fallsington records; the case study says four. | Generate the summary from the validated dataset. |
| Stress thresholds | One record is >35; two are >=35. Field 9 has the maximum value, 38. The case study gives different counts and names Field 6 as the maximum. | Choose documented thresholds, then make KPI, table, gauge, recommendations, and prose agree. |
| NDVI and source provenance | NDVI values are embedded; documentation describes upstream satellite interpolation but the raw imagery, extract records, and processing pipeline are absent here. | Supply provenance, dates, product identifiers, processing steps, and a reproducible sample. Otherwise label the values as illustrative. |
| Other weather units | Annual rainfall displays roughly 8,524–9,935 mm under the existing labels. | Reconcile original NASA POWER variables, units, location, and temporal/spatial aggregation before interpreting totals. Do not apply a guessed scale factor. |
| Recommendation confidence | The UI displays confidence percentages and operational recommendations. | Document the basis and limits or label these as illustrative rules, not calibrated probabilities or validated prescriptions. |

## Hosted application check

- The hosted HTML application loaded at `https://green-ag-intelligence-1.onrender.com/`; demo mode and weather navigation were observed.
- Global search produced a selected-field response.
- KPI values populated after demo activation, but a later overview state returned to placeholders. Reproduce and resolve the state transition.
- At a 1363px-wide desktop viewport, document width was 1430px. Check clipping and overflow, including KPI cards and toolbar.
- The map was blank with “Failed to initialize WebGL” in this browser. This may be environment-specific; validate in a WebGL-capable desktop browser as well as correcting the zero-area geometries.
- A theme-button click did not establish a coherent visual theme change during this check. Re-test; do not mark dark mode as passed.
- A recommendation View Field action kept navigation available and produced a selected-field response; report/export actions were not validated.
- Mobile and a separate private/incognito context were not tested. No full desktop/mobile pass is claimed.
- A successful CI run is not a substitute for these checks.

## Repair sequence

1. Recover source data and provenance; settle geometry and weather units.
2. Derive acreage, crop/soil counts, stress categories, and recommendations from validated inputs.
3. Repair layout, KPI state, theme behavior, and any confirmed navigation/export problems.
4. Add meaningful data checks and browser assertions, including a calendar bound when the metric is defined as days and geometry validity/area checks.
5. Re-run CI, inspect errors, and test a deployed desktop/private window plus at least one mobile viewport.
6. Record commit, deployed revision, device/viewport, date, results, and any remaining limitations.
7. Publish current screenshots; then use the live demo as the first Featured link.

Do not move test files or reorganize imports while resolving the primary data and behavior issues unless the change is necessary and verified. Keep working behavior stable.

## Presentation items

- Set repository description, homepage, and topics as specified in the career handoff.
- Keep source and documentation links prominent.
- The pull-request creation link in the old case study was not an existing completed pull request.
- License choice remains with the repository owner. Add a LICENSE file only after that choice is established.

