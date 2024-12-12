import { MinPriorityQueue } from "@datastructures-js/priority-queue";
import { io, Socket } from "socket.io-client";
import { Measurement, MeasurementType } from "./data";

interface MeasurementConsumer {
  (m: Measurement): void;
}

class LastValuesCache {
  // last n values per measurement_type
  // newer values are appended
  private static MAX_N: number = 1000;
  private values: Map<MeasurementType, MinPriorityQueue<Measurement>> =
    new Map();

  newValue(m: Measurement) {
    const type = m.measurement_type;
    if (!this.values.has(type)) {
      this.values.set(type, new MinPriorityQueue<Measurement>((m) => m.tsp));
    }
    const knownValues = this.values.get(type)!;
    knownValues.push(m);
    while (knownValues.size() > LastValuesCache.MAX_N) {
      knownValues.pop();
    }
  }

  getValues(latestN = LastValuesCache.MAX_N): Measurement[] {
    const allValues: Measurement[] = [];
    for (const knownValues of this.values.values()) {
      const nAvailable = Math.min(latestN, knownValues.size());
      allValues.push(...knownValues.toArray().slice(-nAvailable));
    }
    return allValues;
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
