import { test, expect } from '@playwright/test';

/**
 * Test 6: Visual Styling and Theme
 *
 * Verifies that the dark theme and visual styling is applied correctly.
 */
test.describe('Visual Styling', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should have dark theme background', async ({ page }) => {
    // Check main container has dark background classes
    const container = page.locator('.min-h-screen').first();
    await expect(container).toBeVisible();

    const classes = await container.getAttribute('class');
    expect(classes).toContain('from-slate-900');
  });

  test('should have styled header with backdrop blur', async ({ page }) => {
    const header = page.locator('header');
    await expect(header).toBeVisible();

    const classes = await header.getAttribute('class');
    expect(classes).toContain('backdrop-blur');
    expect(classes).toContain('border-slate-700');
  });

  test('should have white text for title', async ({ page }) => {
    const title = page.locator('h1');
    await expect(title).toBeVisible();

    const classes = await title.getAttribute('class');
    expect(classes).toContain('text-white');
  });

  test('should have muted subtitle text', async ({ page }) => {
    const subtitle = page.locator('text=Real-time agent execution dashboard');
    await expect(subtitle).toBeVisible();

    const classes = await subtitle.getAttribute('class');
    expect(classes).toContain('text-slate-400');
  });

  test('should take a screenshot of the main page', async ({ page }) => {
    await page.waitForLoadState('networkidle');

    // Take a full page screenshot for visual regression
    await expect(page).toHaveScreenshot('orchestrator-main.png', {
      fullPage: true,
      timeout: 10000,
    });
  });

  test('should take a screenshot of command palette', async ({ page }) => {
    await page.waitForLoadState('networkidle');
    await page.keyboard.press('Meta+k');

    // Wait for animation
    await page.waitForTimeout(300);

    await expect(page).toHaveScreenshot('orchestrator-command-palette.png', {
      fullPage: true,
      timeout: 10000,
    });
  });
});
