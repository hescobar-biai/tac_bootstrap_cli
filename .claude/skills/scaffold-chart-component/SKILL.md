---
name: scaffold-chart-component
description: Scaffold a chart component with dark mode support following project conventions. Use when creating line charts, bar charts, pie charts, or composed charts. Triggers on requests like "create a chart", "add a graph", "visualize data", "build a chart component", or "scaffold chart".
---

# Scaffold Chart Component

Generate chart components following project ADRs and conventions.

## Input

Configuration is read from the invoking spec's frontmatter or project context:

| Field | Description | Example |
|-------|-------------|---------|
| `charts_dir` | Directory for chart components | `frontend/components/charts/` |
| `charting_library` | Charting library (from ADRs) | `Recharts`, `Chart.js`, `D3`, `Nivo` |
| `utils_path` | Path to utility/formatting helpers | `@/lib/utils` |
| `file` | Target chart file from the spec | `frontend/components/charts/trend-chart.tsx` |

If no spec is provided, detect the charting library from project ADRs or existing code.

## Chart Type Selection

| Type | When to use | Component |
|------|------------|-----------|
| LineChart | Time series, trends | Line chart component |
| BarChart | Category comparison, breakdown | Bar chart component |
| PieChart | Part-of-whole, distribution | Pie chart component |
| ComposedChart | Mixed (line + bar on same axes) | Composed chart component |

## File Placement

All charts go in `<charts-dir>/` with kebab-case naming: `my-chart.tsx`

## Component Template

```tsx
"use client";

import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from "recharts";
import { formatValue, formatDate } from "<utils-path>";

interface ChartDataItem {
  period: string;
  value: number;
}

interface MyChartProps {
  data: ChartDataItem[];
  height?: number;
}

export function MyChart({ data, height = 300 }: MyChartProps) {
  const chartData = data.map((item) => ({
    ...item,
    formattedDate: formatDate(item.period),
  }));

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" className="stroke-slate-200 dark:stroke-slate-700" />
        <XAxis
          dataKey="formattedDate"
          className="text-sm text-slate-600 dark:text-slate-400"
          tick={{ fill: "currentColor" }}
        />
        <YAxis
          className="text-sm text-slate-600 dark:text-slate-400"
          tick={{ fill: "currentColor" }}
          tickFormatter={(value) => formatValue(value)}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "rgba(15, 23, 42, 0.9)",
            border: "1px solid rgba(71, 85, 105, 0.5)",
            borderRadius: "8px",
            color: "#e2e8f0",
          }}
          itemStyle={{ color: "#e2e8f0" }}
          labelStyle={{ color: "#94a3b8" }}
          formatter={(value: number | undefined, name?: string) => {
            const val = value ?? 0;
            return [formatValue(val), name];
          }}
          labelFormatter={(label) => `Date: ${label}`}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="value"
          name="Metric"
          stroke="#2563eb"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

## Critical: Dark Mode Tooltip

Always use this exact `contentStyle`/`itemStyle`/`labelStyle` for tooltip dark mode:

```tsx
contentStyle={{
  backgroundColor: "rgba(15, 23, 42, 0.9)",   // slate-900 at 90%
  border: "1px solid rgba(71, 85, 105, 0.5)",  // slate-600 at 50%
  borderRadius: "8px",
  color: "#e2e8f0",                             // slate-200
}}
itemStyle={{ color: "#e2e8f0" }}                // slate-200
labelStyle={{ color: "#94a3b8" }}               // slate-400
```

## Axis Formatting

Use project utility helpers for tick formatting:

| Data type | Formatter |
|-----------|-----------|
| Currency | `(v) => formatCurrency(v)` |
| Percentage | `(v) => \`${v.toFixed(1)}%\`` |
| Large numbers | `(v) => formatNumber(v)` |
| Data sizes | `(v) => formatSize(v)` |
| Dates | `(v) => formatDate(v)` |

## Dual Y-Axis

Add `yAxisId="right"` on the secondary Line/Bar and a second `<YAxis>`:

```tsx
<YAxis yAxisId="right" orientation="right" tickFormatter={(v) => `${v.toFixed(0)}%`} />
<Line dataKey="secondary_metric" yAxisId="right" stroke="#10b981" />
```

## Color Palette

| Use | Hex | Tailwind |
|-----|-----|----------|
| Primary metric | `#2563eb` | blue-600 |
| Secondary metric | `#10b981` | emerald-500 |
| Tertiary | `#f59e0b` | amber-500 |
| Grid lines | CSS class | `stroke-slate-200 dark:stroke-slate-700` |

## Detailed Patterns

For annotated examples of LineChart (dual Y-axis, trends) and BarChart (breakdown), see [references/chart-patterns.md](references/chart-patterns.md).

## Checklist

1. Client directive at top (if required by framework)
2. `ResponsiveContainer` wraps the chart
3. Dark tooltip styling applied
4. CartesianGrid uses CSS class for dark mode
5. Axis ticks use `fill: "currentColor"` for theme support
6. Format helpers from project utilities
7. Named export, file in `<charts-dir>/`
