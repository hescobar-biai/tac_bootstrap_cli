import { test, expect } from '@playwright/test';

/**
 * Test 2: Command Palette
 *
 * Verifies that the command palette (⌘K) works correctly for
 * searching agents and tasks.
 */
test.describe('Command Palette', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should open command palette with Cmd+K', async ({ page }) => {
    // Open with keyboard shortcut
    await page.keyboard.press('Meta+k');

    // Command palette should be visible
    const palette = page.locator('input[placeholder*="Search agents"]');
    await expect(palette).toBeVisible({ timeout: 5000 });
  });

  test('should open command palette with Ctrl+K on non-Mac', async ({ page }) => {
    // Open with Ctrl+K (cross-platform)
    await page.keyboard.press('Control+k');

    // Command palette should be visible
    const palette = page.locator('input[placeholder*="Search agents"]');
    await expect(palette).toBeVisible({ timeout: 5000 });
  });

  test('should show empty state when no search query', async ({ page }) => {
    await page.keyboard.press('Meta+k');

    // Empty state text
    const emptyState = page.locator('text=Start typing to search');
    await expect(emptyState).toBeVisible();
  });

  test('should close command palette with Escape', async ({ page }) => {
    await page.keyboard.press('Meta+k');

    const palette = page.locator('input[placeholder*="Search agents"]');
    await expect(palette).toBeVisible();

    // Close with Escape
    await page.keyboard.press('Escape');

    // Palette should be hidden
    await expect(palette).not.toBeVisible();
  });

  test('should close command palette by clicking backdrop', async ({ page }) => {
    await page.keyboard.press('Meta+k');

    const palette = page.locator('input[placeholder*="Search agents"]');
    await expect(palette).toBeVisible();

    // Click backdrop
    await page.locator('.bg-black\\/50').click();

    // Palette should be hidden
    await expect(palette).not.toBeVisible();
  });

  test('should show "No results found" for non-matching query', async ({ page }) => {
    await page.keyboard.press('Meta+k');

    // Type a search query that won't match anything
    await page.locator('input[placeholder*="Search agents"]').fill('nonexistentquery12345');

    // Should show no results message
    const noResults = page.locator('text=No results found');
    await expect(noResults).toBeVisible();
  });
});
