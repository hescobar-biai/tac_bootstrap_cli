# Product Owner - Feature Specification

Create a new product specification for the `Task` using the exact `Specification Format`. Follow the `Instructions` to create the specification.

## Instructions

- IMPORTANT: You are acting as a Product Owner. Your focus is on WHAT to build and WHY, not HOW.
- IMPORTANT: You're creating a product specification that will be handed off to a Tech Lead for technical planning.
- DO NOT include technical implementation details, file paths, or code architecture decisions.
- Focus on: user value, business context, acceptance criteria, and functional requirements.
- Use your reasoning: THINK HARD about the user's needs, edge cases from a user perspective, and what "done" looks like.
- Write acceptance criteria in Gherkin format - these will become the basis for tests.
- Be explicit about what is OUT of scope to prevent scope creep.
- IMPORTANT: Replace every instruction inside angle brackets with your reasoned content. Add as much detail as needed.
- If you need clarification about business requirements, list your questions in the `Open Questions` section.

## Specification Format

```md
## 📋 Product Specification

### 1️⃣ User Story
---
<write a user story following the format. Think about who benefits most from this feature and what value they get>

As a <identify the primary user role or persona who will use this feature>
I want to <describe the capability or action the user wants to perform>
So that <explain the business value or benefit the user receives>

### 2️⃣ Context & Motivation
---

#### Problem Statement
<think deeply about the user's perspective and describe:
- What specific pain point or frustration does the user experience today?
- What task is difficult, tedious, or impossible without this feature?
- What opportunity are we missing by not having this?
Be specific and focus on the human impact, not technical limitations.>

#### Why Now?
<reason about the timing and urgency:
- What triggered this request or made it a priority?
- What is the cost of delay - what happens if we don't do this?
- How does this align with current product priorities or company goals?>

#### Success Metrics
<define 2-4 measurable outcomes that indicate this feature is successful. Think about:
- User adoption metrics (usage, engagement)
- Business metrics (conversion, retention, revenue)
- Efficiency metrics (time saved, errors reduced)
If metrics are not applicable for this type of task, explain why.>

### 3️⃣ Functional Requirements
---

#### Core Requirements
<list the must-have functionality. For each requirement ask yourself: "If we don't have this, does the feature still deliver value?" If no, it's a core requirement. Be specific and actionable.>

#### Nice-to-Have (Future Considerations)
<list functionality that adds value but isn't essential for the initial release. These could become follow-up tasks or future enhancements.>

### 4️⃣ Acceptance Criteria (Gherkin)
---

<write testable scenarios from the USER's perspective using Gherkin format.
Focus on BEHAVIOR and OUTCOMES, not implementation details.
Think through the complete user journey and edge cases.
Create as many scenarios as needed to fully specify the expected behavior.>

#### Scenario 1: <name this scenario - describe the happy path, the most common successful use case>
- Given <describe the initial user context, state, or preconditions>
- And <add additional context if needed, remove if not>
- When <describe the specific user action or trigger>
- Then <describe what the user sees, experiences, or what outcome occurs>
- And <add additional outcomes if needed, remove if not>

#### Scenario 2: <name this scenario - describe an alternate successful path or variation>
- Given <preconditions for this alternate flow>
- When <different user action or different context>
- Then <expected outcome for this path>

#### Scenario 3: <name this scenario - describe an important edge case>
<think about boundary conditions, unusual but valid inputs, or less common user situations

- Given <edge case context>
- When <user action in this edge case>
- Then <expected behavior - the system should handle this gracefully>

#### Scenario 4: <name this scenario - describe error handling from user perspective>
<think about what could go wrong and how the user should experience errors>

- Given <context that will lead to an error or invalid state>
When <user action>
Then <user-friendly error experience - what do they see?>
And <recovery options - what can the user do next?>

<add more scenarios as needed. Consider and include scenarios for:
- Empty states (what happens when there's no data?)
- Boundary conditions (maximum/minimum values, character limits)
- Permission/access scenarios (what if user doesn't have access?)
- First-time user experience (onboarding, empty states)
- Returning user experience (saved state, preferences)
- Concurrent usage (multiple users, multiple tabs)
- Offline/connectivity issues (if applicable to this feature)
Remove this instruction block in the final output.>

### 5️⃣ UI/UX Requirements
---

#### User Flow
<describe the step-by-step journey a user takes. Walk through the feature from start to finish:
1. Where does the user start? (entry point)
2. What actions do they take?
3. What does the system show at each step?
4. How does the user know they've completed the task?>

#### UI States
<list all visual states the interface must handle. For each state, describe what the user sees.>
- Loading: <what does the user see while waiting? Consider skeleton screens, spinners, progress indicators>
- Empty: <what does the user see when there's no data? Consider helpful messaging, calls to action>
- Success: <what does the user see when the action completes successfully? Consider confirmation, next steps>
- Error: <what does the user see when something fails? Consider error messages, recovery actions>
- Partial: <what does the user see with incomplete data? Consider progressive disclosure, placeholders>
<add additional states if relevant to this feature>

#### Mockups/Wireframes
<if designs exist, link to them. If not, describe the visual requirements in enough detail for a designer or developer to understand the intent. Consider layout, key components, and visual hierarchy.>

#### Accessibility Requirements
<list specific accessibility requirements. Consider:
- Keyboard navigation
- Screen reader support
- Color contrast
- Focus management
- ARIA labels
If you're unsure, list "Follow WCAG 2.1 AA standards" as minimum.>

### 6️⃣ Out of Scope
---
<CRITICAL: explicitly list what this feature does NOT include.
Think about what someone might assume is included but isn't.
This prevents scope creep and sets clear expectations.
Be specific - vague exclusions lead to misunderstandings.>

### 7️⃣ Dependencies (Product/Business)
---
<identify any non-technical dependencies that could block or affect this work>
- Requires decision on: <list any pending business decisions that must be made>
- Depends on: <list other features, external factors, or business processes this depends on>
- Stakeholder approval needed: <list stakeholders who must approve before or after implementation>
<if there are no dependencies, state "No product dependencies identified">

### 8️⃣ Open Questions (Product)
---
<list questions that need answers before development can proceed effectively.
These should be product/business questions, not technical questions.
For each question, note who might have the answer if known.>
```

---

## Task

$ARGUMENTS
