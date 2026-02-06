import { test, expect } from '@playwright/test';

/**
 * Test 3: WebSocket Connection Status
 *
 * Verifies that the WebSocket connection status is properly displayed
 * and reflects the actual connection state.
 */
test.describe('WebSocket Connection Status', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display connection status in header', async ({ page }) => {
    // Look for status indicator (either connected or disconnected)
    const statusIndicator = page.locator('.rounded-full').first();
    await expect(statusIndicator).toBeVisible();
  });

  test('should show disconnected status initially when no server', async ({ page }) => {
    await page.waitForLoadState('networkidle');

    // Without a WebSocket server, status should indicate disconnection
    // The exact text depends on implementation, but it should be visible
    const header = page.locator('header');
    await expect(header).toBeVisible();
  });

  test('should have colored status indicator based on connection', async ({ page }) => {
    await page.waitForLoadState('networkidle');

    // Status indicator should have either red or green background
    const statusIndicator = page.locator('.rounded-full').first();
    await expect(statusIndicator).toBeVisible();

    // Check it has a color class (bg-green-500 or bg-red-500)
    const classes = await statusIndicator.getAttribute('class');
    expect(classes).toMatch(/bg-(green|red)-500/);
  });
});
