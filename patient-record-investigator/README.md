# Patient-Record Investigator

An Agentic AI capstone that investigates missing or conflicting information
across a patient's records and prepares an evidence-backed review queue.

**Status:** Project proposal. Implementation has not started.

## Problem

Medical records collected at different times can appear inconsistent. A referral
may describe a test as pending even though a later report contains its result.
Two documents may also contain conflicting allergy entries that require review.
The investigator must distinguish changes over time from unresolved contradictions.

## Proposed workflow

1. Load synthetic patient records and retain each document's source and date.
2. Extract structured facts and assemble a patient timeline.
3. Identify possible inconsistencies or missing information.
4. Select tools to retrieve supporting records and check dates and values.
5. Reassess each finding as new evidence becomes available.
6. Produce a review queue with evidence, uncertainty, and a suggested clarification.

The agent chooses follow-up checks based on its findings. Deterministic tools
perform comparisons and date calculations. Source records remain unchanged;
unresolved clinical discrepancies go to a human reviewer.

## Initial scope

- Synthetic records for a small set of fictional patients.
- Referrals, encounter summaries, allergy entries, and test results.
- Three finding types: pending tests with later results, conflicting allergy
  documentation, and missing documents explicitly referenced in a record.
- A local interface showing the timeline, findings, and supporting evidence.

## Example demonstration

A referral says a test is pending. The agent searches later records, finds the
matching result, and explains that the status changed over time. It also finds
conflicting allergy documentation and leaves that finding unresolved for review.

## Planned tools

| Tool | Purpose |
| --- | --- |
| `list_records(patient_id)` | List available records and their dates |
| `read_record(record_id)` | Retrieve source text |
| `search_records(patient_id, query)` | Find relevant evidence |
| `build_timeline(patient_id)` | Arrange documented events chronologically |
| `compare_facts(fact_ids)` | Check comparable values and dates |
| `save_finding(finding)` | Save a finding with source references |

## Evaluation

Create labelled synthetic cases with known inconsistencies and normal changes
over time. Keep evaluation cases separate from development cases. Compare the
agent with a fixed-rule baseline using:

- Precision and recall of discrepancy detection.
- False alarms on legitimate changes over time.
- Correct source citations and date interpretation.
- Appropriate handling of insufficient evidence.
- Tool calls, latency, and model cost per case.

Synthetic evaluation demonstrates prototype behavior, not clinical validation.

## Milestones

1. Define record formats and create labelled synthetic cases.
2. Implement retrieval, timeline, and comparison tools.
3. Implement the bounded investigation loop and evidence-linked findings.
4. Add the review interface and run baseline comparisons.
5. Prepare the demonstration, evaluation results, and capstone report.

## Data and references

- [Synthea](https://synthetichealth.github.io/synthea/): synthetic patient histories
  available in FHIR and CSV formats. Adapt these or use hand-authored fictional
  documents for the first version.
- [HL7 FHIR overview](https://www.hl7.org/fhir/overview.html): healthcare data
  exchange concepts for a later integration.

Use synthetic data for the public repository and demo. Do not commit patient
records, credentials, or API keys.
