import { test, expect } from '@playwright/test';

/**
 * Test 5: Keyboard Navigation
 *
 * Verifies that keyboard navigation works throughout the app,
 * especially in the command palette.
 */
test.describe('Keyboard Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should focus search input when command palette opens', async ({ page }) => {
    await page.keyboard.press('Meta+k');

    const input = page.locator('input[placeholder*="Search agents"]');
    await expect(input).toBeFocused();
  });

  test('should navigate results with arrow keys', async ({ page }) => {
    // This test validates the arrow key handlers exist
    await page.keyboard.press('Meta+k');

    const input = page.locator('input[placeholder*="Search agents"]');
    await expect(input).toBeVisible();

    // Arrow down should not cause errors
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('ArrowUp');

    // Input should still be focused
    await expect(input).toBeFocused();
  });

  test('should handle Enter key in command palette', async ({ page }) => {
    await page.keyboard.press('Meta+k');

    const input = page.locator('input[placeholder*="Search agents"]');
    await expect(input).toBeVisible();

    // Press enter (should not cause errors even with no selection)
    await page.keyboard.press('Enter');
  });

  test('should allow typing in search input', async ({ page }) => {
    await page.keyboard.press('Meta+k');

    const input = page.locator('input[placeholder*="Search agents"]');
    await input.fill('test query');

    await expect(input).toHaveValue('test query');
  });

  test('should clear search on close and reopen', async ({ page }) => {
    await page.keyboard.press('Meta+k');

    const input = page.locator('input[placeholder*="Search agents"]');
    await input.fill('test query');
    await expect(input).toHaveValue('test query');

    // Close
    await page.keyboard.press('Escape');

    // Reopen
    await page.keyboard.press('Meta+k');

    // Input should be cleared
    const newInput = page.locator('input[placeholder*="Search agents"]');
    await expect(newInput).toHaveValue('');
  });
});
