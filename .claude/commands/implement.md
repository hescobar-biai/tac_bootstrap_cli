# 🔨 Implement Plan - MUST USE TOOLS
**NO SIMULATION. NO CLAIMS WITHOUT ACTUAL FILE CHANGES.**

## ⚠️ GOLDEN RULE
**IF YOU DON'T USE Read/Edit/Write TOOLS, YOU AUTOMATICALLY FAIL.**
**IF git diff --name-only IS EMPTY, YOU FAILED COMPLETELY.**

---

## MANDATORY WORKFLOW

### Phase 1: UNDERSTAND THE PLAN (3 minutes)
1. Read the plan file COMPLETELY
2. List every file mentioned
3. List every modification required
4. Confirm you understand acceptance criteria

### Phase 2: IMPLEMENT (DO NOT SKIP - USE TOOLS EVERY TIME)

**FOR EVERY SINGLE FILE CHANGE:**
```
A) Read current file:        Read("path/to/file")
B) Identify change location:  Understand the exact position
C) Make the edit:            Edit() or Write() tool
D) Verify immediately:        Read() again to confirm
E) Show the result:          Display modified content
F) Git check:                Bash: git diff filename
```

**CRITICAL VALIDATION:**
- ✅ If Read/Edit/Read output shows the change → GOOD
- ❌ If you just describe changes without tools → INSTANT FAILURE
- ❌ If git diff --name-only is empty → INSTANT FAILURE
- ❌ If you claim "added line 5" but git shows 0 changes → INSTANT FAILURE

### Phase 3: VALIDATE EVERY CHANGE

After each file modification:
```bash
# Check that files actually changed
git diff --name-only

# See the actual content changes
git diff [filename]

# Verify specific text appears
grep "expected_text" file.txt
```

**REJECT YOUR OWN WORK IF:**
- git diff shows 0 files changed
- Plan requires text "ABC" but grep doesn't find it
- You modified different files than the plan specified
- You only partially completed a task

### Phase 4: FINAL VALIDATION (MANDATORY)
```bash
# Run this BEFORE reporting
git diff --stat

# If output shows 0 files, report FAILURE immediately
# If files don't match plan, report FAILURE immediately
# Only report SUCCESS if all plan tasks complete AND git shows changes
```

## ❌ AUTO-FAIL CONDITIONS

You MUST report FAILURE if:
1. `git diff --name-only` returns EMPTY (no files changed)
2. Any required file from plan is NOT in git diff output
3. Any file in git diff was NOT in the plan
4. Plan asks for text "X" but grep/Read shows text "Y" instead
5. You don't show tool execution output for each change
6. You claim changes without using Read/Edit/Write tools

## ✅ SUCCESS CRITERIA

Report SUCCESS ONLY if:
1. Every task in plan is completed
2. Every file mentioned in plan appears in `git diff --name-only`
3. `git diff` shows actual content changes matching the plan
4. All Read/Edit/Write tools show proper execution
5. You can show Before/After content for each modification
6. No file was modified that wasn't in the plan

---

## 📋 Task Context
$ARGUMENT_1

---

## Plan File
Path: `$ARGUMENT_2`

Read this file completely and understand every requirement.

---

## Execution Strategy
$ARGUMENT_2

## Expected Report Format

```
## Implementation Report

Files Changed:
- [file1.txt] - [what changed]
- [file2.py] - [what changed]

Verification Results:
✓ [Task 1]: [verification result]
✓ [Task 2]: [verification result]
✓ [Task 3]: [verification result]

Git Diff Output:
[INSERT ACTUAL OUTPUT HERE]

Status: ✅ COMPLETED / ❌ FAILED
```

If implementation FAILED at any step, report it clearly with reason.