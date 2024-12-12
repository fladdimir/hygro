import { MeasurementType } from "./data";

const map = new Map();
map.set(MeasurementType.TEMPERATURE, "#d15f26");
map.set(MeasurementType.HUMIDITY, "#307db5");

export function getColor(mt: MeasurementType): string {
  return map.get(mt);
}
