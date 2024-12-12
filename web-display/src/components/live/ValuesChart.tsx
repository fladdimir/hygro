import { MinPriorityQueue } from "@datastructures-js/priority-queue";
import { useEffect, useState } from "react";
import { latestValueService } from "../../services/LatestValueService";
import { Measurement, MeasurementType } from "../../services/data";
import { Chart } from "../Chart";

// function formatDate(tsp: number | undefined): string | undefined {
//   if (!tsp) return undefined;
//   return new Date(tsp).toLocaleTimeString();
// }

interface LatestValuesChartProps {
  measurementType: MeasurementType;
  color: string;
  width: number;
  height: number;
}
export function LatestValuesChart(props: LatestValuesChartProps) {
  const nMaxValues = 1000;
  const knownValues = new MinPriorityQueue<Measurement>((m) => m.tsp);
  const [displayed, setCurrentValues] = useState<Measurement[]>([]);

  function handleMeasurement(m: Measurement) {
    if (m.measurement_type === props.measurementType) {
      // may come in out of order, efficiently reorder via heap
      knownValues.push(m);
      while (knownValues.size() > nMaxValues) {
        knownValues.pop();
      }
      setCurrentValues(knownValues.toArray());
    }
  }

  useEffect(() => {
    // setup
    latestValueService.addListener(handleMeasurement, nMaxValues);
    return () => {
      // cleanup
      latestValueService.removeListener(handleMeasurement);
      knownValues.clear();
    };
  }, []);

  return (
    <>
      <Chart
        values={displayed}
        color={props.color}
        tickDateFormatter={(d) => d.toLocaleTimeString()}
        width={props.width}
        height={props.height}
      />
    </>
  );
}
