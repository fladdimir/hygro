export interface Measurement {
  sensor_id: string;
  tsp: number; // unix tsp
  measurement_type: MeasurementType;
  value: number;
}

export function formatTime(tsp: number): string {
  return new Date(tsp).toLocaleTimeString();
}

export enum MeasurementType {
  HUMIDITY = "HUMIDITY",
  TEMPERATURE = "TEMPERATURE",
}
