## Patient-Centric Ontology

### Goals

- Keep the patient as the primary anchor for both clinical and financial artifacts.
- Support practical hospital bills while remaining compatible with richer FHIR-style objects.
- Favor additive evolution: add nodes/edges/properties without breaking existing data.

### Core Design Principles

- Hub-and-spoke: everything ultimately connects to `Patient`.
- Nullable, sparse-friendly properties to accommodate noisy OCR and partial documents.
- Clear, verb-phrase relationship names for skimmability (`HAS_ENCOUNTER`, `BILLED_FOR`, `SEEN_BY`).

### Entities (Nodes)

- Patient: `id`, `full_name`, `date_of_birth`, `phone`, `email`, `address`
- Encounter: `id`, `service_start_date`, `service_end_date`, `encounter_type`, `chief_complaint`
- Practitioner: `id`, `name`, `npi`, `specialty`, `contact_phone`, `contact_email`
- Organization: `id`, `name`, `street`, `city`, `state`, `zip`, `phone`
- Invoice: `id`, `account_number`, `statement_date`, `due_date`, `total_balance_cents`, `amount_due_cents`, `minimum_payment_cents`, `website`, `customer_service_phone`
- LineItem: `id`, `description`, `qty`, `charge_cents`, `allowed_cents`, `payer_paid_cents`, `patient_copay_cents`, `patient_deductible_cents`, `patient_coinsurance_cents`, `internal_code`
- Procedure: `id`, `code_system`, `code`, `display`
- Condition: `id`, `code_system`, `code`, `display`
- Payment: `id`, `posted_date`, `amount_cents`, `source`, `method`
- Adjustment: `id`, `posted_date`, `amount_cents`, `reason_code`, `reason_text`
- InsurancePlan: `id`, `plan_name`, `subscriber_number`, `group_number`, `eligibility_date`
- Payer: `id`, `name`, `payer_code`, `contact_phone`
- Document (provenance): `id`, `doc_type`, `issued_date`, `raw_text_ref`, `source`
- Optional Extended: Claim, ExplanationOfBenefit, DiagnosticReport, Observation, MedicationRequest, Guarantor

### Relationships (Edges)

- Patient-centric:

  - `Patient --HAS_ENCOUNTER--> Encounter`
  - `Patient --BILLED_FOR--> Invoice`
  - `Patient --HAS_PAYMENT--> Payment`
  - `Patient --HAS_ADJUSTMENT--> Adjustment`
  - `Patient --COVERED_BY--> InsurancePlan`

- Encounter-centric:

  - `Encounter --SEEN_BY--> Practitioner`
  - `Encounter --AT_FACILITY--> Organization`
  - `Encounter --HAS_PROCEDURE--> Procedure`
  - `Encounter --HAS_CONDITION--> Condition`
  - `Encounter --GENERATED_CLAIM--> Claim`

- Billing:

  - `Invoice --HAS_LINE_ITEM--> LineItem`
  - `LineItem --ITEM_FOR_PROCEDURE--> Procedure`
  - `LineItem --ITEM_HAS_DIAGNOSIS--> Condition`
  - `Payment --APPLIED_TO--> Invoice`
  - `Adjustment --ADJUSTED_ON--> Invoice`
  - `Invoice --BILLED_TO--> Guarantor` (optional)

- Insurance:

  - `InsurancePlan --ISSUED_BY--> Payer`

- Provenance:
  - `Document --MENTIONS_ENTITY--> Patient`
  - `Document --MENTIONS_CONCEPT--> {Invoice|LineItem|Claim|...}`

### Usage Notes

- Extraction and graph construction occur in `graphrag_bootstrap.py`.
- CSVs are loaded into Memgraph using a generated script from `generate_memgraph_loader.py`.
- Suggested indexes (also generated): `Patient(id)`, `Encounter(id)`, `Practitioner(id)`, `Organization(id)`, `Invoice(id)`, `LineItem(id)`, `Procedure(code)`, `Condition(code)`, `InsurancePlan(id)`, `Payer(id)`.
- Example queries: see `patient_centric_queries.cypher` (update queries to use the labels/edges above).
