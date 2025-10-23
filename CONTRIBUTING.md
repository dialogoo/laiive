# Contributing

Thanks for helping improve **laiive**!

---

## Agreement
Take a look to the [Collaborator Agreement](LICENSES/COLLABOATOR_AGREEMENT.md).

---

## How to Contribute
- Open issues for bugs, ideas, or questions.
- Make pull requests with clear, focused changes.
- Follow our commit message guidelines below.

---

## Commit Message Guidelines

We prioritize self-documenting code and meaningful commit messages. Code should clearly express **what** it does, while commit messages explain **why**.

### Format

```
<type>: <brief summary>

<detailed explanation>
- Why was this change necessary?
- What problem does it solve?
- What alternatives were considered?
```

### Types
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `perf:` Performance improvement
- `docs:` Documentation
- `test:` Tests
- `chore:` Maintenance

### Example
```
refactor: Replace nested loops with hash map in findDuplicates

The O(n²) approach was causing timeouts on large datasets.
HashMap provides O(1) lookups and reduces execution time
from 2.3s to 45ms on 10k items.

Refs: #156
```

### Code Documentation Rules

**Avoid:**
- Comments restating obvious code
- Commented-out code (use git history)
- Vague TODOs and FIXMEs without context

**Include:**
- Why non-obvious decisions were made
- Complex business logic explanations
- Known limitations or edge cases
- Public API documentation
- Complex algorithms or patterns

---

## Respect & Kindness
- Be kind and polite.
- Listen to others and assume good intent.
- Disagree with ideas, not with people.

---

That's it. Let's keep things simple, safe, and respectful while building together.

---

## Recomended reading to be a good contributor

- Hunt, A., & Thomas, D. (2019). The pragmatic programmer: Your journey to mastery (20th anniversary ed.). Addison-Wesley.
