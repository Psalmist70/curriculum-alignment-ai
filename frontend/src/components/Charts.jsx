import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

export default function Charts({ analytics }) {

  const data = [
    { name: "High", value: analytics.high_match },
    { name: "Medium", value: analytics.medium_match },
    { name: "Low", value: analytics.low_match },
  ];

  const COLORS = ["#10b981", "#6366f1", "#f43f5e"];

  return (
    <div className="bg-white rounded-3xl p-8 shadow-lg mt-10">

      <h2 className="text-2xl font-bold mb-6 text-center">
        Alignment Distribution
      </h2>

      <div className="flex justify-center">

        <PieChart width={350} height={300}>

          <Pie
            data={data}
            cx="50%"
            cy="50%"
            label
            outerRadius={110}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={index} fill={COLORS[index]} />
            ))}
          </Pie>

          <Tooltip />
          <Legend />

        </PieChart>

      </div>

    </div>
  );
}