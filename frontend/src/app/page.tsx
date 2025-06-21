"use client";
import Link from "next/link";
import styles from "./styles.module.css";
import { useEffect, useState } from "react";
import { TTransport, TTruckStatus } from "@/types/admin";
import useFetchTruckStatuses from "@/hooks/fetchTruckStatuses";
import useFetchTransports from "@/hooks/fetchTransports";

export default function Home() {
  const [truckStatuses, setTruckStatuses] = useState<TTruckStatus[]>([]);

  const { isLoading: isTruckStatusesLoading, fetchTruckStatuses } =
    useFetchTruckStatuses(setTruckStatuses);
  useEffect(() => {
    fetchTruckStatuses();
  }, [fetchTruckStatuses]);

  const [transports, setTransports] = useState<TTransport[]>([]);

  const { isLoading: isTransportsLoading, fetchTransports } =
    useFetchTransports(setTransports);
  useEffect(() => {
    fetchTransports();
  }, [fetchTransports]);
  return (
    <div className={`${styles.home} disf fldc aic`}>
      <div className={`disf ${styles.links}`}>
        <Link className={`button`} href={"/enquiry"}>
          Enquiry Agent
        </Link>
        <Link className={`button`} href={"/leadfinder"}>
          Leadfinder Agent
        </Link>
      </div>

      <div className={`disf ${styles.tables}`}>
        {isTruckStatusesLoading ? (
          "Loading..."
        ) : (
          <div className={`disf aic fldc`}>
            <h2>Truck Status</h2>
            <table>
              <thead>
                <tr>
                  <th>Truck Code</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {truckStatuses.map((truck) => (
                  <tr key={truck.truck_code}>
                    <td>{truck.truck_code}</td>
                    <td>{truck.truck_status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {isTransportsLoading ? (
          "Loading..."
        ) : (
          <div className={`disf aic fldc`}>
            <h2>Transport Details</h2>
            <table>
              <thead>
                <tr>
                  <th>Customer ID</th>
                  <th>From</th>
                  <th>To</th>
                  <th>Mode</th>
                  <th>Transports Goods</th>
                  <th>Weight (kg)</th>
                </tr>
              </thead>
              <tbody>
                {transports.map((t) => (
                  <tr key={t.customer_id}>
                    <td>{t.customer_id}</td>
                    <td>{t.route_from}</td>
                    <td>{t.route_to}</td>
                    <td>{t.transport_mode}</td>
                    <td>{t.transports_goods ? "Yes" : "No"}</td>
                    <td>{t.weight_kg}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
