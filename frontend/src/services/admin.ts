import { TTransport, TTruckStatus } from "@/types/admin";
import { get, TApiResponse } from "./serviceConfig";
import Services from "./serviceUrls";

async function getTruckStatuses(): Promise<TApiResponse<TTruckStatus[]>> {
  return get(Services.trucks);
}

async function getTransports(): Promise<TApiResponse<TTransport[]>> {
  return get(Services.transports);
}

const AdminService = {
  getTransports,
  getTruckStatuses,
};

export default AdminService;
