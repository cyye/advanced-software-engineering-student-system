# User Login Acceptance Criteria

Each criterion uses Given / When / Then and traces to the formal specification. Protocol-specific endpoints, status codes, and payloads remain design decisions.

## Registration, verification, and approval

### AC-LOGIN-001 — Student self-registration

- **ID:** AC-LOGIN-001
- **Related Requirement:** FR-LOGIN-002, FR-LOGIN-003, FR-LOGIN-006
- **Given:** A valid, available username, email, student ID, and conforming password.
- **When:** A prospective student submits a student registration.
- **Then:** A student application is created pending email verification and administrator approval, and its student ID is reserved.

### AC-LOGIN-002 — Teacher self-registration

- **ID:** AC-LOGIN-002
- **Related Requirement:** FR-LOGIN-002, FR-LOGIN-003, FR-LOGIN-006
- **Given:** A valid, available username, email, teacher employee ID, and conforming password.
- **When:** A prospective teacher submits a teacher registration.
- **Then:** A teacher application is created pending email verification and administrator approval.

### AC-LOGIN-003 — Administrator self-registration prohibited

- **ID:** AC-LOGIN-003
- **Related Requirement:** FR-LOGIN-003
- **Given:** The self-registration function is available.
- **When:** A user attempts to self-register as an administrator.
- **Then:** Registration is rejected and no administrator account is created.

### AC-LOGIN-004 — Username normalization and uniqueness

- **ID:** AC-LOGIN-004
- **Related Requirement:** FR-LOGIN-002, FR-LOGIN-006
- **Given:** An account named `Student_1` exists.
- **When:** Registration is attempted with ` student_1 `.
- **Then:** Surrounding whitespace is removed and registration is rejected as a duplicate using case-insensitive comparison.

### AC-LOGIN-005 — Password policy

- **ID:** AC-LOGIN-005
- **Related Requirement:** FR-LOGIN-017
- **Given:** A registration or password operation requires a new password.
- **When:** The password is shorter than 8 characters or lacks uppercase, lowercase, digit, or special character.
- **Then:** The password is rejected.

### AC-LOGIN-006 — Verify email

- **ID:** AC-LOGIN-006
- **Related Requirement:** FR-LOGIN-007, FR-LOGIN-009
- **Given:** An unverified account has a current, unused verification link issued less than 10 minutes ago.
- **When:** The account holder uses the link.
- **Then:** The email becomes verified and the link cannot be used again.

### AC-LOGIN-007 — Replace verification link

- **ID:** AC-LOGIN-007
- **Related Requirement:** FR-LOGIN-007
- **Given:** At least 5 minutes have elapsed since a verification link was sent.
- **When:** The user requests a new verification link.
- **Then:** A new 10-minute one-time link is sent and the previous link becomes invalid.

### AC-LOGIN-008 — Approve self-registered account

- **ID:** AC-LOGIN-008
- **Related Requirement:** FR-LOGIN-008, FR-LOGIN-009
- **Given:** A self-registered account has a verified email and is pending review.
- **When:** An administrator approves it.
- **Then:** Its state becomes approved and it becomes eligible to log in.

### AC-LOGIN-009 — Reject and resubmit account

- **ID:** AC-LOGIN-009
- **Related Requirement:** FR-LOGIN-006, FR-LOGIN-008
- **Given:** A pending application exists.
- **When:** An administrator rejects it with a reason.
- **Then:** The applicant can see the reason and resubmit; username, email, and teacher employee ID are released, while a student ID remains reserved to that application.

### AC-LOGIN-010 — Administrator-created account

- **ID:** AC-LOGIN-010
- **Related Requirement:** FR-LOGIN-004, FR-LOGIN-009
- **Given:** An administrator creates an account for any supported role.
- **When:** Creation succeeds but the email is unverified.
- **Then:** No approval is required, but login remains prohibited until email verification.

## Login, tokens, and passwords

### AC-LOGIN-011 — Successful login and token generation

- **ID:** AC-LOGIN-011
- **Related Requirement:** FR-LOGIN-009, FR-LOGIN-010, FR-LOGIN-011, FR-LOGIN-012
- **Given:** An eligible, unlocked account and matching username and password.
- **When:** The user logs in.
- **Then:** Login succeeds, a 1-hour HS256 Access Token and 7-day Refresh Token are returned, and any prior session is invalidated.

### AC-LOGIN-012 — Uniform login failure

- **ID:** AC-LOGIN-012
- **Related Requirement:** FR-LOGIN-009, FR-LOGIN-010
- **Given:** The username is absent or unknown, the password is absent or wrong, or the account is unverified, unapproved, rejected, disabled, or deleted.
- **When:** Login is attempted.
- **Then:** The same external login-failure result is returned, the user is not authenticated, and no tokens are issued.

### AC-LOGIN-013 — Access with valid Bearer token

- **ID:** AC-LOGIN-013
- **Related Requirement:** FR-LOGIN-011, FR-LOGIN-016
- **Given:** A valid, current Access Token for an eligible account.
- **When:** It is presented as `Authorization: Bearer <access-token>` for a role-permitted operation.
- **Then:** The account and role are recognized and the operation proceeds to authorization.

### AC-LOGIN-014 — Expired or invalidated Access Token

- **ID:** AC-LOGIN-014
- **Related Requirement:** FR-LOGIN-015, FR-LOGIN-016
- **Given:** An Access Token is expired, malformed, invalidated, or belongs to an old session.
- **When:** It is used for a protected operation.
- **Then:** The operation is rejected and the user must authenticate again or use an eligible refresh flow.

### AC-LOGIN-015 — Rotate Refresh Token

- **ID:** AC-LOGIN-015
- **Related Requirement:** FR-LOGIN-013
- **Given:** A current, unexpired Refresh Token for an eligible account.
- **When:** It alone is submitted for refresh.
- **Then:** A new token pair is issued and the submitted Refresh Token is immediately invalidated.

### AC-LOGIN-016 — Detect Refresh Token reuse

- **ID:** AC-LOGIN-016
- **Related Requirement:** FR-LOGIN-014, FR-LOGIN-015
- **Given:** A Refresh Token has already been rotated.
- **When:** The old token is submitted again.
- **Then:** Refresh is rejected and all sessions for the account are invalidated.

### AC-LOGIN-017 — Logout everywhere

- **ID:** AC-LOGIN-017
- **Related Requirement:** FR-LOGIN-015
- **Given:** A user has an active session.
- **When:** The user logs out.
- **Then:** All Access Tokens and Refresh Tokens for that account are invalid on their next use.

### AC-LOGIN-018 — Change password

- **ID:** AC-LOGIN-018
- **Related Requirement:** FR-LOGIN-017, FR-LOGIN-018
- **Given:** An authenticated user supplies the correct current password and a different conforming password.
- **When:** Password change is submitted.
- **Then:** The password changes and all account tokens are invalidated; a wrong current password or reused current password is rejected.

### AC-LOGIN-019 — Request password reset uniformly

- **ID:** AC-LOGIN-019
- **Related Requirement:** FR-LOGIN-019, SR-LOGIN-004, SR-LOGIN-005
- **Given:** Any email is supplied to password reset.
- **When:** The request is made, including for absent, unverified, rate-limited, or delivery-failure cases.
- **Then:** The same external result is returned; a valid link is sent only to an eligible verified email and no more often than once per 5 minutes.

### AC-LOGIN-020 — Use password-reset link

- **ID:** AC-LOGIN-020
- **Related Requirement:** FR-LOGIN-019
- **Given:** A current, unused reset link issued less than 10 minutes ago and a conforming password different from the current password.
- **When:** The user resets the password.
- **Then:** Reset succeeds, the link becomes unusable, and all account tokens are invalidated.

### AC-LOGIN-021 — Invalid password-reset link

- **ID:** AC-LOGIN-021
- **Related Requirement:** FR-LOGIN-019
- **Given:** A reset link is invalid, expired, already used, or superseded.
- **When:** It is submitted.
- **Then:** The same “invalid or expired” result is returned in every case.

### AC-LOGIN-022 — Login lockout

- **ID:** AC-LOGIN-022
- **Related Requirement:** FR-LOGIN-021
- **Given:** An account has four failed logins in the preceding hour.
- **When:** A fifth login fails.
- **Then:** The account is locked for 15 minutes and even correct credentials are rejected during that period.

### AC-LOGIN-023 — Administrator unlock

- **ID:** AC-LOGIN-023
- **Related Requirement:** FR-LOGIN-021, FR-LOGIN-033
- **Given:** An account is temporarily locked with its failure count retained.
- **When:** An administrator unlocks it and the user next logs in correctly.
- **Then:** Login succeeds and clears the failure count; another wrong password before success may immediately relock it.

## Authorization and profile review

### AC-LOGIN-024 — Student authorization

- **ID:** AC-LOGIN-024
- **Related Requirement:** FR-LOGIN-022, SR-LOGIN-006, SR-LOGIN-007
- **Given:** A logged-in student.
- **When:** The student queries their own record or attempts another student's record.
- **Then:** Their own record is returned; the other request is rejected explicitly as insufficient permission.

### AC-LOGIN-025 — Initial profile review

- **ID:** AC-LOGIN-025
- **Related Requirement:** FR-LOGIN-023, FR-LOGIN-025, FR-LOGIN-026
- **Given:** A student submits the registered student ID, name, email, major, and grade and has an assigned teacher.
- **When:** The assigned teacher approves the pending version.
- **Then:** It becomes the official profile; before approval it is visible only to the student, assigned teachers, and administrators.

### AC-LOGIN-026 — Reject profile with reason

- **ID:** AC-LOGIN-026
- **Related Requirement:** FR-LOGIN-024–026
- **Given:** An assigned teacher reviews a pending profile version.
- **When:** The teacher rejects it with a reason.
- **Then:** No pending data becomes official, the prior approved version remains effective if present, and the student may revise and resubmit the retained rejected version.

### AC-LOGIN-027 — Prevent concurrent pending versions

- **ID:** AC-LOGIN-027
- **Related Requirement:** FR-LOGIN-024
- **Given:** A student already has a pending profile version.
- **When:** The student attempts another profile submission.
- **Then:** The new submission is rejected until the existing version is reviewed.

### AC-LOGIN-028 — First teacher review wins

- **ID:** AC-LOGIN-028
- **Related Requirement:** FR-LOGIN-025, FR-LOGIN-028
- **Given:** Multiple teachers are assigned to one pending profile.
- **When:** One teacher completes review and another later submits a decision.
- **Then:** The first decision remains effective and the later attempt is rejected as already processed.

### AC-LOGIN-029 — Teacher scope

- **ID:** AC-LOGIN-029
- **Related Requirement:** FR-LOGIN-028, SR-LOGIN-006
- **Given:** A logged-in teacher and a student not assigned to that teacher.
- **When:** The teacher queries or reviews that student.
- **Then:** The operation is rejected as insufficient permission.

### AC-LOGIN-030 — Unassigned profile remains pending

- **ID:** AC-LOGIN-030
- **Related Requirement:** FR-LOGIN-031
- **Given:** A submitted student profile has no CSV-assigned teacher.
- **When:** An administrator or unassigned teacher attempts review.
- **Then:** Review is rejected and the profile remains pending until an assignment is loaded.

### AC-LOGIN-031 — Change email

- **ID:** AC-LOGIN-031
- **Related Requirement:** FR-LOGIN-007, FR-LOGIN-027
- **Given:** Any account holder requests an available new email.
- **When:** The change starts and later the new address is verified.
- **Then:** The pending email is reserved immediately; neither address supports reset while pending; after verification the new email replaces the old one without teacher review.

## CSV, administration, audit, and operations

### AC-LOGIN-032 — Load valid and invalid CSV rows

- **ID:** AC-LOGIN-032
- **Related Requirement:** FR-LOGIN-029, FR-LOGIN-030
- **Given:** A UTF-8 CSV with the required header contains blank, duplicate, valid, and invalid rows.
- **When:** An administrator refreshes it.
- **Then:** Blank lines are ignored, whitespace is trimmed, duplicates are deduplicated, valid relationships load, and each invalid row is reported by line and reason.

### AC-LOGIN-033 — CSV unavailable

- **ID:** AC-LOGIN-033
- **Related Requirement:** FR-LOGIN-030
- **Given:** The CSV is missing or unusable at startup, or a later refresh cannot produce usable content.
- **When:** Loading occurs.
- **Then:** Startup continues with no teacher permissions in the first case; a later failure preserves the last valid relationships.

### AC-LOGIN-034 — Logical delete and restore

- **ID:** AC-LOGIN-034
- **Related Requirement:** FR-LOGIN-006, FR-LOGIN-015, FR-LOGIN-033
- **Given:** An administrator logically deletes an account.
- **When:** Deletion and later restoration occur.
- **Then:** Tokens are invalidated, identifiers and related data remain reserved, login is denied while deleted, and restoration retains the password but requires a new login.

### AC-LOGIN-035 — Preserve last administrator

- **ID:** AC-LOGIN-035
- **Related Requirement:** FR-LOGIN-034
- **Given:** Only one effective administrator remains.
- **When:** an action would disable, delete, or change that account to a non-administrator role.
- **Then:** The action is rejected.

### AC-LOGIN-036 — Audit security events

- **ID:** AC-LOGIN-036
- **Related Requirement:** FR-LOGIN-035, FR-LOGIN-036
- **Given:** A specified security or administrative event occurs.
- **When:** Its audit record is written.
- **Then:** Event type, time, actor, and applicable target are recorded without passwords, complete tokens, or complete reset links, and users and administrators cannot alter or delete it.

### AC-LOGIN-037 — Audit retention and access

- **ID:** AC-LOGIN-037
- **Related Requirement:** FR-LOGIN-036
- **Given:** Online audit records exist and one becomes older than 90 days.
- **When:** Records are queried and the retention boundary passes.
- **Then:** Administrators see all online records, users see only events related to themselves, and the old record moves to a permanent immutable archive accessible only to system operators.

### AC-LOGIN-038 — Fail closed

- **ID:** AC-LOGIN-038
- **Related Requirement:** FR-LOGIN-016, NFR-LOGIN-004
- **Given:** The system cannot read current account or session state.
- **When:** A protected operation or token refresh is requested.
- **Then:** The request is rejected even if the presented token is correctly signed and unexpired.

### AC-LOGIN-039 — Performance

- **ID:** AC-LOGIN-039
- **Related Requirement:** NFR-LOGIN-001, NFR-LOGIN-002
- **Given:** A representative environment handles 100 concurrent users.
- **When:** Login and Access Token validation workloads are measured.
- **Then:** At least 99% of logins complete within 1 second and at least 99% of token validations within 200 milliseconds.

### AC-LOGIN-040 — Security configuration startup checks

- **ID:** AC-LOGIN-040
- **Related Requirement:** FR-LOGIN-017, SR-LOGIN-001
- **Given:** The HS256 secret is absent or shorter than 64 bytes, or PBKDF2 iterations are configured below 600,000.
- **When:** The application starts.
- **Then:** Startup is refused.

## Student Information API Acceptance Criteria

### AC-STUDENT-001 — Create student account application and pending profile

- **ID:** AC-STUDENT-001
- **Related Requirement:** FR-STUDENT-001, FR-STUDENT-002, FR-STUDENT-004
- **Given:** A prospective student submits valid username, password, email, student ID, name, major, and grade.
- **When:** `POST /students` is called.
- **Then:** The system atomically creates a pending student account application and pending profile, returns `201` with only a unified success message, and does not treat the profile as official.

### AC-STUDENT-002 — Validate registration fields

- **ID:** AC-STUDENT-002
- **Related Requirement:** FR-STUDENT-003, FR-STUDENT-005
- **Given:** A registration contains a blank trimmed student ID, name, or major; an invalid or duplicate email; a duplicate student ID; or a grade that is not a four-digit integer.
- **When:** `POST /students` is called.
- **Then:** The system returns `422` for missing/invalid fields or `409` for duplicate data, identifies the relevant duplicate field when applicable, and creates neither application nor profile.

### AC-STUDENT-003 — Registration is atomic on partial failure

- **ID:** AC-STUDENT-003
- **Related Requirement:** FR-STUDENT-001, FR-STUDENT-005, DR-STUDENT-001
- **Given:** Valid registration data reaches a failure while creating either the account application or pending profile.
- **When:** The operation completes.
- **Then:** Neither partial record is retained.

### AC-STUDENT-004 — Failed registration does not reserve identifiers

- **ID:** AC-STUDENT-004
- **Related Requirement:** FR-STUDENT-006
- **Given:** A registration fails validation or duplicate checking.
- **When:** Another registration uses its submitted email or student ID.
- **Then:** The later registration is not rejected merely because of the failed request.

### AC-STUDENT-005 — Student list access

- **ID:** AC-STUDENT-005
- **Related Requirement:** FR-STUDENT-007, FR-STUDENT-012
- **Given:** A valid authenticated student, teacher, or administrator requests `GET /students`.
- **When:** The request is authorized.
- **Then:** The student receives only their own record, the teacher receives assigned students, and the administrator receives all approved visible students, with status `200`.

### AC-STUDENT-006 — Student list pagination and ordering

- **ID:** AC-STUDENT-006
- **Related Requirement:** FR-STUDENT-008, FR-STUDENT-009
- **Given:** More than 20 authorized approved student records exist.
- **When:** A caller requests a page without custom page size.
- **Then:** The response contains at most 20 records sorted by student ID ascending, includes the list, total visible count, and `has_next`; a requested page beyond the last returns `200` with an empty list.

### AC-STUDENT-007 — Student list maximum page size

- **ID:** AC-STUDENT-007
- **Related Requirement:** FR-STUDENT-008
- **Given:** A caller requests a page size greater than 100.
- **When:** `GET /students` is called.
- **Then:** The request is rejected as an invalid request and no more than 100 records are returned.

### AC-STUDENT-008 — Empty authorized student list

- **ID:** AC-STUDENT-008
- **Related Requirement:** FR-STUDENT-009
- **Given:** A caller is authenticated but has no visible approved student records.
- **When:** `GET /students` is called.
- **Then:** The system returns `200` with an empty list and total `0`.

### AC-STUDENT-009 — Student detail access

- **ID:** AC-STUDENT-009
- **Related Requirement:** FR-STUDENT-010, FR-STUDENT-012
- **Given:** An approved student profile exists.
- **When:** The associated student, an assigned teacher, or an administrator calls `GET /students/{student_id}`.
- **Then:** The system returns `200` and the seven approved profile fields.

### AC-STUDENT-010 — Detail for missing or unapproved profile

- **ID:** AC-STUDENT-010
- **Related Requirement:** FR-STUDENT-011
- **Given:** The requested student ID does not exist or has no approved profile.
- **When:** An authenticated caller calls `GET /students/{student_id}`.
- **Then:** The system returns `404`.

### AC-STUDENT-011 — Detail authorization denial

- **ID:** AC-STUDENT-011
- **Related Requirement:** FR-STUDENT-010, FR-STUDENT-011, FR-STUDENT-012
- **Given:** A student requests another student's profile or a teacher requests a non-assigned student's profile.
- **When:** The authenticated caller calls `GET /students/{student_id}`.
- **Then:** The system returns `403`.

### AC-STUDENT-012 — Unauthenticated student query access

- **ID:** AC-STUDENT-012
- **Related Requirement:** FR-STUDENT-007, FR-STUDENT-010, FR-STUDENT-012
- **Given:** No valid authentication is supplied.
- **When:** The caller invokes `GET /students` or `GET /students/{student_id}`.
- **Then:** The system returns `401` and does not expose student data.

### AC-STUDENT-014 — Public student registration

- **ID:** AC-STUDENT-014
- **Related Requirement:** FR-STUDENT-001, FR-STUDENT-004, FR-STUDENT-012
- **Given:** A prospective student has no existing account and submits valid registration data.
- **When:** The unauthenticated caller invokes `POST /students`.
- **Then:** The system accepts the registration request, returns `201` with the unified success message, and creates the pending account application and pending profile atomically.

### AC-STUDENT-013 — Logical deletion and query visibility

- **ID:** AC-STUDENT-013
- **Related Requirement:** FR-STUDENT-007, FR-STUDENT-010, BR-STUDENT-005
- **Given:** A student's account is logically deleted.
- **When:** Any role calls the list or detail operation for that student.
- **Then:** The student is excluded from ordinary query results and detail lookup returns `404`.
