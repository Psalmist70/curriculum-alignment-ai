export default function AnalyticsCards({ analytics }) {
  if (!analytics) return null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 my-6">

      <div className="bg-white p-4 rounded-xl shadow">
        <h3>Total Courses</h3>
        <p className="text-2xl font-bold">
          {analytics.total_courses}
        </p>
      </div>

      <div className="bg-white p-4 rounded-xl shadow">
        <h3>Average Score</h3>
        <p className="text-2xl font-bold">
          {analytics.average_score?.toFixed(2)}
        </p>
      </div>

      <div className="bg-white p-4 rounded-xl shadow">
        <h3>High Match</h3>
        <p className="text-2xl font-bold">
          {analytics.high_match}
        </p>
      </div>

      <div className="bg-white p-4 rounded-xl shadow">
        <h3>Low Match</h3>
        <p className="text-2xl font-bold">
          {analytics.low_match}
        </p>
      </div>

    </div>
  );
}
