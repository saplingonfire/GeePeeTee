import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export default function RenderBarCharts(data) {
  return (
    <BarChart
      width={500}
      height={300}
      data={data}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <Tooltip shared={false} trigger="hover" />
      <Bar dataKey="Score" fill="#bb0000" />
      <Bar dataKey="out of" name='Dimension Total' fill="#999999" />
    </BarChart>
  );
}
