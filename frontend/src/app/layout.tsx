
export const metadata = { title: 'Pico OTA', description: 'Starter UI' }
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pl">
      <body style={{ fontFamily: 'system-ui', margin: 0, padding: 24 }}>
        {children}
      </body>
    </html>
  )
}
