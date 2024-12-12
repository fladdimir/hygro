import { MeasurementType } from "../../services/data";
import NotificationSubscription from "./NotificationSubscription";
import { ValueDisplay } from "./ValueDisplay";
import { LatestValuesChart } from "./ValuesChart";

interface ValueDisplayWithChartProps {
  measurementType: MeasurementType;
  valueFormatter: (v: number) => string;
  color: string;
  width: number;
  height: number;
  subscriptionAvailable: boolean;
}

export function ValueDisplayWithChart(props: ValueDisplayWithChartProps) {
  return (
    <>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <ValueDisplay
          measurementType={props.measurementType}
          valueFormatter={props.valueFormatter}
        />
        <div style={{ width: "25px" }} />
        <NotificationSubscription available={props.subscriptionAvailable} />
      </div>
      <LatestValuesChart
        measurementType={props.measurementType}
        color={props.color}
        width={props.width}
        height={props.height}
      />
    </>
  );
}
