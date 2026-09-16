# Repository Guidelines

## Architecture

Keep the current simple layered structure:

```text
API → Service → Database
```

Business logic should remain in `services.py`.

API handlers should remain small.

Do not access the database directly from API handlers unless already required by the existing design.

## Code Changes

Prefer minimal changes.

Do not perform unrelated refactoring.

Follow the existing code style.

## Testing

Run pytest after changing application behavior.

New features should include corresponding tests.

## Compatibility

Do not break existing APIs.
