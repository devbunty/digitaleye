import { useMemo, useState } from "react";

import { BRAND } from "../brand";
import { AuthContext } from "./authContext";

/**
 * Demo-only authentication: accounts live in the browser bundle and the
 * session is kept in localStorage. Replace with real server-side auth
 * before exposing the dashboard to anyone you do not trust.
 */
const USERS = [
  {
    username: "admin",
    password: "admin123",
    name: "Administrator",
    role: "Security Operations",
  },
  {
    username: "analyst",
    password: "analyst123",
    name: "SOC Analyst",
    role: "Threat Hunter",
  },
];

const STORAGE_KEY = `${BRAND.slug}_session`;

function readSession() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(readSession);

  const value = useMemo(() => {
    function login(username, password) {
      const match = USERS.find(
        (u) => u.username === username.trim() && u.password === password
      );

      if (!match) {
        throw new Error("Invalid username or password.");
      }

      const session = {
        username: match.username,
        name: match.name,
        role: match.role,
      };

      setUser(session);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
      return session;
    }

    function logout() {
      setUser(null);
      localStorage.removeItem(STORAGE_KEY);
    }

    return {
      user,
      isAuthenticated: Boolean(user),
      login,
      logout,
      demoCredentials: USERS.map(({ username, password, name }) => ({
        username,
        password,
        name,
      })),
    };
  }, [user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
