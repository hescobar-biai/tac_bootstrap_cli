---
name: scaffold-frontend-page
description: Scaffold a frontend page with data fetching, state management, and layout following project conventions. Use when creating a new page, adding a route, or building a dashboard view. Triggers on requests like "create a page", "add a new route", "scaffold page", "build a dashboard", or "new frontend view".
---

# Scaffold Frontend Page

Generate frontend pages following project ADRs and conventions.

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `frontend_dir` | Root directory for frontend code | `frontend/` |
| `framework` | Frontend framework (from ADRs) | `Next.js App Router`, `React SPA`, `Vue` |
| `state_management` | State approach (from ADRs) | `React hooks`, `Redux`, `Zustand` |
| `file` | Target page file from the spec | `frontend/app/analytics/page.tsx` |

If no spec is provided, detect the frontend framework from project ADRs or existing code.

## Step 1: Create Route File

Create `<frontend-dir>/app/<route>/page.tsx` (or equivalent route file per framework).

For React-based frameworks, pages that manage client state start with `"use client"`.

## Step 2: State Variables

Declare all state per project state management approach:

```tsx
// Filter state
const [startDate, setStartDate] = useState<string>("");
const [endDate, setEndDate] = useState<string>("");
const [filters, setFilters] = useState<string[]>([]);

// Data state
const [data, setData] = useState<DataType[]>([]);
const [summary, setSummary] = useState<SummaryType | null>(null);

// UI state
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
```

## Step 3: Data Fetching Effects

Two effects pattern — one for initial defaults, one for fetching on filter change:

```tsx
// Initialize defaults
useEffect(() => {
  const now = new Date();
  const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
  setEndDate(now.toISOString().split("T")[0]);
  setStartDate(thirtyDaysAgo.toISOString().split("T")[0]);
}, []);

// Fetch when filters change
useEffect(() => {
  if (startDate && endDate) {
    fetchData();
  }
}, [startDate, endDate, filters]);
```

## Step 4: fetchData with Parallel Calls

Parallel API calls for all data needed:

```tsx
async function fetchData() {
  setLoading(true);
  setError(null);
  try {
    const [summaryData, trendsData, breakdownData] = await Promise.all([
      getSummary(startDate, endDate, filters),
      getTrends(startDate, endDate, "daily", filters),
      getBreakdown(startDate, endDate, filters),
    ]);
    setSummary(summaryData);
    setTrends(trendsData);
    setBreakdown(breakdownData);
  } catch (err) {
    setError(err instanceof Error ? err.message : "Failed to fetch data");
  } finally {
    setLoading(false);
  }
}
```

## Step 5: Computed Values

Derive aggregations and chart transforms from raw data:

```tsx
const chartData = useMemo(() =>
  trends.reduce((acc, item) => {
    const existing = acc.find(d => d.period === item.period);
    if (existing) {
      existing.value += item.value;
    } else {
      acc.push({ ...item });
    }
    return acc;
  }, [] as typeof trends).sort((a, b) => a.period.localeCompare(b.period)),
  [trends]
);
```

## Step 6: Layout Structure

Standard layout: Navigation -> Header with filters -> Content sections.

```tsx
return (
  <div className="min-h-screen bg-slate-50 dark:bg-gray-900">
    <Navbar />
    <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Header + filters row */}
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Page Title</h1>
          <p className="mt-2 text-slate-600 dark:text-slate-400">Description</p>
        </div>
        <div className="flex items-center gap-4">
          {/* Filter components */}
        </div>
      </div>

      {/* Error banner */}
      {error && (
        <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 dark:border-red-800 dark:bg-red-900/20">
          <p className="text-sm text-red-800 dark:text-red-400">{error}</p>
        </div>
      )}

      {/* Loading spinner */}
      {loading && !data ? (
        <div className="flex min-h-[400px] items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
        </div>
      ) : (
        <>
          {/* Summary cards row */}
          <div className="mb-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <SummaryCard title="Metric" value={formatValue(val)} icon={<Icon />} />
          </div>

          {/* Charts grid */}
          <div className="mb-8 grid gap-6 lg:grid-cols-2">
            <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800">
              <h2 className="mb-4 text-lg font-semibold text-slate-900 dark:text-white">Chart Title</h2>
              <MyChart data={chartData} />
            </div>
          </div>

          {/* Tables */}
          <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800">
            <h2 className="mb-4 text-lg font-semibold text-slate-900 dark:text-white">Table Title</h2>
            <SortableTable data={tableData} columns={columns} />
          </div>
        </>
      )}
    </main>
  </div>
);
```

## Step 7: Register in Navigation

Add the route link to the navigation component (e.g., `<frontend-dir>/components/navbar.tsx`).

## API Client Functions

API functions live in `<frontend-dir>/lib/api.ts` (or equivalent). Pattern:

```tsx
export async function getItems(startDate: string, endDate: string, filters: string[] = []): Promise<ItemType[]> {
  const params = new URLSearchParams({ start_date: startDate, end_date: endDate });
  filters.forEach((f) => params.append('filters', f));
  const response = await fetch(`${API_BASE}/api/v1/domain/items?${params}`);
  return handleResponse<ItemType[]>(response);
}
```

## Detailed Patterns

For the annotated dashboard page skeleton and API client patterns, see [references/page-pattern.md](references/page-pattern.md).

## Checklist

1. Client directive at top of page file (if required by framework)
2. All state via project state management approach
3. Data fetching effect with dependency array on filter state
4. Parallel API calls for independent data
5. Computed/memoized values for derived data
6. Layout: Navigation -> max-width main -> filters -> cards -> charts -> tables
7. Dark mode on all styled elements
8. Loading spinner and error banner
9. Route registered in navigation
