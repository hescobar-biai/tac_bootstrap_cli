---
name: react-frontend
description: "Generates React 19 components, hooks, pages, and data tables following Celes project conventions. Use when building UI features, forms, dashboards, DataTable views, or supply chain data visualizations with TanStack Query, MUI X Data Grid Premium (DataTable.Root), TailwindCSS 4.1 custom theme, Ky HTTP client, and Valibot validation."
---

# React Frontend Skill

Scaffolds production-ready React 19 components, custom hooks, data tables, and full page layouts following Celes project conventions. Designed for supply chain, logistics, and enterprise dashboard applications with TypeScript strict mode, MUI X Data Grid Premium, TanStack ecosystem, and custom TailwindCSS theme.

## Instructions

### Prerequisites

- React 19.x with React Compiler enabled (`'use memo'` directive)
- TypeScript 5.9+ in strict mode (no `any` — use `unknown` + type guards)
- TanStack Query 5.90+ for server state management
- TanStack Router 1.132+ for file-based routing
- TanStack Form + Valibot for form validation
- Zustand 5 with localStorage persistence for client state
- MUI 7 + MUI X Data Grid Premium 8.19+
- TailwindCSS 4.1 with custom Celes color palette
- Ky HTTP client (NOT axios, NOT raw fetch)
- Vitest + React Testing Library + Playwright + MSW for testing
- react-i18next for internationalization (Spanish/English)
- clsx for conditional class names
- @tabler/icons-react for icons

### Workflow

1. **Understand the requirement**:
   - Determine what type of UI element is needed: component, hook, page, data table, or full feature
   - Identify the data source (API endpoint, Firestore, local state, or derived)
   - Clarify if a DataTable is needed (use DataTable.Root composition, NEVER DataGridPremium directly)
   - Check if forms are needed (TanStack Form + Valibot, schemas in `helpers.ts`)
   - Identify the module: Administration, WorkArea, Planning, ReportsAndAnalitycs, Dashboard

2. **Determine file placement** (see [reference.md](reference.md) > Code Organization):
   - Pages: `src/pages/{Module}/{PageName}/{PageName}.tsx` + `index.ts`
   - Routes: `src/routes/_layout.{path}.index.lazy.tsx` (+ `.index.tsx` if `validateSearch`/`loader` needed)
   - Page-local components: `{Page}/components/Component.tsx`
   - Module-shared components: `{Module}/common/Component.tsx`
   - Page-local hooks: `{Page}/hooks/useHook.ts`
   - Query/mutation options: `{Module}/queries.ts` or `{Page}/queries.ts`
   - Global shared: `src/components/`, `src/hooks/`, `src/types/`

3. **Select the appropriate template**:
   - **Component** (card, modal, badge): Use [templates/Component.tsx](templates/Component.tsx)
   - **Data fetching hook** (API integration with Ky + TanStack Query): Use [templates/useDataHook.ts](templates/useDataHook.ts)
   - **Dashboard page with DataTable** (filters + DataTable.Root + KPIs): Use [templates/DashboardPage.tsx](templates/DashboardPage.tsx)
   - For composite features, combine multiple templates

4. **Follow Celes project conventions**:
   - Use `clsx` for conditional class merging (NOT template literals)
   - Use Celes custom colors: `night-*`, `seasalt`, `ghostwhite`, `orangepeel-*`, `emerald-*`, `bittersweet-*`
   - Use Celes typography: `text-title-1`, `text-body-1`, `text-body-2`, `text-caption-1` (NOT `text-sm`/`text-base`/`text-lg`)
   - Use `~/` path alias for imports from `src/`
   - Named exports for components, `index.ts` exports only the main component
   - NEVER use `any` type — use `unknown` with type guards
   - All user-facing strings through `useTranslation` (react-i18next)
   - Use `useId()` for accessibility ID generation
   - Database IDs as list keys (NEVER array indices)
   - Form validation schemas in `helpers.ts` (NEVER inline in components)
   - JSDoc documentation on all exports

5. **Build data tables with DataTable.Root** (CRITICAL):
   - ALWAYS use `DataTable.Root` — NEVER use `DataGridPremium` directly
   - Required: `tableId` prop (stable, unique string)
   - Use `processApiColumns()` for API column mapping
   - Use `wrapActionsColDef()` for action columns (always pin right)
   - Use `useSearchPaginationModel()` for URL-persisted pagination
   - Use `useSortModelPersisted()` for localStorage-persisted sorting
   - Compose: `DataTable.Box` > `DataTable.Toolbar` > `DataTable.Table` + `DataTable.Footer` > `DataTable.Pagination`

6. **Integrate data with Ky + TanStack Query**:
   - Use `queryOptions()` and `mutationOptions()` in dedicated `queries.ts` files
   - Naming: `scenariosQueryOptions`, `createCampaignMutationOptions` (NO `get` prefix)
   - Inline fetch logic in `queryFn`/`mutationFn` using Ky: `api.get('endpoint/').json()`
   - Import query keys from `~/lib/queryKeys`
   - Use `stringifySearchParams` for query parameters
   - Handle loading/error states explicitly

7. **Build forms with TanStack Form + Valibot**:
   - Define schemas in `helpers.ts`: `export const myFormSchema = v.object({...})`
   - Infer types: `type MyFormValues = v.InferOutput<typeof myFormSchema>`
   - Use `useAppForm` from `~/lib/tanstackForm`
   - Validate search params with `validateSearch` in route files

8. **Test the component**:
   - Vitest + React Testing Library for unit/integration tests
   - Co-locate test files: `Component.test.tsx` next to `Component.tsx`
   - Query priority: `getByRole` > `getByLabelText` > `getByText` > `getByTestId`
   - Mock API with MSW (Mock Service Worker)
   - Test loading, error, and empty states
   - E2E with Playwright: `src/e2e/tests/{PageName}/{PageName}.spec.ts`

### Supporting Files

| File | Purpose |
|------|---------|
| [reference.md](reference.md) | Complete Celes patterns: DataTable.Root, Ky, TanStack Query/Router/Form, Zustand, TailwindCSS theme, code organization, testing, i18n, accessibility |
| [templates/Component.tsx](templates/Component.tsx) | TypeScript functional component with clsx, custom Tailwind theme, and JSDoc |
| [templates/useDataHook.ts](templates/useDataHook.ts) | Custom data fetching hook using Ky + TanStack Query queryOptions pattern |
| [templates/DashboardPage.tsx](templates/DashboardPage.tsx) | Full dashboard page with DataTable.Root composition, server pagination, and KPIs |

### Key Patterns

**DataTable.Root Composition**: ALL data tables use the `DataTable.Root` wrapper — NEVER `DataGridPremium` directly. The composition provides state persistence, standardized toolbar, quick search, and consistent styling.

**Server State vs Client State**: TanStack Query owns all server-fetched data (via Ky HTTP client). Zustand 5 with localStorage persistence owns UI-only state (sidebar open, selected tab, filter values). TanStack Form owns form state.

**React Compiler (`'use memo'`)**: React 19 with React Compiler is enabled. Use `'use memo'` directive at module level instead of manual `useMemo`/`useCallback`. Only add manual memoization after profiling confirms need.

**Type Safety**: No `any` type anywhere. Use `unknown` + type guards. Infer types from Valibot schemas with `v.InferOutput`. API types in `src/types/apiContracts.ts`.

**Custom Theme**: Use ONLY Celes custom Tailwind colors (`night-*`, `seasalt`, `ghostwhite`, `orangepeel-*`, `emerald-*`). NEVER use Tailwind defaults (`gray-*`, `neutral-*`). Use custom typography classes (`text-body-1`, NOT `text-sm`).

## Examples

### Example 1: Inventory Data Table with Server Pagination

User request:
```
Create an inventory management table that shows SKU, warehouse, quantity on hand, and reorder point. Include search by SKU and filter by warehouse.
```

You would:
1. Create file structure:
   ```
   src/pages/WorkArea/WorkAreaInventory/WorkAreaInventoryPage/
   ├── index.ts
   ├── WorkAreaInventoryPage.tsx
   ├── queries.ts
   ├── helpers.ts
   └── components/
       └── InventoryFilters.tsx
   ```
2. Define `inventoryQueryOptions` in `queries.ts` using Ky:
   ```typescript
   export const inventoryQueryOptions = (params: InventoryParams) =>
     queryOptions({
       queryKey: [INVENTORY, params],
       queryFn: async () => {
         const searchParams = stringifySearchParams(params)
         const response = (await api
           .get('inventory/items/', { searchParams })
           .json()) as ApiResponse<InventoryItem[]>
         return response.data
       },
     })
   ```
3. Build the page with `DataTable.Root`:
   ```tsx
   <DataTable.Root
     tableId="inventory-items-table"
     rows={data}
     columns={columns}
     pagination
     paginationMode="server"
     paginationModel={paginationModel}
     onPaginationModelChange={setPaginationModel}
     sortingMode="server"
     sortModel={sortModel}
     onSortModelChange={handleSortModelChange}
     rowCount={totalCount}
     loading={isLoading}
     isLoadingFirstTime={isPending}
   >
     <div className="h-full overflow-auto">
       <DataTable.Box>
         <DataTable.Toolbar>
           <DataTable.QuickSearch />
           <DataTable.ExportButton onClick={handleExport} />
           <DataTable.ColumnsPanelButton />
         </DataTable.Toolbar>
         <DataTable.Table />
       </DataTable.Box>
       <DataTable.Footer>
         <DataTable.Pagination />
       </DataTable.Footer>
     </div>
   </DataTable.Root>
   ```
4. Use `processApiColumns()` for column definitions, highlight low-stock rows
5. Add route: `src/routes/_layout.work-area.inventory.index.lazy.tsx`
6. All user-facing text through `useTranslation('workArea')`

### Example 2: Planning Form with Valibot Validation

User request:
```
Create a form for creating promotional campaigns with name, start/end dates, and discount percentage.
```

You would:
1. Define validation schema in `helpers.ts`:
   ```typescript
   import * as v from 'valibot'

   export const campaignFormSchema = v.object({
     name: v.pipe(v.string(), v.minLength(1, 'Name is required')),
     startDate: v.pipe(v.string(), v.minLength(1, 'Start date is required')),
     endDate: v.pipe(v.string(), v.minLength(1, 'End date is required')),
     discountPercent: v.pipe(v.number(), v.minValue(0), v.maxValue(100)),
   })

   export type CampaignFormValues = v.InferOutput<typeof campaignFormSchema>
   ```
2. Create mutation in `queries.ts`:
   ```typescript
   export const createCampaignMutationOptions = mutationOptions({
     mutationFn: async (campaign: CampaignFormValues) => {
       const res = (await api
         .post('inventory/promotional_campaigns/', { json: campaign })
         .json()) as ApiResponse
       return res.data
     },
     onSuccess: () => {
       queryClient.invalidateQueries({ queryKey: [CAMPAIGNS] })
     },
   })
   ```
3. Build form with `useAppForm`:
   ```typescript
   const form = useAppForm({
     defaultValues: { name: '', startDate: '', endDate: '', discountPercent: 0 },
     validators: { onChange: campaignFormSchema },
   })
   ```
4. All labels through `t('planning.campaign.fieldName')`

### Example 3: Dashboard with KPI Cards and Chart

User request:
```
Create a demand forecasting dashboard with KPI cards showing total predicted demand, accuracy percentage, and a line chart of predicted vs actual over time.
```

You would:
1. Create page in `src/pages/Planning/PlanningDemandForecast/PlanningDemandForecastPage/`
2. Define `forecastQueryOptions` in `queries.ts` using Ky
3. Build KPI cards using custom Tailwind theme:
   ```tsx
   <div className="grid grid-cols-3 gap-4">
     <div className="rounded-lg border border-night-100 bg-ghostwhite p-4">
       <p className="text-caption-1 text-night-400">{t('totalDemand')}</p>
       <p className="text-title-1 text-night-900">{formatNumber(totalDemand)}</p>
     </div>
   </div>
   ```
4. Use Celes colors: `night-*` for text, `ghostwhite`/`seasalt` for backgrounds, `emerald-*` for positive trends, `bittersweet-*` for negative
5. Add route lazy file with `validateSearch` for date range params using Valibot
6. All strings through `useTranslation('planning')`
