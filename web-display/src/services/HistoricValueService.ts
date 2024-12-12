import { Measurement, MeasurementType } from "./data";

class HistoricValueService {
  async getValues(
    from: Date,
    to: Date,
    type: MeasurementType
  ): Promise<Measurement[]> {
    const url =
      "/query-api/measurements-time-buckets?" +
      new URLSearchParams({
        from: from.toISOString(),
        to: to.toISOString(),
        type,
        limit: "1000",
      });
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    const json: any[] = await response.json();
    json.forEach((m) => (m.tsp = new Date(m.tsp).getTime()));
    return json;
  }
}

export const historicValueService = new HistoricValueService();
