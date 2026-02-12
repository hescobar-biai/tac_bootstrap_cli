# Page Pattern Reference

## Table of Contents
- [Dashboard Page Skeleton](#dashboard-page-skeleton)
- [API Client Function Pattern](#api-client-function-pattern)

---

## Dashboard Page Skeleton

Source: `<frontend-dir>/app/<route>/page.tsx`

Annotated skeleton showing the complete page structure:

```tsx
"use client";

// 1. IMPORTS — React hooks, components, API functions, utils
import { useEffect, useState } from "react";
import { Navbar } from "@/components/navbar";
import { SummaryCard } from "@/components/summary-card";
import { TrendChart } from "@/components/charts/trend-chart";
import { BreakdownChart } from "@/components/charts/breakdown-chart";
import { DateRangePicker } from "@/components/date-range-picker";
import { CategoryPicker } from "@/components/category-picker";
import { FilterPicker } from "@/components/filter-picker";
import {
  getSummary, getTrends, getCategoryBreakdown, getTopItems,
  type SummaryMetrics, type TrendData, type CategoryBreakdown, type TopItem,
} from "@/lib/api";
import { formatValue, formatNumber } from "@/lib/utils";
import { ChartIcon, ListIcon, DatabaseIcon, TrendingUpIcon } from "@/components/icons";
import { SortableTable } from "@/components/ui/sortable-table";
import type { Column } from "@/components/ui/sortable-table";

// 2. DEFAULT EXPORT — pages use default export (components use named)
export default function DashboardPage() {

  // 3. STATE — filter state, data state, UI state
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [categories, setCategories] = useState<string[]>(["all"]);
  const [filters, setFilters] = useState<string[]>([]);
  const [summary, setSummary] = useState<SummaryMetrics | null>(null);
  const [trends, setTrends] = useState<TrendData[]>([]);
  const [categoryBreakdown, setCategoryBreakdown] = useState<CategoryBreakdown[]>([]);
  const [topItems, setTopItems] = useState<TopItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 4. EFFECT: Initialize defaults (runs once)
  useEffect(() => {
    const now = new Date();
    const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
    setEndDate(now.toISOString().split("T")[0]);
    setStartDate(thirtyDaysAgo.toISOString().split("T")[0]);
  }, []);

  // 5. EFFECT: Fetch on filter change
  useEffect(() => {
    if (startDate && endDate) {
      fetchData();
    }
  }, [startDate, endDate, categories, filters]);

  // 6. FETCH: Promise.all for parallel API calls
  async function fetchData() {
    setLoading(true);
    setError(null);
    try {
      const [summaryData, trendsData, breakdownData, topData] = await Promise.all([
        getSummary(startDate, endDate, categories, filters),
        getTrends(startDate, endDate, "daily", "category", categories, filters),
        getCategoryBreakdown(startDate, endDate, categories, filters),
        getTopItems(startDate, endDate, 10, categories, filters),
      ]);
      setSummary(summaryData);
      setTrends(trendsData);
      setCategoryBreakdown(breakdownData);
      setTopItems(topData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch data");
    } finally {
      setLoading(false);
    }
  }

  // 7. HANDLERS: one per filter component
  function handleDateRangeChange(start: string, end: string) {
    setStartDate(start);
    setEndDate(end);
  }

  // 8. RENDER: structured layout
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-gray-900">
      <Navbar />
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">

        {/* Header row: title + filter pickers */}
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Analytics Dashboard</h1>
            <p className="mt-2 text-slate-600 dark:text-slate-400">Monitor your key metrics</p>
          </div>
          <div className="flex items-center gap-4">
            <FilterPicker onSelect={handleFilterChange} categories={categories} />
            <CategoryPicker onSelect={handleCategoryChange} defaultCategories={["all"]} />
            <DateRangePicker onSelect={handleDateRangeChange} />
          </div>
        </div>

        {/* Error banner */}
        {error && (
          <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 dark:border-red-800 dark:bg-red-900/20">
            <p className="text-sm text-red-800 dark:text-red-400">{error}</p>
          </div>
        )}

        {/* Loading state */}
        {loading && !summary ? (
          <div className="flex min-h-[400px] items-center justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
          </div>
        ) : (
          <>
            {/* Summary cards: 4-column grid */}
            <div className="mb-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              <SummaryCard title="Total Value" value={formatValue(summary?.total_value || 0)} icon={<ChartIcon />} />
              <SummaryCard title="Total Items" value={formatNumber(summary?.total_items || 0)} icon={<ListIcon />} />
              {/* ... more cards ... */}
            </div>

            {/* Charts: 2-column grid, each in card container */}
            <div className="mb-8 grid gap-6 lg:grid-cols-2">
              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800">
                <h2 className="mb-4 text-lg font-semibold text-slate-900 dark:text-white">Trends</h2>
                <TrendChart data={aggregatedTrends} />
              </div>
              <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800">
                <h2 className="mb-4 text-lg font-semibold text-slate-900 dark:text-white">By Category</h2>
                <BreakdownChart data={breakdownData} />
              </div>
            </div>

            {/* Table: full width in card container */}
            <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800">
              <h2 className="mb-4 text-lg font-semibold text-slate-900 dark:text-white">Top Items</h2>
              <SortableTable
                data={topItems}
                columns={itemColumns}
                rowKey="item_id"
                initialSortKey="value"
                initialSortDirection="desc"
              />
            </div>
          </>
        )}
      </main>
    </div>
  );
}
```

---

## API Client Function Pattern

Source: `<frontend-dir>/lib/api.ts`

```tsx
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || `HTTP ${response.status}`);
  }
  return response.json();
}

// Pattern: typed params, URLSearchParams, array params via forEach append
export async function getTrends(
  startDate: string,
  endDate: string,
  granularity: 'daily' | 'weekly' | 'monthly' = 'daily',
  groupBy: 'category' | 'source' = 'category',
  categories: string[] = ['all'],
  filters: string[] = [],
): Promise<TrendData[]> {
  const params = new URLSearchParams({
    start_date: startDate,
    end_date: endDate,
    granularity,
    group_by: groupBy,
  });
  // Array params: append each value with same key
  categories.forEach((c) => params.append('categories', c));
  filters.forEach((f) => params.append('filters', f));

  const response = await fetch(`${API_BASE}/api/v1/domain/trends?${params}`);
  return handleResponse<TrendData[]>(response);
}
```

Key elements:
- `API_BASE` from env var with localhost fallback
- Generic `handleResponse<T>` for type-safe error handling
- `URLSearchParams` for scalar params, `.append()` for array params
- Return type matches backend response model
