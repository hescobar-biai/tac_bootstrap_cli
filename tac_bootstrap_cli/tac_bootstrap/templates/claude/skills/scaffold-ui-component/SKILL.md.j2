---
name: scaffold-ui-component
description: Scaffold a new React UI component following project styling conventions. Use when creating new UI primitives, domain components, or reusable widgets. Triggers on requests like "create a component", "add a new UI element", "build a card/button/modal/dropdown", or "scaffold component".
---

# Scaffold UI Component

Generate React UI components following project styling conventions.

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `components_dir` | Root directory for components | `frontend/components/` |
| `styling` | Styling approach (from ADRs) | `Tailwind`, `CSS Modules`, `styled-components` |
| `utils_path` | Path to utility helpers | `@/lib/utils` |
| `file` | Target component file from the spec | `frontend/components/ui/card.tsx` |

If no spec is provided, detect the styling approach from project ADRs or existing code.

## Component Placement

| Type | Path | Examples |
|------|------|----------|
| UI primitive | `<components-dir>/ui/` | card, button, modal, sortable-table |
| Domain component | `<components-dir>/` | summary-card, navbar, date-range-picker |
| Grouped feature | `<components-dir>/<feature>/` | charts/, filters/ |

## File Naming

- Kebab-case: `my-component.tsx`
- One component per file; named export matching PascalCase of filename

## Component Template

```tsx
import { cn } from "<utils-path>";

interface MyComponentProps {
  children: React.ReactNode;
  className?: string;
}

export function MyComponent({ children, className, ...props }: MyComponentProps) {
  return (
    <div
      className={cn(
        "base-classes-here",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
```

## Key Patterns

### Class merging helper

Always use the project's class merging utility (e.g., `cn()` wrapping `clsx` + `tailwind-merge`) to combine base styles with caller overrides:

```tsx
className={cn(
  "rounded-lg border bg-white shadow-sm dark:bg-slate-800",
  className
)}
```

### Dark mode

Use dark mode variants on every color utility. Follow the project's color scale conventions:

```tsx
// Text
"text-slate-900 dark:text-white"           // primary
"text-slate-600 dark:text-slate-400"        // secondary
"text-slate-500 dark:text-slate-400"        // muted

// Backgrounds
"bg-white dark:bg-slate-800"               // card surface
"bg-slate-50 dark:bg-gray-900"             // page background

// Borders
"border-slate-200 dark:border-slate-700"   // standard
"divide-slate-200 dark:divide-slate-700"   // table rows
```

### Z-index for overlays

Use `z-50` for dropdowns, modals, popovers.

### Compound components

For complex UI, use multiple named exports from one file (Card pattern):

```tsx
export function Card({ children, className, ...props }: CardProps) { ... }
export function CardHeader({ children, className, ...props }: CardProps) { ... }
export function CardTitle({ children, className, ...props }: Props) { ... }
export function CardContent({ children, className, ...props }: CardProps) { ... }
```

### Generic components

For data-driven components, use TypeScript generics:

```tsx
export interface Column<T> {
  key: keyof T | string;
  header: string;
  sortable?: boolean;
  render?: (value: any, row: T) => React.ReactNode;
}

export function SortableTable<T extends Record<string, any>>({
  data, columns, ...
}: SortableTableProps<T>) { ... }
```

### Interactive states

```tsx
"hover:bg-slate-50 dark:hover:bg-slate-700/50"     // row hover
"cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-700/50 transition-colors select-none"  // clickable header
```

## Checklist

1. File in correct directory per type
2. Class merging utility used for all className composition
3. `className` prop accepted for caller overrides
4. Dark mode variant on every color utility
5. Project color scale for neutrals
6. Named export (not default export)
7. Props interface defined with explicit types
