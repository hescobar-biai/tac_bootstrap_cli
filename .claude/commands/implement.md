# Implement the following plan
Execute each task in the plan step-by-step, then report results.

## CRITICAL INSTRUCTIONS - READ CAREFULLY

**Your job is to ACTUALLY EXECUTE the plan, not simulate it.**

### Step 1: READ THE PLAN
Read the entire plan file and understand:
- What files need to be modified
- What text/code needs to be added/changed
- What the acceptance criteria are
- What verification steps are required

### Step 2: EXECUTE EACH TASK IN ORDER
For each task in the plan:
1. **FIRST**: Use Read to check current file content
2. **THEN**: Use Edit or Write to make the modification
3. **THEN**: Use Read again to confirm the change was applied
4. **THEN**: Show the file content with the modification visible
5. **CRITICAL**: Use tools EVERY TIME - don't skip to reporting

⚠️ **IMPORTANT**: If you don't see tool execution output showing actual file content being modified, you failed.

### Step 3: VERIFY EACH CHANGE
After each modification:
- Read the file to confirm the change was applied
- Check the modification matches the plan requirements
- Look for the specific text/changes mentioned in plan
- If verification fails, the change wasn't made correctly

### Step 4: VALIDATE WITH GIT
```bash
git diff --name-only          # Show files that changed
git diff --stat               # Show change statistics
git diff [filename]           # Show actual content changes
```

**CRITICAL**: If `git diff --name-only` is EMPTY, you failed to implement anything.

### Step 5: REPORT WHAT YOU ACTUALLY DID
**ONLY report changes that appear in `git diff --stat`**

Do NOT claim:
- "I added text to file" if git diff shows 0 changes
- "File modified" if it doesn't appear in `git diff`
- "2 lines added" if git diff shows different number

Report EXACTLY what git shows.

## ⚠️ FAILURE CONDITIONS (report FAILURE if any occur)

1. **No changes made**: `git diff --name-only` returns empty
2. **Wrong files changed**: Files modified that aren't in the plan
3. **Content missing**: Plan says "add text X" but `grep` shows X not in file
4. **Incomplete changes**: Plan has 3 tasks but only 2 completed
5. **Verification failed**: Spec includes verification command that fails

## Plan
$ARGUMENTS

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