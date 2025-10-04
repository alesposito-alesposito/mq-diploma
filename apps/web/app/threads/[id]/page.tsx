import { notFound } from 'next/navigation'

async function fetchThread(id: string) {
  const res = await fetch(`${process.env.API_INTERNAL_URL || 'http://localhost:8000'}/threads?page=1&page_size=1`, { cache: 'no-store' })
  if (!res.ok) return null
  const data = await res.json()
  const thread = data.items?.[0]
  return thread
}

export default async function ThreadPage({ params }: { params: { id: string }}) {
  const thread = await fetchThread(params.id)
  if (!thread) return notFound()
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-semibold">{thread.subject || 'No subject'}</h1>
      <div className="prose dark:prose-invert">
        <p>Demo message body from API.</p>
      </div>
      <div>
        <h2 className="font-medium mb-2">Notes</h2>
        <div className="border rounded p-3">This is a placeholder for Notion-style notes.</div>
      </div>
    </div>
  )
}
