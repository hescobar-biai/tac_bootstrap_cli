import { test, expect } from '@playwright/test';

/**
 * Test 1: Application Loads
 *
 * Verifies that the orchestrator frontend loads correctly and
 * displays the main UI elements.
 */
test.describe('Application Loading', () => {
  test('should load the main page', async ({ page }) => {
    await page.goto('/');

    // Check page title is present
    await expect(page).toHaveTitle(/Orchestrator/);
  });

  test('should display header with title', async ({ page }) => {
    await page.goto('/');

    // Check main header
    const header = page.locator('h1');
    await expect(header).toHaveText('Orchestrator');

    // Check subtitle
    const subtitle = page.locator('text=Real-time agent execution dashboard');
    await expect(subtitle).toBeVisible();
  });

  test('should display connection status indicator', async ({ page }) => {
    await page.goto('/');

    // Connection status should be visible in header
    const statusIndicator = page.locator('.rounded-full').first();
    await expect(statusIndicator).toBeVisible();
  });

  test('should display empty state when no agents connected', async ({ page }) => {
    await page.goto('/');

    // Wait for app to initialize
    await page.waitForLoadState('networkidle');

    // Empty state message should be visible
    const emptyState = page.locator('text=No agents available');
    await expect(emptyState).toBeVisible({ timeout: 10000 });
  });
});
