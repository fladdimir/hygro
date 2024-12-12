import { io, Socket } from "socket.io-client";
import { Measurement, MeasurementType } from "./data";

interface MeasurementConsumer {
  (m: Measurement): void;
}

class LastValuesCache {
  // last n values per measurement_type
  // newer values are appended
  private static MAX_N: number = 1000;
  private values: Map<MeasurementType, Measurement[]> = new Map();

  newValue(m: Measurement) {
    const type = m.measurement_type;
    if (!this.values.has(type)) {
      this.values.set(type, []);
    }
    const knownValues = this.values.get(type)!;
    knownValues.push(m);
    while (knownValues.length > LastValuesCache.MAX_N) {
      knownValues.shift();
    }
  }

  getValues(latestN = LastValuesCache.MAX_N): Measurement[] {
    const values: Measurement[] = [];
    for (var [_, v] of this.values) {
      const available = Math.min(latestN, v.length);
      values.push(...v.slice(-available));
    }
    return values.sort((m1, m2) => m1.tsp - m2.tsp);
  }
}

class LatestValueService {
  private socket: Socket | undefined = undefined;
  private measurementConsumers: Set<MeasurementConsumer> = new Set();
  private lvc = new LastValuesCache();

  addListener(mc: MeasurementConsumer, nReplayedValues = 1) {
    this.measurementConsumers.add(mc);
    this.lvc.getValues(nReplayedValues).forEach((m) => mc(m));
  }
  removeListener(mc: MeasurementConsumer) {
    this.measurementConsumers.delete(mc);
  }

  constructor() {
    this.socket = io();
    this.socket.on("data", (data) => {
      if (data instanceof Array) {
        // batched messages
        data.forEach((d) => this.newMessage(d));
      } else {
        // single value
        this.newMessage(data);
      }
    });
  }

  private newMessage(data: string) {
    this.newMeasurement(this.parse(data));
  }

  private newMeasurement(m: Measurement) {
    this.lvc.newValue(m);
    this.measurementConsumers.forEach((cb) => cb(m));
  }

  private parse(str: string): Measurement {
    const json = JSON.parse(str);
    json.tsp = new Date(json.tsp).getTime();
    return json;
  }
}

export const latestValueService = new LatestValueService();
