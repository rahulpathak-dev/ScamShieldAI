# ScamShieldAI Web

Next.js frontend for ScamShieldAI.

## Stack

- Next.js App Router
- TypeScript
- Tailwind CSS
- shadcn-compatible component structure
- Recharts dependency for future dashboards

## Local Setup

```powershell
cd apps/web
npm install
npm run dev
```

The app expects:

```text
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Folder Structure

```text
src/app/                 Next.js routes and global styles
src/components/ui/       Reusable shadcn-compatible primitives
src/components/          Product components
src/lib/                 Runtime config, API client, utilities
src/types/               Shared frontend DTO types
```

## Design Direction

The first screen is an operational analysis workspace. The frontend avoids a marketing landing page because analysts and users need direct access to the product workflow.
