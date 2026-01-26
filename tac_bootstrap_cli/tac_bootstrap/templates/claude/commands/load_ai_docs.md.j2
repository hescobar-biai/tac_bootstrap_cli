# Load AI Documentation

Load AI documentation from the `ai_docs/doc/` directory into context using specialized exploration agents. This command efficiently ingests TAC methodology documentation, project-specific AI patterns, and guidelines to help agents understand the project's AI development approach.

## Variables

doc_filter: $ARGUMENT (optional) - Filter for specific documents (e.g., "1-3" for docs 1-3, "5" for doc 5)

## Instructions

**AI Documentation Structure:**
- TAC projects typically have documentation in: `ai_docs/doc/`
- TAC courses are numbered 1-8 (doc/1.md through doc/8.md)
- Projects may include additional custom documentation files
- Documentation covers AI methodologies, patterns, workflows, and best practices

**Documentation Path:**
- Expected directory: `ai_docs/doc/`
- Contains markdown files with AI development guidelines
- Files may include TAC course materials and project-specific patterns

**Filtering Syntax:**
- No filter: Load all documents from ai_docs/doc/
- Single doc: `doc_filter=5` loads only doc/5.md
- Range: `doc_filter=1-3` loads doc/1.md, doc/2.md, and doc/3.md
- Multiple ranges: `doc_filter=1-3,5,7-8` loads docs 1, 2, 3, 5, 7, 8

**Loading Strategy:**
- Use Task tool with `subagent_type=Explore` for efficient documentation scanning
- The Explore agent is optimized for reading and understanding large documentation sets
- Set thoroughness level to "medium" for balanced exploration
- Load filtered documents or all if no filter specified

## Run

1. **Determine documentation path:**
   - Use default path: `ai_docs/doc/`
   - Verify directory exists before proceeding
   - If directory is missing, report error and suggest creating it

2. **Parse doc_filter argument:**
   - If no doc_filter provided: prepare to load all documents
   - If single number (e.g., "5"): load only that document
   - If range (e.g., "1-3"): expand to list [1, 2, 3]
   - If multiple ranges (e.g., "1-3,5"): expand to [1, 2, 3, 5]

3. **Use Task tool with Explore agent:**
   - Launch exploration agent with appropriate prompt
   - Prompt should request reading documentation files
   - If filter specified: mention specific documents to focus on
   - Request summary of key concepts, methodologies, and patterns
   - Set thoroughness to "medium" for comprehensive but efficient scanning

4. **Process exploration results:**
   - Agent will read and understand documentation
   - Context will be loaded with documentation content
   - Agent may summarize key findings

5. **Report summary:**
   - List which documents were loaded
   - Provide count of files processed
   - Note any missing or skipped documents
   - Highlight key topics found in the documentation

## Examples

**Example 1: Load all AI documentation**
```
User: /load_ai_docs
Agent: Loading all AI documentation from ai_docs/doc/...
       Launching Explore agent to scan documentation...
       Loaded 8 documents: doc/1.md through doc/8.md
       Key topics: TAC methodology, agentic workflows, testing patterns
```

**Example 2: Load specific TAC courses**
```
User: /load_ai_docs doc_filter=1-3
Agent: Loading TAC courses 1-3 from ai_docs/doc/...
       Launching Explore agent to scan filtered documentation...
       Loaded 3 documents: doc/1.md, doc/2.md, doc/3.md
       Key topics: Foundation concepts, basic workflows, architecture patterns
```

**Example 3: Load single document**
```
User: /load_ai_docs doc_filter=5
Agent: Loading doc/5.md from ai_docs/doc/...
       Launching Explore agent to scan documentation...
       Loaded 1 document: doc/5.md
       Key topics: Advanced testing strategies, CI/CD integration
```

**Example 4: Load multiple ranges**
```
User: /load_ai_docs doc_filter=1-2,5,7-8
Agent: Loading selected documents from ai_docs/doc/...
       Launching Explore agent to scan filtered documentation...
       Loaded 5 documents: doc/1.md, doc/2.md, doc/5.md, doc/7.md, doc/8.md
       Key topics: Foundations, testing, deployment, optimization
```

**Example 5: Handle missing directory**
```
User: /load_ai_docs
Agent: Error: ai_docs/doc/ directory not found
       The ai_docs/doc/ directory is expected to contain AI documentation.
       Please create the directory and add documentation files.
```

## Report

Report to the user:

1. **Loading Summary:**
   - Documentation path used
   - Filter applied (if any)
   - Number of documents processed

2. **Loaded Documents:**
   - List of successfully loaded files with paths
   - Example: doc/1.md, doc/2.md, doc/3.md

3. **Key Topics Found:**
   - Brief summary of main topics discovered
   - Methodologies and patterns identified
   - Areas of focus in the documentation

4. **Missing Documents:**
   - Note any documents that were expected but not found
   - Suggest creating missing documentation if needed

**Format:**
```
AI documentation loaded from: ai_docs/doc/
Filter applied: {filter or "none (all documents)"}
Documents loaded: {count}

Successfully loaded:
  - doc/1.md
  - doc/2.md
  - doc/3.md
  - ...

Key topics identified:
  - {topic_1}
  - {topic_2}
  - {topic_3}

Missing documents: {count or "none"}
  - {missing_doc_1}
  - ...

Documentation context successfully loaded. Agents can now reference TAC methodology and project-specific AI patterns.
```
