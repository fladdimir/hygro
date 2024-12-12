import {
  CartesianGrid,
  Line,
  LineChart,
  Tooltip,
  TooltipProps,
  XAxis,
  YAxis,
} from "recharts";
import { Measurement } from "../services/data";
import {
  NameType,
  ValueType,
} from "recharts/types/component/DefaultTooltipContent";

type ChartProps = {
  values: Measurement[];
  color: string;
  tickDateFormatter: (d: Date) => string;
  width: number;
  height: number;
};

const CustomTooltip = ({
  active,
  payload,
  label,
}: TooltipProps<ValueType, NameType>) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="label">{`${new Date(label).toLocaleString()} : ${
          payload?.[0].value
            ? Math.round(payload?.[0].value as number)
            : undefined
        }`}</p>
      </div>
    );
  }

  return null;
};
export function Chart(props: ChartProps) {
  return (
    <>
      <LineChart width={props.width} height={props.height} data={props.values}>
        <XAxis
          dataKey="tsp"
          type="number"
          tickFormatter={(v: number) => props.tickDateFormatter(new Date(v))}
          domain={["dataMin", "dataMax"]}
        />
        <YAxis dataKey="value" domain={["auto", "auto"]} />
        <Line
          type="monotone"
          dataKey="value"
          isAnimationActive={false}
          stroke={props.color}
        />
        <CartesianGrid stroke="#555" strokeDasharray="5 5" />
        <Tooltip isAnimationActive={false} content={<CustomTooltip />} />
      </LineChart>
    </>
  );
}
