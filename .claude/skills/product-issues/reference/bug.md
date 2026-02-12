# 🐛 Product Owner - Bug Specification

Create a bug specification for the `Task` using the `Specification Format`.

## Instructions

- You are a Product Owner. Focus on WHAT is broken and USER IMPACT, not HOW to fix it.
- DO NOT include technical root cause, file paths, or code fixes.
- Focus on: user impact, reproduction steps, expected vs actual behavior.
- Replace every `<instruction>` with your reasoned content.

## Specification Format

```md
## 🐛 Product Specification

### 1️⃣ Bug Summary
---
<clear summary of what's broken from user perspective>

### 2️⃣ User Impact
---

#### Affected Users
<who is affected, what percentage, are there workarounds?>

#### Severity
<Critical | High | Medium | Low - explain why>

#### Business Impact
<consequences: revenue, user frustration, support tickets?>

### 3️⃣ Bug Description
---

#### Expected Behavior
<what SHOULD happen>

#### Actual Behavior
<what IS happening>

#### Steps to Reproduce
1. <step 1>
2. <step 2>
3. <step 3>

### 4️⃣ Acceptance Criteria (Gherkin)
---

#### Scenario 1: Bug Fixed
Given <context where bug occurred>
When <user action that triggered bug>
Then <expected behavior works correctly>

#### Scenario 2: No Regression
Given <related functionality>
When <user performs related actions>
Then <everything still works>

### 5️⃣ Out of Scope
---
<what this fix does NOT include>
```

---

## Task

$ARGUMENTS
