// src/App.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/history?days=7")
      .then(({ data }) => {
        const formatted = data.history.map(
          ({ timestamp, price, prediction }) => ({
            timestamp: new Date(timestamp).getTime(),
            price,
            pred: prediction,
          })
        );
        setData(formatted);
      })
      .catch(console.error);
  }, []);

  const CustomDot = ({ cx, cy, payload }) => {
    if (payload.pred !== 0 && payload.pred !== 1) return null;
    return (
      <circle
        cx={cx}
        cy={cy}
        r={4}
        fill={payload.pred === 1 ? "green" : "red"}
        stroke="none"
      />
    );
  };

  function CustomTooltip({ active, payload, label }) {
    if (!active || !payload?.length) return null;

    // payload[0].payload is the original data object: { timestamp, price, pred }
    const { price, pred } = payload[0].payload;

    const time = new Date(label).toLocaleTimeString([], {
      month: "numeric",
      day: "numeric",
      hour12: false,
      hour: "2-digit",
      minute: "2-digit",
    });

    return (
      <div
        style={{
          background: "#fff",
          padding: "0.5rem 1rem",
          border: "1px solid #ccc",
          borderRadius: 4,
        }}
      >
        <p style={{ margin: 0, fontWeight: "bold" }}>{time}</p>
        <p style={{ margin: "0.25rem 0" }}>Price: {price.toFixed(2)}</p>
        <p style={{ margin: 0 }}>Prediction: {pred === 1 ? "Buy" : "None"}</p>
      </div>
    );
  }
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        height: "100vh",
        fontFamily: "sans-serif",
      }}
    >
      {/* Left panel */}
      <div
        style={{
          flex: "0 0 30%",
          padding: "2rem",
          boxSizing: "border-box",
          backgroundColor: "#f5f5f5",
        }}
      >
        <h1>Hourly Price &amp; Predictions</h1>
        <p>
          This chart shows the last 7 days of hourly closing prices for AAPL,
          with green dots indicating “pred = 1” signals (buy) and red dots for
          “pred = 0” (sell/hold). Hover over any point to see the exact time and
          price.
        </p>
        <p>
          Github repo can be found{" "}
          <a
            href="https://github.com/mohamad-damaj/Auto-trader"
            target="_blank"
            rel="noreferrer"
          >
            {" "}
            here
          </a>
          .
        </p>
        <p>
          DISCLAIMER: Please do not use this to make any form of descision,
          without the intent of actual use.
        </p>
      </div>

      {/* Right panel: chart */}
      <div
        style={{
          flex: 1,
          padding: "2rem",
          boxSizing: "border-box",
        }}
      >
        <ResponsiveContainer width="90%" height="100%">
          <ComposedChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="timestamp"
              type="number"
              scale="time"
              domain={["auto", "auto"]}
              tick={false}
              label={{
                value: "Date & Time",
                offset: 10,
                position: "middle",

                style: { textAnchor: "middle" },
              }}
            />

            <YAxis
              domain={["auto", "auto"]}
              label={{
                value: "Price (USD)",
                angle: -90,
                position: "insideLeft",
                offset: 10,
                style: { textAnchor: "middle" },
              }}
            />

            <Tooltip
              content={<CustomTooltip />}
              cursor={{ stroke: "#888", strokeDasharray: "5 5" }}
            />

            <Line
              type="monotone"
              dataKey="price"
              stroke="#8884d8"
              dot={false}
              name="Close Price"
            />

            <Scatter dataKey="price" shape={CustomDot} name="Prediction" />

            <Legend verticalAlign="top" height={36} />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;
