import React from 'react'

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' }

export function Button({ variant = 'primary', className = '', ...props }: ButtonProps) {
  const base = 'inline-flex items-center gap-2 rounded px-3 py-2 text-sm font-medium'
  const styles = variant === 'primary' ? 'bg-brand text-white hover:opacity-90' : 'bg-gray-200 text-gray-900 hover:bg-gray-300'
  return <button className={`${base} ${styles} ${className}`} {...props} />
}
