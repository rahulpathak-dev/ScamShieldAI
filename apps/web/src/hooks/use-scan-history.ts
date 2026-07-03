"use client";

import { useEffect, useState } from "react";

import { getScanHistory, StoredScan } from "@/lib/scan-history";

export function useScanHistory() {
  const [history, setHistory] = useState<StoredScan[]>([]);

  useEffect(() => {
    function syncHistory() {
      setHistory(getScanHistory());
    }

    syncHistory();
    window.addEventListener("storage", syncHistory);
    window.addEventListener("scamshield:history-updated", syncHistory);

    return () => {
      window.removeEventListener("storage", syncHistory);
      window.removeEventListener("scamshield:history-updated", syncHistory);
    };
  }, []);

  return history;
}