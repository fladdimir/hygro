import { Link } from "react-router";
import { Chart } from "../Chart";
import { useState } from "react";
import { Measurement, MeasurementType } from "../../services/data";
import { historicValueService } from "../../services/HistoricValueService";
import { getColor } from "../../services/colorService";
import useWindowDimensions from "../useWindowDimensions";

// https://stackoverflow.com/a/60884408
function toLocalISOString(date: Date) {
  const localDate = new Date((date as any) - date.getTimezoneOffset() * 60000);
  //offset in milliseconds. Credit https://stackoverflow.com/questions/10830357/javascript-toisostring-ignores-timezone-offset
  // Optionally remove second/millisecond if needed
  localDate.setSeconds(null as any);
  localDate.setMilliseconds(null as any);
  return localDate.toISOString().slice(0, -1);
}

function History() {
  const { height, width } = useWindowDimensions();

  const now = new Date();
  const nowStr = toLocalISOString(now);
  const nowMinusXh = new Date(
    new Date(now).setTime(now.getTime() + -8 * 60 * 60 * 1000)
  );
  const nowMinusXhStr = toLocalISOString(nowMinusXh);

  const [fromDateStr, setFromDateStr] = useState(nowMinusXhStr);
  const [toDateStr, setToDateStr] = useState(nowStr);
  const [measurementType, setMeasurementType] = useState(
    MeasurementType.HUMIDITY
  );
  const [isWaiting, setIsWaiting] = useState(false);

  const [data, setData] = useState<Measurement[]>([]);

  const runQuery = async () => {
    const fromDate = new Date(fromDateStr);
    const toDate = new Date(toDateStr);
    setIsWaiting(true);
    let values = await historicValueService.getValues(
      fromDate,
      toDate,
      measurementType
    );
    setIsWaiting(false);
    setData(values);
  };

  return (
    <>
      <input
        type="datetime-local"
        style={{ margin: "10px", height: "25px" }}
        value={fromDateStr}
        onChange={(ev) => setFromDateStr(ev.target.value)}
      ></input>
      -
      <input
        type="datetime-local"
        style={{ margin: "10px", height: "25px" }}
        value={toDateStr}
        onChange={(ev) => setToDateStr(ev.target.value)}
      ></input>
      <select
        style={{ margin: "10px", height: "32px" }}
        value={measurementType}
        onChange={(ev) =>
          setMeasurementType(ev.target.value as MeasurementType)
        }
      >
        {Object.values(MeasurementType).map((mt) => (
          <option value={mt} key={mt}>
            {mt}
          </option>
        ))}
      </select>
      <button
        onClick={() => runQuery()}
        disabled={isWaiting}
        style={{ margin: "10px" }}
      >
        Query data
      </button>
      <Chart
        values={data}
        color={getColor(measurementType)}
        tickDateFormatter={(d) => d.toLocaleString()}
        width={width * 0.95}
        height={height * 0.65}
      />
      <Link to={"/"}>
        <button>Live</button>
      </Link>
    </>
  );
}

export default History;
