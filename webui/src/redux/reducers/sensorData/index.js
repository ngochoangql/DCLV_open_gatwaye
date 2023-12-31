import {
  SET_STREAM_SENSOR_DATA,
  SET_STREAM_SENSOR_RECORD_DATA,
  SET_STREAM_SENSOR_DATA_RESET,
} from "../../actions/actionTypes";

const initialState = {
  sensorSimpleData: new Float32Array(),
  sensorRecordedData: new Float32Array(),
};

export default function sensorData(state = initialState, action) {
  switch (action.type) {
    case SET_STREAM_SENSOR_DATA_RESET:
      return {
        ...state,
        sensorSimpleData: new Float32Array(),
        sensorRecordedData: new Float32Array(),
      };
    case SET_STREAM_SENSOR_DATA:
      return {
        ...state,
        sensorSimpleData: [...action.payload],
      };
    case SET_STREAM_SENSOR_RECORD_DATA:
      return {
        ...state,
        sensorRecordedData: [...action.payload],
      };
    default:
      return state;
  }
}
