# Open Questions

No unresolved stakeholder decision currently blocks functional design or acceptance-test design.

The following are implementation-design decisions rather than missing business requirements and should be resolved during technical design:

1. API response property names and protocol-specific status-code payload details (the three paths and result categories are confirmed).
2. Database schema, migrations, and persistence technology details.
3. Concrete libraries for PBKDF2, JWT, email delivery, and CSV processing.
4. Runtime configuration names and secret-delivery mechanism.
5. Exact user-facing wording for the defined error categories.
6. Email templates and the application URL embedded in verification and reset links.
7. Deployment topology, HTTPS termination, and the representative environment used for performance verification.

The business behavior of `GET /students`, `GET /students/{student_id}`, and `POST /students` is specified in `student-requirements.md` and traced from `US-STUDENT-*` to `AC-STUDENT-*`.

Any decision that changes observable behavior must first be added to `login-requirements.md` and traced into `user-stories.md` and `acceptance-criteria.md`.
