export interface Measurement {
  sensor_id: string;
  tsp: number; // unix tsp
  measurement_type: MeasurementType;
  value: number;
}

export enum MeasurementType {
  HUMIDITY = "HUMIDITY",
  TEMPERATURE = "TEMPERATURE",
}
