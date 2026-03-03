"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface ScoreOverviewChartProps {
  data: Array<{
    name: string;
    "Final Score": number;
    "Skill Match": number;
    "Experience Match": number;
  }>;
}

export default function ScoreOverviewChart({ data }: ScoreOverviewChartProps) {
  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          margin={{
            top: 20,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#1e3a5f" />
          <XAxis
            dataKey="name"
            tick={{ fill: "#22d3ee", fontSize: 12 }}
            axisLine={{ stroke: "#06b6d4" }}
            tickLine={{ stroke: "#06b6d4" }}
          />
          <YAxis
            tick={{ fill: "#22d3ee", fontSize: 12 }}
            axisLine={{ stroke: "#06b6d4" }}
            tickLine={{ stroke: "#06b6d4" }}
            domain={[0, 100]}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "rgba(10, 25, 47, 0.95)",
              border: "1px solid rgba(6, 182, 212, 0.4)",
              borderRadius: "12px",
              color: "#f1f5f9",
              boxShadow: "0 0 20px rgba(6, 182, 212, 0.3)",
            }}
            labelStyle={{ color: "#22d3ee", fontWeight: "bold" }}
            cursor={{ fill: "rgba(6, 182, 212, 0.1)" }}
          />
          <Legend
            wrapperStyle={{ paddingTop: "20px" }}
            formatter={(value) => <span style={{ color: "#22d3ee" }}>{value}</span>}
          />
          <Bar
            dataKey="Final Score"
            fill="url(#colorFinal)"
            radius={[6, 6, 0, 0]}
            maxBarSize={50}
          />
          <Bar
            dataKey="Skill Match"
            fill="url(#colorSkill)"
            radius={[6, 6, 0, 0]}
            maxBarSize={50}
          />
          <Bar
            dataKey="Experience Match"
            fill="url(#colorExperience)"
            radius={[6, 6, 0, 0]}
            maxBarSize={50}
          />
          <defs>
            <linearGradient id="colorFinal" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#22d3ee" stopOpacity={1} />
              <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.6} />
            </linearGradient>
            <linearGradient id="colorSkill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#60a5fa" stopOpacity={1} />
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.6} />
            </linearGradient>
            <linearGradient id="colorExperience" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#34d399" stopOpacity={1} />
              <stop offset="95%" stopColor="#10b981" stopOpacity={0.6} />
            </linearGradient>
          </defs>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

