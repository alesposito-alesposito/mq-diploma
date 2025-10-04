import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

export async function GET(req: Request) {
  const url = new URL(req.url)
  const page = url.searchParams.get('page') || '1'
  const page_size = url.searchParams.get('page_size') || '20'
  const q = url.searchParams.get('q')
  const apiUrl = `${process.env.API_INTERNAL_URL || 'http://localhost:8000'}/threads?page=${page}&page_size=${page_size}${q ? `&q=${encodeURIComponent(q)}` : ''}`
  const res = await fetch(apiUrl)
  const data = await res.json()
  return NextResponse.json(data)
}
