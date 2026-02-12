/**
 * DashboardPage.tsx -- Celes Dashboard Page Template
 *
 * Usage:
 *   1. Copy and rename to your page (e.g., WorkAreaInventoryPage.tsx)
 *   2. Create matching index.ts that exports ONLY the component
 *   3. Create queries.ts with your queryOptions/mutationOptions
 *   4. Create helpers.ts with validation schemas if forms are needed
 *   5. Add route file: src/routes/_layout.{path}.index.lazy.tsx
 *
 * Structure provided:
 *   - KPI metrics bar at top
 *   - DataTable.Root with server pagination, sorting, toolbar
 *   - Uses Celes custom theme (night-*, seasalt, ghostwhite, etc.)
 *   - All text through useTranslation (react-i18next)
 *   - Ky + TanStack Query for data fetching
 *
 * Conventions:
 *   - Page naming: {Module}{Feature}Page (e.g., WorkAreaInventoryPage)
 *   - DataTable.Root with stable tableId (NEVER DataGridPremium directly)
 *   - processApiColumns for column mapping
 *   - useSearchPaginationModel for URL-persisted pagination
 *   - useSortModelPersisted for localStorage-persisted sorting
 */

import { useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useTranslation } from 'react-i18next'
import clsx from 'clsx'
import { DataTable } from '~/components/UI/DataTable'
import {
  processApiColumns,
  useSearchPaginationModel,
  useSortModelPersisted,
} from '~/utils/dataGrid'
// import { resourceQueryOptions } from './queries'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface KpiMetric {
  label: string
  value: string | number
  trend?: { direction: 'up' | 'down' | 'flat'; value: string }
}

interface ResourceItem {
  id: string
  name: string
  status: string
  // Replace with your actual fields
}

// ---------------------------------------------------------------------------
// KPI Metrics Bar
// ---------------------------------------------------------------------------

function MetricsBar({ metrics }: { metrics: KpiMetric[] }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {metrics.map((metric) => (
        <div
          key={metric.label}
          className="rounded-lg border border-night-100 bg-ghostwhite p-4"
        >
          <p className="text-caption-1 text-night-400">{metric.label}</p>
          <p className="text-title-1 text-night-900 mt-1">{metric.value}</p>
          {metric.trend && (
            <p
              className={clsx(
                'text-caption-1 mt-1',
                metric.trend.direction === 'up' && 'text-emerald-600',
                metric.trend.direction === 'down' && 'text-bittersweet-600',
                metric.trend.direction === 'flat' && 'text-night-400',
              )}
            >
              {metric.trend.direction === 'up' ? '+' : metric.trend.direction === 'down' ? '-' : ''}
              {metric.trend.value}
            </p>
          )}
        </div>
      ))}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Main Page Component
// ---------------------------------------------------------------------------

/**
 * DashboardPage -- Supply chain dashboard with KPIs and data table.
 *
 * Replace this with your actual page description.
 * Rename to {Module}{Feature}Page following Celes conventions.
 *
 * @example
 * ```tsx
 * // In index.ts:
 * export { DashboardPage } from './DashboardPage'
 *
 * // In route file (_layout.module.feature.index.lazy.tsx):
 * import { createLazyFileRoute } from '@tanstack/react-router'
 * import { DashboardPage } from '~/pages/Module/Feature/DashboardPage'
 * export const Route = createLazyFileRoute('/_layout/module/feature/')({
 *   component: DashboardPage,
 * })
 * ```
 */
export function DashboardPage() {
  const { t } = useTranslation('module') // Replace 'module' with your namespace

  // -----------------------------------------------------------------------
  // Pagination & Sorting (URL + localStorage persisted)
  // -----------------------------------------------------------------------
  const { paginationModel, setPaginationModel } = useSearchPaginationModel({
    initialPageSize: 25,
  })

  const { sortModel, handleSortModelChange } = useSortModelPersisted(
    'dashboard-page-sort',
  )

  // -----------------------------------------------------------------------
  // Data Fetching (Ky + TanStack Query)
  // -----------------------------------------------------------------------
  // Replace with your actual queryOptions:
  // const { data, isLoading, isPending } = useQuery(
  //   resourceQueryOptions({
  //     page: paginationModel.page,
  //     pageSize: paginationModel.pageSize,
  //     sortField: sortModel[0]?.field,
  //     sortDirection: sortModel[0]?.sort ?? undefined,
  //   })
  // )

  // Placeholder data (remove when wiring real API)
  const data = { items: [] as ResourceItem[], total: 0 }
  const isLoading = false
  const isPending = false

  // -----------------------------------------------------------------------
  // Columns
  // -----------------------------------------------------------------------
  const columns = useMemo(
    () =>
      processApiColumns(
        [
          { field: 'name', headerName: t('columns.name'), flex: 1, minWidth: 200 },
          { field: 'status', headerName: t('columns.status'), width: 120 },
          // Add more columns matching your data
        ],
        {
          defaultColDefProps: { flex: 1 },
        },
      ),
    [t],
  )

  // -----------------------------------------------------------------------
  // KPI Metrics (derive from fetched data)
  // -----------------------------------------------------------------------
  const metrics: KpiMetric[] = [
    { label: t('metrics.total'), value: data.total },
    { label: t('metrics.active'), value: 0, trend: { direction: 'up', value: '12%' } },
    { label: t('metrics.pending'), value: 0 },
    { label: t('metrics.issues'), value: 0, trend: { direction: 'down', value: '3%' } },
  ]

  // -----------------------------------------------------------------------
  // Handlers
  // -----------------------------------------------------------------------
  const handleExport = () => {
    // Implement CSV/Excel export
  }

  // -----------------------------------------------------------------------
  // Render
  // -----------------------------------------------------------------------
  return (
    <div className="flex flex-col gap-6 p-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-title-1 text-night-900">{t('pageTitle')}</h1>
      </div>

      {/* KPI Metrics */}
      <MetricsBar metrics={metrics} />

      {/* Data Table */}
      <DataTable.Root
        tableId="dashboard-resource-table" // REQUIRED: stable unique ID
        rows={data.items}
        columns={columns}
        getRowId={(row) => row.id}
        pagination
        paginationMode="server"
        paginationModel={paginationModel}
        onPaginationModelChange={setPaginationModel}
        sortingMode="server"
        sortModel={sortModel}
        onSortModelChange={handleSortModelChange}
        rowCount={data.total}
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
    </div>
  )
}
