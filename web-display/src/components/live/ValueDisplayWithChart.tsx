import { MeasurementType } from "../../services/data";
import { ValueDisplay } from "./ValueDisplay";
import { LatestValuesChart } from "./ValuesChart";

interface ValueDisplayWithChartProps {
  measurementType: MeasurementType;
  valueFormatter: (v: number) => string;
  color: string;
  width: number;
  height: number;
}

export function ValueDisplayWithChart(props: ValueDisplayWithChartProps) {
  return (
    <>
      <ValueDisplay
        measurementType={props.measurementType}
        valueFormatter={props.valueFormatter}
      />
      <LatestValuesChart
        measurementType={props.measurementType}
        color={props.color}
        width={props.width}
        height={props.height}
      />
    </>
  );
}
