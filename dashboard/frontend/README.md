# Digital Eye dashboard

React 19 + Vite + Tailwind CSS 4 front end for the Digital Eye API.

```bash
npm install
npm run dev      # http://localhost:5173
npm run lint
npm run build
```

The API base URL defaults to `http://localhost:5000`. Override it with
`VITE_API_URL` in `.env.local`.

## Layout

| Folder | Purpose |
|---|---|
| `src/pages` | One component per sidebar page |
| `src/components` | Reusable UI, grouped by feature (`ui/` holds the shared primitives) |
| `src/services` | API calls; `http.js` is the single `fetch` wrapper |
| `src/hooks` | `useFetch` (load + refresh) and `useAutoRefresh` (polling) |
| `src/contexts` | Auth and theme providers |
| `src/constants`, `src/utils` | Shared severity styling and pure helpers |
