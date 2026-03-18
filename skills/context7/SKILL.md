# Context7 Skill for OpenClaw

Use this skill when you need to search for up-to-date documentation for programming libraries, packages, or frameworks.

## When to Use

- User asks about latest version of a package
- User wants documentation for a specific library/framework
- User wants code examples for a library
- User asks "what's the latest version of X" or "how to use X"

## Setup (Already Done)

API key sudah disetup di VPS. Environment variable: `CONTEXT7_API_KEY`

## How to Use

### 1. Find Library ID

```bash
npx ctx7 library <library-name>
```

Contoh:
```bash
npx ctx7 library react
npx ctx7 library nextjs
npx ctx7 library rust
```

### 2. Get Documentation

```bash
npx ctx7 docs <library-id> "<query>"
```

Contoh:
```bash
npx ctx7 docs /facebook/react "useState hook"
npx ctx7 docs /vercel/next.js "app router"
npx ctx7 docs /rust-lang/rust "ownership"
```

## Examples

- "apa versi terbaru react?" → `npx ctx7 library react`
- "cek docs next.js latest" → `npx ctx7 docs /vercel/next.js "app router"`
- "carikan contoh useState react" → `npx ctx7 docs /facebook/react "useState"`

## Notes

- Context7 provides up-to-date, version-specific docs
- Much better than outdated training data
- Supports 1000+ popular libraries
- Library IDs start with "/" (e.g., /facebook/react)
