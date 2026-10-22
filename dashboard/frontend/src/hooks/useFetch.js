import { useEffect, useState } from "react";

/**
 * Load data once and again whenever `refreshToken` changes.
 *
 * `fetcher` must be a stable reference (a module-level function). Failures
 * are logged and the previous data is kept, so a hiccup never blanks a panel.
 */
export function useFetch(fetcher, initialData, refreshToken = 0) {
  const [data, setData] = useState(initialData);

  useEffect(() => {
    let cancelled = false;

    fetcher()
      .then((result) => {
        if (!cancelled) setData(result);
      })
      .catch((error) => console.error(error));

    return () => {
      cancelled = true;
    };
  }, [fetcher, refreshToken]);

  return data;
}
