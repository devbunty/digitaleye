<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
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
<<<<<<< HEAD
=======
=======
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
