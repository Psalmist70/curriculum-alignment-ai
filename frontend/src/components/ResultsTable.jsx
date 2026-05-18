export default function ResultsTable({ results }) {

  return (

    <div className="bg-white p-6 rounded-xl shadow overflow-x-auto">

      <table className="w-full border-collapse">

        <thead>

          <tr className="bg-gray-100">

            <th className="p-3 text-left">Course</th>
            <th className="p-3 text-left">Matched Job</th>
            <th className="p-3 text-left">Score</th>
            <th className="p-3 text-left">Missing Skills</th>

          </tr>

        </thead>

        <tbody>

          {results.map((r, i) => (

            <tr key={i} className="border-t">

              <td className="p-3">{r.course_name}</td>

              <td className="p-3">{r.matched_job}</td>

              <td className="p-3">
                {r.similarity_score}
              </td>

              <td className="p-3">
                {r.missing_skills.join(", ")}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}