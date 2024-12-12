import { useEffect, useState } from "react";
import { latestValueService } from "../../services/LatestValueService";
import { Measurement, MeasurementType } from "../../services/data";
import { Chart } from "../Chart";

interface LatestValuesChartProps {
  measurementType: MeasurementType;
  color: string;
  width: number;
  height: number;
}
export function LatestValuesChart(props: LatestValuesChartProps) {
  const nMaxValues = 1000;
  const [currentValues, setCurrentValues] = useState<Measurement[]>([]);

  function handleMeasurement(m: Measurement) {
    if (m.measurement_type === props.measurementType) {
      currentValues.push(m);
      while (currentValues.length > nMaxValues) {
        currentValues.shift();
      }
      setCurrentValues([...currentValues]);
    }
  }

  useEffect(() => {
    // setup
    latestValueService.addListener(handleMeasurement, nMaxValues);
    return () => {
      // cleanup
      latestValueService.removeListener(handleMeasurement);
    };
  }, []);

  return (
    <>
      <Chart
        values={currentValues}
        color={props.color}
        tickDateFormatter={(d) => d.toLocaleTimeString()}
        width={props.width}
        height={props.height}
      />
    </>
  );
}
