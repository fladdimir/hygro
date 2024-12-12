import { useEffect, useState } from "react";
import { latestValueService } from "../../services/LatestValueService";
import { formatTime, Measurement, MeasurementType } from "../../services/data";

interface ValueDisplayProps {
  measurementType: MeasurementType;
  valueFormatter: (v: number) => string;
}

export function ValueDisplay(props: ValueDisplayProps) {
  const [currentValue, setCurrentValue] = useState<Measurement | undefined>(
    undefined
  );

  function handleMeasurement(m: Measurement) {
    if (
      m.measurement_type === props.measurementType &&
      (!currentValue || m.tsp > currentValue.tsp)
    ) {
      setCurrentValue(m);
    }
  }

  useEffect(() => {
    // setup
    latestValueService.addListener(handleMeasurement, 1);
    return () => {
      // cleanup
      latestValueService.removeListener(handleMeasurement);
      setCurrentValue(undefined);
    };
  }, []);

  return (
    <>
      <div style={{ fontSize: "32px" }}>
        {currentValue ? (
          <>
            {props.valueFormatter(currentValue.value)}
            <br />
            <div style={{ fontSize: "16px" }}>
              {`${formatTime(currentValue.tsp)}`}
            </div>
          </>
        ) : (
          <>-</>
        )}
      </div>
    </>
  );
}
