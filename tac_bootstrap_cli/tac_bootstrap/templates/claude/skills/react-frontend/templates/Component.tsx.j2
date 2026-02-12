/**
 * Component.tsx -- Celes React Component Template
 *
 * Usage:
 *   1. Copy this file and rename to your component name (PascalCase)
 *   2. Replace "Component" with your component name throughout
 *   3. Define your props interface with all required and optional fields
 *   4. Implement the component body
 *   5. Add co-located tests in Component.test.tsx
 *
 * Conventions:
 *   - Named export for reusable components
 *   - index.ts exports ONLY the main component
 *   - All props typed via interface {ComponentName}Props
 *   - Use clsx for conditional class merging
 *   - Use Celes custom colors (night-*, seasalt, ghostwhite, orangepeel-*, emerald-*)
 *   - Use Celes typography (text-title-1, text-body-1, text-body-2, text-caption-1)
 *   - No `any` type — use `unknown` with type guards
 *   - All user-facing text through useTranslation
 *   - Use useId() for accessibility ID generation
 *   - JSDoc on all exports
 */

import { useId, type ReactNode } from 'react'
import clsx from 'clsx'
import { useTranslation } from 'react-i18next'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/**
 * Props for the Component.
 *
 * Replace these fields with the actual props your component needs.
 * Keep required props minimal; prefer optional with sensible defaults.
 */
interface ComponentProps {
  /** Primary content or label displayed by the component. */
  title: string

  /** Optional secondary text shown below the title. */
  subtitle?: string

  /** Visual variant controlling color and emphasis. */
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'danger'

  /** Whether the component is in a disabled/non-interactive state. */
  disabled?: boolean

  /** Slot for an icon or decorative element rendered before the title. */
  icon?: ReactNode

  /** Content rendered inside the component body. */
  children?: ReactNode

  /** Click handler. Omit if the component is purely presentational. */
  onClick?: () => void

  /** Additional CSS classes merged with the component's base styles. */
  className?: string
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Maps the variant prop to Celes custom Tailwind color classes. */
function getVariantClasses(variant: ComponentProps['variant'] = 'default') {
  const map: Record<NonNullable<ComponentProps['variant']>, string> = {
    default: 'bg-ghostwhite text-night-900 border-night-200',
    primary: 'bg-orangepeel-50 text-orangepeel-900 border-orangepeel-200',
    success: 'bg-emerald-50 text-emerald-900 border-emerald-200',
    warning: 'bg-orangepeel-50 text-night-900 border-orangepeel-300',
    danger: 'bg-bittersweet-50 text-bittersweet-900 border-bittersweet-200',
  }
  return map[variant]
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

/**
 * Component -- A reusable UI building block.
 *
 * Replace this docstring with a description of what your component does,
 * when to use it, and any important behavioral notes.
 *
 * @example
 * ```tsx
 * <Component title="Inventory Alert" variant="warning">
 *   <p>Stock for SKU-1234 is below reorder point.</p>
 * </Component>
 * ```
 */
export function Component({
  title,
  subtitle,
  variant = 'default',
  disabled = false,
  icon,
  children,
  onClick,
  className,
}: ComponentProps) {
  const { t } = useTranslation('common')
  const headingId = useId()

  return (
    <div
      className={clsx(
        'rounded-lg border p-4 transition-colors',
        getVariantClasses(variant),
        onClick && !disabled && 'cursor-pointer hover:shadow-md',
        disabled && 'opacity-50 cursor-not-allowed',
        className,
      )}
      onClick={disabled ? undefined : onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick && !disabled ? 0 : undefined}
      aria-disabled={disabled || undefined}
      aria-labelledby={headingId}
      onKeyDown={
        onClick && !disabled
          ? (e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault()
                onClick()
              }
            }
          : undefined
      }
    >
      {/* Header */}
      <div className="flex items-center gap-2">
        {icon && <span className="shrink-0">{icon}</span>}
        <div>
          <h3 id={headingId} className="text-body-1 font-semibold leading-tight text-night-900">
            {title}
          </h3>
          {subtitle && (
            <p className="text-caption-1 text-night-400 mt-0.5">{subtitle}</p>
          )}
        </div>
      </div>

      {/* Body */}
      {children && <div className="mt-3">{children}</div>}
    </div>
  )
}
