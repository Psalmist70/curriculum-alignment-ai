import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function Charts({ analytics }) {

  const data = [
    {
      name: "High",
      value: analytics.high_match
    },
    {
      name: "Medium",
      value: analytics.medium_match
    },
    {
      name: "Low",
      value: analytics.low_match
    }
  ];

  return (

    <div className="bg-white p-6 rounded-xl shadow my-6">

      <h2 className="text-xl font-bold mb-4">
        Alignment Distribution
      </h2>

      <ResponsiveContainer width="100%" height={300}>

        <BarChart data={data}>

          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" />

        </BarChart>

      </ResponsiveContainer>

    </div>
  );
}