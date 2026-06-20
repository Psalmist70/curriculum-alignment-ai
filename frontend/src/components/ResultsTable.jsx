export default function ResultsTable({ results }) {

  if (!results) return null;

  const safeResults = results || [];

  return (

    <div className="bg-white p-6 rounded-xl shadow overflow-x-auto">

      <table className="w-full border-collapse">

        <thead>

          <tr className="bg-gray-100">

            <th className="p-3 text-left">Course</th>
            <th className="p-3 text-left">Matched Job</th>
            <th className="p-3 text-left">Score</th>
            <th className="p-3 text-left">Missing Skills</th>
            <th className="p-3 text-left">Recommendations</th>

          </tr>

        </thead>

        <tbody>

          {safeResults.map((r, i) => (

            <tr key={i} className="border-t">

              <td className="p-3">{r.course_name}</td>

              <td className="p-3">{r.matched_job}</td>

              <td className="p-3 font-semibold text-indigo-600">
                {r.similarity_score?.toFixed(2)}
              </td>

              <td className="p-3 text-red-600">
                {r.missing_skills?.length
                  ? r.missing_skills.join(", ")
                  : "None"}
              </td>

              <td className="p-3 text-green-700">

                {r.recommendations?.length
                  ? r.recommendations.map((rec, idx) => (
                      <div key={idx}>• {rec}</div>
                    ))
                  : "No recommendations"}

              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}
