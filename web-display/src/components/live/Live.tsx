import { Link } from "react-router";
import { getColor } from "../../services/colorService";
import { MeasurementType } from "../../services/data";
import useWindowDimensions from "../useWindowDimensions";
import { ValueDisplayWithChart } from "./ValueDisplayWithChart";
function Live() {
  const { height, width } = useWindowDimensions();

  return (
    <>
      <ValueDisplayWithChart
        measurementType={MeasurementType.TEMPERATURE}
        valueFormatter={(v) => `${v} °C`}
        color={getColor(MeasurementType.TEMPERATURE)}
        height={height / 3}
        width={width * 0.9}
        subscriptionAvailable={false}
      />
      <br />
      <ValueDisplayWithChart
        measurementType={MeasurementType.HUMIDITY}
        valueFormatter={(v) => `${v} %`}
        color={getColor(MeasurementType.HUMIDITY)}
        height={height / 3}
        width={width * 0.9}
        subscriptionAvailable={true}
      />
      <Link to={"/history"}>
        <button>past values</button>
      </Link>
    </>
  );
}

export default Live;
