import { useEffect, useState } from "react";
import { latestValueService } from "../../services/LatestValueService";
import { Measurement, MeasurementType } from "../../services/data";

interface ValueDisplayProps {
  measurementType: MeasurementType;
  valueFormatter: (v: number) => string;
}

export function ValueDisplay(props: ValueDisplayProps) {
  const [currentValue, setCurrentValue] = useState<Measurement | undefined>(
    undefined
  );

  function handleMeasurement(m: Measurement) {
    if (m.measurement_type === props.measurementType) {
      setCurrentValue(m);
    }
  }

  useEffect(() => {
    // setup
    latestValueService.addListener(handleMeasurement);
    return () => {
      // cleanup
      latestValueService.removeListener(handleMeasurement);
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
              {`${new Date(currentValue.tsp).toLocaleTimeString()}`}
            </div>
          </>
        ) : (
          <>-</>
        )}
      </div>
    </>
  );
}
