import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen grid grid-cols-[260px_1fr_480px]">
      <aside className="border-r p-4">
        <div className="font-semibold text-sm text-gray-500 mb-2">Accounts</div>
        <ul className="space-y-2">
          <li>demo@example.com</li>
        </ul>
        <div className="mt-6 font-semibold text-sm text-gray-500">Folders</div>
        <ul className="space-y-2 mt-2">
          <li>Inbox</li>
          <li>Starred</li>
          <li>Sent</li>
        </ul>
      </aside>
      <main className="border-r p-4">
        <div className="flex items-center gap-3 mb-4">
          <input className="border rounded px-3 py-2 w-full" placeholder="Search mail" />
          <button className="bg-brand text-white px-3 py-2 rounded">Compose</button>
        </div>
        <div className="space-y-2">
          {[1,2,3,4,5].map((id) => (
            <Link key={id} href={`/threads/${id}`} className="block border rounded p-3 hover:bg-gray-50">
              <div className="font-medium">Thread Subject {id}</div>
              <div className="text-sm text-gray-500">Snippet preview of the message...</div>
            </Link>
          ))}
        </div>
      </main>
      <section className="p-4">
        <div className="text-gray-500 text-sm mb-2">Thread</div>
        <div className="text-gray-400 text-sm">Select a thread</div>
      </section>
    </div>
  )
}
