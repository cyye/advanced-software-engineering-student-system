# User Stories

## Account and access

### US-LOGIN-001 — Self-register

- **Role:** Prospective student or teacher
- **Goal:** Submit a role-appropriate account application
- **Benefit:** I can request access without administrator account creation
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-001–003, FR-LOGIN-006

As a prospective student or teacher, I want to self-register with my required identifiers so that I can request access to the system.

### US-LOGIN-002 — Verify email

- **Role:** Account holder
- **Goal:** Verify my unique email with a one-time link
- **Benefit:** My email can safely support account access and recovery
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-007, FR-LOGIN-009

As an account holder, I want to verify my email so that my account can become eligible to log in.

### US-LOGIN-003 — Review account applications

- **Role:** Administrator
- **Goal:** Approve or reject self-registered accounts with a reason
- **Benefit:** Only reviewed applicants can access the system
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-008, FR-LOGIN-033

As an administrator, I want to review student and teacher applications so that only approved accounts can log in.

### US-LOGIN-004 — Revise a rejected application

- **Role:** Applicant
- **Goal:** View the rejection reason and resubmit corrected information
- **Benefit:** I can correct my application without losing my reserved student ID
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-006, FR-LOGIN-008, FR-LOGIN-026

As an applicant, I want to revise a rejected application so that I can address the administrator's reason and apply again.

### US-LOGIN-005 — Create accounts

- **Role:** Administrator
- **Goal:** Create student, teacher, and administrator accounts
- **Benefit:** Accounts can be provisioned without self-registration or approval
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-004, FR-LOGIN-033

As an administrator, I want to create accounts for all supported roles so that authorized users can be provisioned directly.

### US-LOGIN-006 — Bootstrap administration

- **Role:** System operator
- **Goal:** Configure one initial administrator securely
- **Benefit:** The system has an administrator at first initialization
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-005, FR-LOGIN-020

As a system operator, I want the configured initial administrator created once so that account administration can begin securely.

## Authentication and password management

### US-LOGIN-007 — Log in

- **Role:** Eligible user
- **Goal:** Log in with username and password
- **Benefit:** I receive authenticated access for my role
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-009, FR-LOGIN-010, FR-LOGIN-011, FR-LOGIN-012, FR-LOGIN-017, FR-LOGIN-021

As an eligible user, I want to log in with my username and password so that I can access permitted operations.

### US-LOGIN-008 — Refresh a session

- **Role:** Logged-in user
- **Goal:** Rotate my Refresh Token and obtain a new Access Token
- **Benefit:** I can continue my session without entering credentials again
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-013, FR-LOGIN-014

As a logged-in user, I want to refresh my tokens so that I can continue an eligible session securely.

### US-LOGIN-009 — Log out everywhere

- **Role:** Logged-in user
- **Goal:** Invalidate all of my sessions
- **Benefit:** Previously issued tokens can no longer access my account
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-015, FR-LOGIN-016

As a logged-in user, I want logout to invalidate all my sessions so that no existing token remains usable.

### US-LOGIN-010 — Change password

- **Role:** Logged-in user
- **Goal:** Change my password using my current password
- **Benefit:** I can update my credential and invalidate existing sessions
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-017, FR-LOGIN-018

As a logged-in user, I want to change my password so that I can protect my account with a new credential.

### US-LOGIN-011 — Reset password

- **Role:** User who forgot a password
- **Goal:** Receive a one-time reset link at my verified email
- **Benefit:** I can regain access without exposing whether an account exists
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-019

As a user who forgot my password, I want to reset it through my verified email so that I can regain account access.

### US-LOGIN-012 — Change email

- **Role:** Account holder
- **Goal:** Replace my email after verifying the new address
- **Benefit:** My account and recovery email remain current
- **Priority:** Medium
- **Related Functional Requirements:** FR-LOGIN-027

As an account holder, I want to verify a new email before it replaces my old email so that the change is controlled.

## Student profile and teacher review

### US-LOGIN-013 — View own information

- **Role:** Student
- **Goal:** View only my own student information
- **Benefit:** I can inspect my record without seeing another student's information
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-022

As a student, I want to view my own information so that student privacy is maintained.

### US-LOGIN-014 — Submit initial profile

- **Role:** Student
- **Goal:** Submit my complete profile for assigned-teacher review
- **Benefit:** An approved official profile can be established
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-023, FR-LOGIN-026, FR-LOGIN-031

As a student, I want to submit my first profile so that an assigned teacher can review it.

### US-LOGIN-015 — Modify profile

- **Role:** Student
- **Goal:** Submit permitted changes while the prior approved version stays effective
- **Benefit:** My official information changes only after review
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-024–026

As a student, I want to submit changes for review so that approved information remains stable until a decision.

### US-LOGIN-016 — Review assigned student

- **Role:** Teacher
- **Goal:** Approve or reject an assigned student's profile with a reason
- **Benefit:** Only reviewed profile data becomes official
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-025, FR-LOGIN-028

As a teacher, I want to review only my assigned students so that review authority follows supervision relationships.

### US-LOGIN-017 — Query assigned students

- **Role:** Teacher
- **Goal:** View my assigned-student list and their permitted profile information
- **Benefit:** I can perform my supervision responsibilities
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-028–031

As a teacher, I want to query my assigned students so that I can supervise them without accessing other students.

## Administration and operations

### US-LOGIN-018 — Manage accounts

- **Role:** Administrator
- **Goal:** Query, create, approve, reject, disable, restore, delete, and change roles
- **Benefit:** I can administer the account lifecycle
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-033, FR-LOGIN-034

As an administrator, I want to manage accounts while preserving at least one effective administrator so that the system remains administrable.

### US-LOGIN-019 — View all information

- **Role:** Administrator
- **Goal:** View all system information
- **Benefit:** I can perform system-wide administration
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-032

As an administrator, I want to view all information so that I can fulfill administrative duties.

### US-LOGIN-020 — Refresh supervision relationships

- **Role:** Administrator
- **Goal:** Load valid CSV relationships and inspect invalid-row results
- **Benefit:** Teacher permissions reflect the supplied supervision data
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-029–031

As an administrator, I want to refresh supervision relationships and see invalid rows so that assignment errors can be corrected.

### US-LOGIN-021 — View audit history

- **Role:** Administrator
- **Goal:** View all online security audit records
- **Benefit:** I can investigate security and administrative events
- **Priority:** High
- **Related Functional Requirements:** FR-LOGIN-035, FR-LOGIN-036

As an administrator, I want to view online audit history so that security-sensitive actions are traceable.

### US-LOGIN-022 — View own security events

- **Role:** Account holder
- **Goal:** View security events related to my account
- **Benefit:** I can recognize relevant account activity
- **Priority:** Medium
- **Related Functional Requirements:** FR-LOGIN-035, FR-LOGIN-036

As an account holder, I want to view security events related to me so that I can monitor my account.

### US-LOGIN-023 — Access archived audit records

- **Role:** System operator
- **Goal:** Access permanent immutable audit archives
- **Benefit:** Long-term audit evidence remains available
- **Priority:** Medium
- **Related Functional Requirements:** FR-LOGIN-036

As a system operator, I want access to archived audit records so that older events remain traceable.

## Student Information APIs

The following stories trace to `student-requirements.md`.

### US-STUDENT-001 — Register a student account and profile

- **Role:** Prospective student
- **Goal:** Submit username, password, email, student ID, name, major, and grade in one registration request
- **Benefit:** My account application and pending profile are created together
- **Priority:** High
- **Related Functional Requirements:** FR-STUDENT-001–004

As a prospective student, I want to submit my account and profile information together so that I can begin the email, account, and teacher-review process.

### US-STUDENT-002 — Receive a safe registration result

- **Role:** Prospective student
- **Goal:** Receive a success message without credentials or pending-record details
- **Benefit:** My sensitive information is not exposed in the registration response
- **Priority:** High
- **Related Functional Requirements:** FR-STUDENT-004–006

As a prospective student, I want registration to be atomic and not return secrets so that a failed request leaves no partial data and a successful response is safe.

### US-STUDENT-003 — View the permitted student list

- **Role:** Authenticated student, teacher, or administrator
- **Goal:** Query a paginated list limited to my role's visibility
- **Benefit:** I see exactly the student records I am authorized to see
- **Priority:** High
- **Related Functional Requirements:** FR-STUDENT-007–009

As an authenticated user, I want a paginated role-scoped student list so that I can access permitted records efficiently.

### US-STUDENT-004 — View a permitted student profile

- **Role:** Authenticated student, teacher, or administrator
- **Goal:** Query an approved student profile by student ID when authorized
- **Benefit:** I can inspect the relevant official information without seeing pending or unauthorized records
- **Priority:** High
- **Related Functional Requirements:** FR-STUDENT-010–012

As an authenticated user, I want to query an authorized student's approved profile so that access follows ownership, supervision, and administrator permissions.

### US-STUDENT-005 — Handle registration validation

- **Role:** Prospective student
- **Goal:** Receive clear duplicate or invalid-field results
- **Benefit:** I can correct a registration without creating partial records
- **Priority:** High
- **Related Functional Requirements:** FR-STUDENT-003, FR-STUDENT-005, FR-STUDENT-006

As a prospective student, I want invalid or duplicate registration data rejected consistently so that I can correct it safely.

### US-STUDENT-006 — Handle empty and unavailable query results

- **Role:** Authenticated user
- **Goal:** Receive an empty list or not-found result when no permitted data exists
- **Benefit:** I can distinguish an empty authorized list from an unavailable individual profile
- **Priority:** Medium
- **Related Functional Requirements:** FR-STUDENT-008–011

As an authenticated user, I want defined empty-list and not-found behavior so that query results are predictable.
