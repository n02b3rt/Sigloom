
async function getDevices() {
  const res = await fetch(process.env.NEXT_PUBLIC_API_BASE + '/devices', { cache: 'no-store' })
  if (!res.ok) throw new Error('API error')
  return res.json()
}

export default async function Home() {
  const data = await getDevices()
  return (
    <main>
      <h1>SigLoom - Devices</h1>
      <ul>
        {data.items.map((d: any) => (
          <li key={d.id}>
            <strong>{d.id}</strong> — {d.online ? 'online ✅' : 'offline ⛔'} — ver {d.app_ver}
          </li>
        ))}
      </ul>
      <p style={{marginTop: 16, opacity: .7}}>API: {process.env.NEXT_PUBLIC_API_BASE}</p>
    </main>
  )
}
