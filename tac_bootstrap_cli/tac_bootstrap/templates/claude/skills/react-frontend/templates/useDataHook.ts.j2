/**
 * useDataHook.ts -- Celes Data Fetching Template (Ky + TanStack Query)
 *
 * Usage:
 *   1. Copy this file to your page's `queries.ts` or `hooks/` directory
 *   2. Replace "Resource" with your entity name (e.g., Inventory, Campaign)
 *   3. Update the API endpoint path for Ky
 *   4. Define proper TypeScript types for params and response
 *   5. Import query keys from ~/lib/queryKeys
 *
 * Conventions:
 *   - queryOptions in dedicated `queries.ts` files
 *   - Naming: `{entity}QueryOptions` (NO `get` prefix)
 *   - mutationOptions: `{action}{Entity}MutationOptions`
 *   - Inline fetch logic in queryFn/mutationFn using Ky
 *   - Import query keys from ~/lib/queryKeys
 *   - JSDoc on all exports
 *   - Use stringifySearchParams for query parameters
 */

import { queryOptions, useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api, stringifySearchParams } from '~/lib/api'
import { queryClient } from '~/lib/queryClient'
import { RESOURCE } from '~/lib/queryKeys' // Replace RESOURCE with actual key
import { mutationOptions } from '~/utils/tanstackQuery'
import type { ApiResponse } from '~/types/apiContracts'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/** Parameters for filtering and paginating resources. */
interface ResourceParams {
  page?: number
  pageSize?: number
  search?: string
  sortField?: string
  sortDirection?: 'asc' | 'desc'
}

/** Single resource item from the API. */
interface ResourceItem {
  id: string
  name: string
  status: string
  // Add fields matching your API response
}

/** Paginated API response structure. */
interface PaginatedResourceResponse {
  items: ResourceItem[]
  total: number
  page: number
  pageSize: number
}

// ---------------------------------------------------------------------------
// Query Options
// ---------------------------------------------------------------------------

/**
 * Query options for fetching a paginated list of resources.
 * @param params - Filter and pagination parameters
 * @returns TanStack Query options for the resource list endpoint
 */
export const resourceQueryOptions = (params: ResourceParams) =>
  queryOptions({
    queryKey: [RESOURCE, params],
    queryFn: async () => {
      const searchParams = stringifySearchParams({
        page: params.page,
        page_size: params.pageSize,
        search: params.search,
        sort_field: params.sortField,
        sort_direction: params.sortDirection,
      })
      const response = (await api
        .get('your-module/resources/', { searchParams })
        .json()) as ApiResponse<PaginatedResourceResponse>
      return response.data
    },
  })

/**
 * Query options for fetching a single resource by ID.
 * @param id - The resource identifier
 */
export const resourceDetailQueryOptions = (id: string) =>
  queryOptions({
    queryKey: [RESOURCE, id],
    queryFn: async () => {
      const response = (await api
        .get(`your-module/resources/${id}/`)
        .json()) as ApiResponse<ResourceItem>
      return response.data
    },
    enabled: !!id,
  })

// ---------------------------------------------------------------------------
// Mutation Options
// ---------------------------------------------------------------------------

/**
 * Mutation options for creating a new resource.
 * Invalidates resource list cache on success.
 */
export const createResourceMutationOptions = mutationOptions({
  mutationFn: async (payload: Omit<ResourceItem, 'id'>) => {
    const res = (await api
      .post('your-module/resources/', { json: payload })
      .json()) as ApiResponse<ResourceItem>
    return res.data
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: [RESOURCE] })
  },
})

/**
 * Mutation options for updating an existing resource.
 * Invalidates both the list and detail cache on success.
 */
export const editResourceMutationOptions = mutationOptions({
  mutationFn: async (payload: Partial<ResourceItem> & { id: string }) => {
    const res = (await api
      .patch(`your-module/resources/${payload.id}/`, { json: payload })
      .json()) as ApiResponse<ResourceItem>
    return res.data
  },
  onSuccess: (_, variables) => {
    queryClient.invalidateQueries({ queryKey: [RESOURCE] })
    queryClient.invalidateQueries({ queryKey: [RESOURCE, variables.id] })
  },
})

/**
 * Mutation options for deleting a resource.
 * Invalidates resource list cache on success.
 */
export const deleteResourceMutationOptions = mutationOptions({
  mutationFn: async (id: string) => {
    await api.delete(`your-module/resources/${id}/`)
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: [RESOURCE] })
  },
})

// ---------------------------------------------------------------------------
// Custom Hook (optional - use when you need additional logic)
// ---------------------------------------------------------------------------

/**
 * Hook for fetching resources with derived state.
 * Use this when you need computed values from the query result.
 * For simple fetching, use resourceQueryOptions directly with useQuery/useSuspenseQuery.
 *
 * @param params - Filter and pagination parameters
 */
export function useResourceData(params: ResourceParams) {
  const query = useQuery(resourceQueryOptions(params))

  return {
    ...query,
    items: query.data?.items ?? [],
    totalCount: query.data?.total ?? 0,
    isEmpty: query.isSuccess && (query.data?.items.length ?? 0) === 0,
  }
}
