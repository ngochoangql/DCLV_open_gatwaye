import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

const SensorDataChart = (props) => {
  const { sensorData, title } = props;
  const [revision, setRevision] = useState(0);
  let opacity = "1";

  useEffect(() => {
    setRevision(revision + 1);
    if (sensorData && sensorData.length) {
      if (sensorData[0].x && sensorData[0].x.length) {
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sensorData]);

  return (
    <Plot
      data={sensorData}
      revision={revision}
      style={{ width: "100%", height: "100%", opacity }}
      layout={{
        title,
        visible: false,
        autosize: true,
        margin: {
          l: 50,
          r: 50,
          b: 100,
          t: 100,
          pad: 4,
        },
        xaxis: {
          autorange: true,
          tickformat: '.1f'
        },
        yaxis: {
          autorange: true,
          tickformat: '.1f'
        },
      }}
    />
  );
};

export default SensorDataChart;
