import { test, expect } from '@playwright/test';

/**
 * Test 4: Swimlane Board
 *
 * Verifies that the swimlane board component renders correctly
 * and can display agent lanes.
 */
test.describe('Swimlane Board', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should render main content area', async ({ page }) => {
    // Main content area should exist
    const main = page.locator('main');
    await expect(main).toBeVisible();
  });

  test('should display empty state when no agents', async ({ page }) => {
    // Without agents, should show empty state
    const emptyState = page.locator('text=No agents available');
    await expect(emptyState).toBeVisible({ timeout: 10000 });
  });

  test('should have grid layout for agent lanes', async ({ page }) => {
    // The swimlane board uses a grid layout
    const main = page.locator('main');
    await expect(main).toBeVisible();

    // Check for grid container (exists even when empty)
    const gridOrEmpty = page.locator('main > div');
    await expect(gridOrEmpty).toBeVisible();
  });

  test('should be responsive with proper spacing', async ({ page }) => {
    // Check the main content has padding
    const main = page.locator('main');
    await expect(main).toHaveClass(/p-6/);
  });
});
