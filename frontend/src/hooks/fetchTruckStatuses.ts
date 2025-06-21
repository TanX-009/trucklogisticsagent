"use client";

import { Dispatch, SetStateAction, useCallback, useRef, useState } from "react";
import AdminService from "@/services/admin";
import { TTruckStatus } from "@/types/admin";

export default function useFetchTruckStatuses(
  setter: Dispatch<SetStateAction<TTruckStatus[]>>,
) {
  const isLoadingRef = useRef(false);
  const [isLoading, setIsLoading] = useState(false);

  const fetchTruckStatuses = useCallback(async () => {
    if (isLoadingRef.current) return;
    isLoadingRef.current = true;
    try {
      setIsLoading(true);
      const response = await AdminService.getTruckStatuses();

      if (response.success) setter(response.data || []);
    } finally {
      setIsLoading(false);
      isLoadingRef.current = false;
    }
  }, [setter]);

  return { isLoading, fetchTruckStatuses };
}
