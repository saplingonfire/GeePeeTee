import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function RenderBarCharts(data) {
  return (
    <ResponsiveContainer width="100%" height="80%">
      <BarChart
        data={data}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name"/>
        <Tooltip shared={false} trigger="hover" wrapperStyle={{width: "auto"}} contentStyle={{backgroundColor: 'rgba(255, 255, 255, 0.75)', borderRadius: "10px"}}/>
        <Bar dataKey="Score" fill="#bb0000" />
        <Bar dataKey="out of" name='Dimension_total' fill="#999999" />
      </BarChart>
    </ResponsiveContainer>
  );
}
