export interface TTruckStatus {
  truck_code: string;
  truck_status: string;
}

export interface TTransport {
  customer_id: string;
  route_from: string;
  route_to: string;
  transport_mode: string;
  transports_goods: boolean;
  weight_kg: number;
}
