# User Login Requirements Specification

## 1. Background

The student management system currently exposes student creation and query operations without authentication or authorization. It shall add account registration, login, token authentication, account administration, role-based access, student-profile review, and security controls for students, teachers, and administrators. This specification records confirmed, externally observable requirements without prescribing APIs or database schemas.

## 2. Scope

The scope includes student and teacher self-registration; administrator-created accounts; email verification and account approval; username/password authentication; JWT Access Tokens and rotating Refresh Tokens; password change and reset; session, logout and lockout controls; role authorization; reviewed student-profile versions; CSV supervision relationships; account administration; auditing; and performance targets.

## 3. Actors

- **Student:** Maintains one student profile and views their own account and profile status.
- **Teacher:** Queries assigned students and reviews their profile submissions.
- **Administrator:** Approves and manages accounts, views all information, refreshes the supervision CSV, and views online audit records.
- **System Operator:** Configures runtime secrets and the initial administrator and may access archived audit records.

## 4. Functional Requirements

### Account identity and registration

#### FR-LOGIN-001 — Roles

The system shall support exactly one role per account: student, teacher, or administrator.

#### FR-LOGIN-002 — Username

The system shall use an independent username as the login identifier. It shall be globally unique using case-insensitive comparison, contain 3–32 English letters, digits, or underscores, have surrounding whitespace removed, and be immutable.

#### FR-LOGIN-003 — Self-registration

Students and teachers, but not administrators, may self-register. All self-registrations shall provide username, password, email, and role. A student shall additionally provide a student ID; a teacher shall additionally provide a teacher employee ID.

#### FR-LOGIN-004 — Administrator-created accounts

An administrator may create student, teacher, and administrator accounts. Such accounts shall not require account approval but shall require email verification before login.

#### FR-LOGIN-005 — Initial administrator

On first initialization, the system shall create one administrator from a username, password, and email supplied through the runtime environment and automatically send a verification email. Later starts shall not overwrite that account.

#### FR-LOGIN-006 — Identifier reservation

Usernames, emails, teacher employee IDs, and student IDs shall be globally unique in their respective namespaces. Rejection shall release username, email, and teacher employee ID. A rejected application's student ID shall remain reserved to that application for resubmission. Identifiers retained by a logically deleted account shall not be reusable.

### Email verification and account approval

#### FR-LOGIN-007 — Email verification

Every account shall verify its unique email before login. A verification link shall be valid for 10 minutes and usable once. A new link may be requested no more than once per 5 minutes and shall invalidate the previous link. A pending email shall be reserved immediately.

#### FR-LOGIN-008 — Self-registration approval

After email verification, an administrator shall review a self-registered student or teacher account. States shall include pending, approved, and rejected. Rejection requires a reason. The applicant may view the state and reason, revise the application, and resubmit it.

#### FR-LOGIN-009 — Login eligibility

A self-registered account shall not log in until its email is verified and application approved. An administrator-created account shall not log in until email verification. A disabled, logically deleted, or temporarily locked account shall not log in.

### Authentication, tokens, and sessions

#### FR-LOGIN-010 — Password login

The system shall authenticate an eligible account with its case-insensitive username and password. All login failures shall have the same external result without revealing their cause.

#### FR-LOGIN-011 — Token issuance

A successful login shall issue an HS256 JWT Access Token valid for 1 hour and an independent Refresh Token valid for 7 days. The Access Token shall contain account identifier, role, issued-at time, and expiration time and be submitted as `Authorization: Bearer <access-token>`.

#### FR-LOGIN-012 — Single active session

Each account shall have at most one active session. A successful new login shall immediately invalidate that account's previous Access Token and Refresh Token.

#### FR-LOGIN-013 — Token refresh

An unexpired Refresh Token alone shall request refresh. Successful refresh shall issue a new Access Token and Refresh Token and immediately invalidate the old Refresh Token. The account shall first be confirmed as not deleted or disabled, unchanged in role, and still eligible to log in.

#### FR-LOGIN-014 — Refresh-token reuse

Reuse of a rotated Refresh Token shall be rejected and immediately invalidate all sessions for that account.

#### FR-LOGIN-015 — Logout and global invalidation

Logout shall invalidate all account sessions. Account disablement, logical deletion, role change, password change, password reset, HS256 signing-key change, and detected Refresh Token reuse shall invalidate affected tokens on their next use.

#### FR-LOGIN-016 — Protected access

Expired, invalidated, malformed, or otherwise invalid Access Tokens shall not authorize protected operations. If current account state cannot be read, protected operations and token refresh shall be rejected.

### Password management

#### FR-LOGIN-017 — Password policy and storage

A password shall contain at least 8 characters and include uppercase, lowercase, digit, and special characters. Passwords shall use PBKDF2-HMAC-SHA256 with at least 600,000 iterations and a separate random salt of at least 16 bytes. The iteration count shall be runtime-configurable; the system shall refuse to start below the minimum.

#### FR-LOGIN-018 — Password change

An authenticated user may change password only with the correct current password. The new password shall satisfy FR-LOGIN-017 and differ from the current password. Success shall invalidate all account tokens.

#### FR-LOGIN-019 — Password reset

A user shall request reset by email. Only a verified account email may receive a reset link. A link shall be valid for 10 minutes and usable once. No new link shall be issued while one remains valid. Invalid, expired, used, or superseded links shall have the same external result. Success shall enforce the password rules and invalidate all tokens.

#### FR-LOGIN-020 — Initial administrator password

The initial administrator shall change the environment-supplied password after first login before any other business operation. That change shall invalidate the initial session and require login again.

### Login protection

#### FR-LOGIN-021 — Login lockout

Five failed login attempts for the same account within 1 hour shall lock it for 15 minutes. Correct credentials shall also be rejected while locked. Lock expiration or successful login shall clear the failure count. An administrator may unlock early without clearing the count.

### Student information and review

#### FR-LOGIN-022 — Student access

A student shall query only the student information associated one-to-one with their account and shall not access another student's information.

#### FR-LOGIN-023 — Initial student profile

A student shall create one profile containing student ID, name, email, major, and grade. Student ID shall be the immutable ID supplied at registration. The first version shall remain pending until reviewed by an assigned teacher and shall not become official before approval.

#### FR-LOGIN-024 — Profile modification

A student may submit changes to an approved profile except username, student ID, and name. Only one pending version may exist. The previous approved version shall remain effective and visible while a change is pending or rejected.

#### FR-LOGIN-025 — Profile review

An assigned teacher shall approve or reject an initial or modified profile. Rejection requires a reason. A rejected version and reason shall remain available for student revision and resubmission. With multiple assigned teachers, the first completed review decides the version; later attempts shall be rejected as already processed.

#### FR-LOGIN-026 — Profile and state visibility

The student, assigned teachers, and administrators may view pending or rejected profile versions and review state; others may not. A user may view their own account application state, rejection reason, email-verification state, and applicable profile-review state.

#### FR-LOGIN-027 — Email change

All three roles may change their own email. A new unique email shall be reserved as pending and replace the old email only after verification. Email change requires no teacher review. Until verification, neither old nor pending email may be used for password reset.

### Teacher authorization and supervision CSV

#### FR-LOGIN-028 — Teacher access

A teacher shall query and review only assigned students. A student may have multiple teachers, each eligible to review subject to FR-LOGIN-025.

#### FR-LOGIN-029 — CSV structure

Relationships shall come from a UTF-8 CSV headed `teacher_employee_id,student_id`, with one relationship per row. The loader shall trim field whitespace, ignore blank lines, and deduplicate repeated relationships.

#### FR-LOGIN-030 — CSV loading

The system shall load the CSV at startup. If missing or invalid, it shall continue with no teacher permissions. During operation only an administrator may trigger refresh. Invalid rows shall be ignored while valid rows load; each invalid row's line number and reason shall be recorded and visible to administrators. If refresh cannot produce usable content, the last valid relationships shall remain active.

#### FR-LOGIN-031 — Unassigned profile

Without an assigned teacher, a submitted profile shall remain pending until CSV update. Administrators and unassigned teachers shall not review it. A CSV relationship may refer to a student ID whose profile is pending.

### Administration and audit

#### FR-LOGIN-032 — Administrator information access

An administrator shall be able to view all system information.

#### FR-LOGIN-033 — Account administration

An administrator may query, create, approve, reject, disable, re-enable, logically delete, restore, and change account roles. Logical deletion shall preserve account, audit history, and student profile. Restoration retains the prior password but requires login. Role change retains business data but grants only new-role permissions.

#### FR-LOGIN-034 — Administrator continuity

The system shall always retain at least one effective administrator. An administrator may act on their own account only if the action does not disable, delete, or remove the administrator role from the last effective administrator.

#### FR-LOGIN-035 — Security audit

The system shall audit registration, account review, successful and failed login, token refresh, logout, password change and reset, account disablement and restoration, role change, profile review, and CSV refresh. Records shall include event type, time, executing account, and applicable target account or resource. Passwords, complete tokens, and complete reset links shall not be logged. Users and administrators shall not modify or delete audit records.

#### FR-LOGIN-036 — Audit access and retention

Administrators may view all online audit records. Other users may view security events related to their accounts. Online records shall be retained for 90 days and then moved to permanent immutable archives accessible only to system operators.

## 5. Non-functional Requirements

- **NFR-LOGIN-001:** Under 100 concurrent users, at least 99% of login requests shall complete within 1 second.
- **NFR-LOGIN-002:** Under 100 concurrent users, at least 99% of Access Token validation requests shall complete within 200 milliseconds.
- **NFR-LOGIN-003:** In production, communication involving login, passwords, tokens, email verification, or reset links shall use HTTPS.
- **NFR-LOGIN-004:** If current account state cannot be checked, protected access and token refresh shall fail closed.

## 6. Business Rules

- **BR-LOGIN-001:** An account has exactly one role; only students and teachers may self-register.
- **BR-LOGIN-002:** All accounts require verified email before login; self-registered accounts additionally require approval.
- **BR-LOGIN-003:** Account email, student-profile email, and reset email are the same value.
- **BR-LOGIN-004:** A student account and profile have a one-to-one relationship.
- **BR-LOGIN-005:** Student ID is immutable and permanently reserved to its application or account.
- **BR-LOGIN-006:** Username, student ID, and student name are not student-editable after profile creation.
- **BR-LOGIN-007:** Teachers access and review only CSV-assigned students.
- **BR-LOGIN-008:** Existing student operations require authentication: students access themselves, teachers assigned students, and administrators all students.
- **BR-LOGIN-009:** One account has one active session.
- **BR-LOGIN-010:** At least one effective administrator shall always exist.

## 7. Data Requirements

- **DR-LOGIN-001:** Account data shall distinguish username, role, email and verification state, registration origin, review state, enabled/deleted state, lock state, and token-invalidating state.
- **DR-LOGIN-002:** Student accounts retain unique student IDs; teacher accounts retain unique employee IDs.
- **DR-LOGIN-003:** Password data retains a derived value, per-account salt, and derivation parameters, never plaintext.
- **DR-LOGIN-004:** Session data supports one active session, Refresh Token rotation and reuse detection, logout, and account-wide invalidation.
- **DR-LOGIN-005:** Profile data distinguishes the effective approved version from one pending or rejected version and retains review decisions and reasons.
- **DR-LOGIN-006:** Pending email and email/reset tokens support reservation, expiration, replacement, and one-time use.
- **DR-LOGIN-007:** Audit data meets FR-LOGIN-035 and FR-LOGIN-036.

## 8. Security Requirements

- **SR-LOGIN-001:** HS256 signing material shall come from the runtime environment, contain at least 64 bytes, never be committed, and cause startup refusal if absent or too short.
- **SR-LOGIN-002:** Password protection shall comply with FR-LOGIN-017.
- **SR-LOGIN-003:** Token validity shall be checked against session and account state so FR-LOGIN-015 invalidations take effect on the next request.
- **SR-LOGIN-004:** Reset requests shall return a uniform response whether email is absent, unverified, rate-limited, or delivery fails. Requests for the same email are limited to one per 5 minutes.
- **SR-LOGIN-005:** Verification-email delivery failure may be disclosed; reset-email delivery failure shall not and shall be audited.
- **SR-LOGIN-006:** Authorization shall enforce ownership, role, assignment, and administrator-continuity rules.
- **SR-LOGIN-007:** Unauthorized student-information requests shall explicitly report insufficient permission.

## 9. Error Handling

- Login failures shall share one external result; missing username or password shall issue no token.
- Invalid, expired, invalidated, or malformed tokens shall reject protected access.
- Invalid, expired, used, or replaced reset links shall share one "invalid or expired" result.
- A second review of a processed profile and a submission while another version is pending shall be rejected.
- Unauthorized student access shall report permission denied.
- Invalid CSV rows shall not block valid rows and shall be reported by line and reason.
- Verification-email delivery failure shall be reported; reset-email delivery failure shall use the uniform reset response.

Protocol-specific status codes and payloads are not prescribed.

## 10. Out of Scope

- Database schema, persistence technology, API paths, payload shapes, and protocol-specific status codes.
- Multi-factor or federated authentication.
- Concurrent sessions for one account.
- Roles beyond student, teacher, and administrator.
- Editing supervision relationships through this feature.
- Physical deletion of accounts, profiles, or audit records.

## 11. Open Questions

No unresolved stakeholder decision currently blocks functional or test design. API structure, database schema, email provider, exact error text, and deployment topology remain implementation-design choices.
