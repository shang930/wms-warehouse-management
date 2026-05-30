export { default as dayjs } from 'dayjs'
export function deepClone<T>(obj: T): T { return JSON.parse(JSON.stringify(obj)) }

export function exportCSV(filename: string, columns: string[], rows: any[][]) {
  const BOM = '﻿'
  const header = columns.join(',')
  const body = rows.map(row => row.map(v => {
    const s = String(v ?? '')
    return s.includes(',') || s.includes('"') || s.includes('\n') ? `"${s.replace(/"/g,'""')}"` : s
  }).join(','))
  const csv = BOM + [header, ...body].join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url; link.download = `${filename}.csv`; link.click()
  URL.revokeObjectURL(url)
}
