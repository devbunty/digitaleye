import { Component } from "react";

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
import { BRAND } from "../../brand";

export default class ErrorBoundary extends Component {
  state = { hasError: false };
<<<<<<< HEAD
=======
=======
export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
    console.error(`${BRAND.name} UI error:`, error, info);
  }

  render() {
    if (!this.state.hasError) return this.props.children;

    return (
      <div className="flex h-screen items-center justify-center bg-[#020817] text-white">
        <div className="max-w-md rounded-2xl border border-red-500/30 bg-slate-900 p-8 text-center">
          <h1 className="text-2xl font-bold text-red-400">
            Something went wrong
          </h1>
          <p className="mt-3 text-slate-400">
            This section of the dashboard hit an unexpected error. Try
            reloading the page.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="mt-6 rounded-xl bg-cyan-600 px-4 py-3 font-semibold transition hover:bg-cyan-500"
          >
            Reload
          </button>
        </div>
      </div>
    );
<<<<<<< HEAD
=======
=======
    console.error("NOVAIRIS UI error:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex h-screen items-center justify-center bg-[#020817] text-white">
          <div className="max-w-md rounded-2xl border border-red-500/30 bg-slate-900 p-8 text-center">
            <h1 className="text-2xl font-bold text-red-400">
              Something went wrong
            </h1>
            <p className="mt-3 text-slate-400">
              This section of the dashboard hit an unexpected error. Try
              reloading the page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="mt-6 rounded-xl bg-cyan-600 px-4 py-3 font-semibold transition hover:bg-cyan-500"
            >
              Reload
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
  }
}
