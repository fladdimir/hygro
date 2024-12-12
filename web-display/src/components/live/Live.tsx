import { ValueDisplayWithChart } from "./ValueDisplayWithChart";
import { MeasurementType } from "../../services/data";
import { Link } from "react-router";
import { getColor } from "../../services/colorService";
import useWindowDimensions from "../useWindowDimensions";
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
      />
      <br />
      <ValueDisplayWithChart
        measurementType={MeasurementType.HUMIDITY}
        valueFormatter={(v) => `${v} %`}
        color={getColor(MeasurementType.HUMIDITY)}
        height={height / 3}
        width={width * 0.9}
      />
      <Link to={"/history"}>
        <button>past values</button>
      </Link>
    </>
  );
}

export default Live;
