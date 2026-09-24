# Student Information API Requirements

## 1. Background and Scope

The system provides three student-facing HTTP capabilities: student account/profile registration, a role-scoped student list, and role-scoped student detail lookup. These requirements complement the authentication and authorization rules in `login-requirements.md`.

## 2. Actors

- **Student:** Registers a student account and pending profile, and views their own approved profile.
- **Teacher:** Views and queries approved profiles for assigned students.
- **Administrator:** Views all approved student profiles and manages account approval as defined by the login requirements.

## 3. Functional Requirements

### FR-STUDENT-001 — Student registration operation

The `POST /students` operation shall create a student account application and its pending student profile atomically. It shall no longer mean immediate creation of an official Student record.

### FR-STUDENT-002 — Registration fields

The registration request shall contain username, password, email, student ID, name, major, and grade. Teacher employee ID and administrator role are not applicable to this operation.

### FR-STUDENT-003 — Registration validation

After trimming surrounding whitespace, student ID, name, and major shall be non-empty. Email shall be valid and globally unique using case-insensitive comparison. Student ID shall be globally unique. Grade shall be a four-digit integer. Username and password shall comply with `login-requirements.md`.

### FR-STUDENT-004 — Registration lifecycle

Successful registration shall return `201` and a unified success message only. It shall not return a password, Token, account state, or profile contents. The account requires email verification and administrator approval before login; the profile requires assigned-teacher approval before becoming official.

### FR-STUDENT-005 — Registration atomicity and duplicates

If validation fails or username, email, or student ID is already used, the operation shall create neither the account application nor the profile. It shall return `409` for duplicate data and `422` for missing or invalid fields, identifying the duplicated field in the duplicate result.

### FR-STUDENT-006 — Failed registration identifiers

A failed request shall not retain its submitted email or student ID. A rejected application is distinct from a failed request: a rejected application's student ID remains reserved to that application for resubmission.

### FR-STUDENT-007 — Student list operation

The `GET /students` operation shall require authentication and return only approved student profiles visible to the caller:

- a student receives their own profile, at most one record;
- a teacher receives profiles of assigned students;
- an administrator receives all approved profiles.

### FR-STUDENT-008 — Student list pagination

`GET /students` shall use page-number pagination starting at page 1, default page size 20, and maximum page size 100. Results shall be sorted by student ID ascending. A page beyond the last page shall return `200` with an empty list. The response shall include the list, total visible record count, and `has_next`.

### FR-STUDENT-009 — Student list response

Each returned student shall include internal ID, student ID, name, email, major, grade, and creation time. An authorized query with no visible students shall return `200` with an empty list.

### FR-STUDENT-010 — Student detail operation

The `GET /students/{student_id}` operation shall require authentication and return the approved profile only when:

- the caller is the student associated with that profile;
- the caller is a teacher assigned to that student; or
- the caller is an administrator.

### FR-STUDENT-011 — Student detail not-found behavior

The detail operation shall return `404` when the student does not exist or has no approved profile. It shall return `403` when the student exists but the authenticated caller is not permitted to access it.

### FR-STUDENT-012 — Authentication and protocol results

`GET /students` and `GET /students/{student_id}` shall use the authentication rules in `login-requirements.md`: unauthenticated or invalid-token requests shall return `401`, authenticated but unauthorized requests shall return `403`, and successful queries shall return `200`. An unauthenticated prospective student may call `POST /students` as the public registration entry point; successful registration shall return `201`.

## 4. Business Rules

- **BR-STUDENT-001:** Registration creates a pending account application and pending profile together.
- **BR-STUDENT-002:** Account approval and profile approval are separate: email verification and administrator account approval precede login; assigned-teacher approval precedes an official profile.
- **BR-STUDENT-003:** No student profile is visible through ordinary queries until teacher approval.
- **BR-STUDENT-004:** List totals and `has_next` are calculated only over records visible to the caller.
- **BR-STUDENT-005:** Logical deletion excludes the account's student from both ordinary query operations.
- **BR-STUDENT-006:** No filtering capability is required for the list operation.

## 5. Data Requirements

- **DR-STUDENT-001:** The pending account and pending profile must be committed or rejected as one operation.
- **DR-STUDENT-002:** A student account has one student profile and one immutable student ID.
- **DR-STUDENT-003:** Ordinary query responses expose the seven fields in FR-STUDENT-009 and only approved profile values.
- **DR-STUDENT-004:** Pagination metadata must describe the caller-scoped result set.

## 6. Error Handling and Security

- `401` shall be returned for missing, invalid, or expired authentication on the two query operations. `POST /students` is public for prospective-student registration and does not require an existing account.
- `403` shall be returned for an authenticated caller without permission for the requested student.
- `404` shall be returned for a missing student or a student without an approved profile.
- `409` shall identify the duplicate username, email, or student ID.
- `422` shall identify missing or invalid registration fields.
- Registration success shall not disclose credentials, Tokens, or internal approval details in its success body.
- Existing account, password, email, Token, audit, and fail-closed controls remain governed by `login-requirements.md`.

## 7. Non-functional Requirements

The list and detail operations shall meet the authentication-system performance and HTTPS requirements in `login-requirements.md`. No additional student-API performance target has been confirmed.

## 8. Out of Scope

- Filtering, searching, or custom sorting for `GET /students`.
- Returning pending or rejected profiles through ordinary list/detail queries.
- Direct creation of an official profile through `POST /students`.
- API path changes, database schema, and implementation technology.

## 9. Open Questions

No stakeholder decision currently blocks the three API requirements. Query parameter names, response property names, exact success/error text, and database/API implementation details remain design decisions.
