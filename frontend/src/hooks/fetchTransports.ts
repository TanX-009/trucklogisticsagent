"use client";

import { Dispatch, SetStateAction, useCallback, useRef, useState } from "react";
import AdminService from "@/services/admin";
import { TTransport } from "@/types/admin";

export default function useFetchTransports(
  setter: Dispatch<SetStateAction<TTransport[]>>,
) {
  const isLoadingRef = useRef(false);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTransports = useCallback(async () => {
    if (isLoadingRef.current) return;
    isLoadingRef.current = true;
    try {
      setIsLoading(true);
      const response = await AdminService.getTransports();

      if (response.success) setter(response.data || []);
    } finally {
      setIsLoading(false);
      isLoadingRef.current = false;
    }
  }, [setter]);

  return { isLoading, fetchTransports };
}
