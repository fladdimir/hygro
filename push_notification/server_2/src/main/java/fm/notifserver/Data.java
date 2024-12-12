package fm.notifserver;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Data {

    private static final ObjectMapper mapper = new ObjectMapper();

    enum MeasurementType {
        HUMIDITY, TEMPERATURE
    }

    record MeasurementData(String sensor_id, String tsp, MeasurementType measurement_type, double value) {

        public static MeasurementData fromString(String string) {
            try {
                return mapper.readValue(string, MeasurementData.class);
            } catch (JsonProcessingException e) {
                throw new IllegalArgumentException(e);
            }
        }

        public static String toString(MeasurementData data) {
            try {
                return mapper.writeValueAsString(data);
            } catch (JsonProcessingException e) {
                throw new IllegalArgumentException(e);
            }
        }
    }

}
