import { useState } from "react";

import UploadBox from "./components/UploadBox";
import AnalyticsCards from "./components/AnalyticsCards";
import Charts from "./components/Charts";
import ResultsTable from "./components/ResultsTable";

export default function App() {

  const [data, setData] = useState(null);

  return (

    <div className="min-h-screen">

      {/* HERO SECTION */}

      <div className="relative overflow-hidden">

        <div className="absolute inset-0 bg-gradient-to-r from-blue-700 to-indigo-700 opacity-95"></div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 py-20 text-center text-white">

          <h1 className="text-5xl md:text-6xl font-extrabold mb-6 leading-tight">

            Dynamic Curriculum
            <br />
            Alignment System

          </h1>

          <p className="max-w-3xl mx-auto text-lg md:text-xl text-blue-100 leading-relaxed">

            An intelligent AI-powered platform that analyzes
            academic curriculum structures against industry
            job market requirements to detect skill gaps,
            improve employability, and enhance curriculum relevance.

          </p>

          <div className="mt-10 flex justify-center gap-6 flex-wrap">

            <div className="bg-white/10 backdrop-blur-md px-6 py-4 rounded-2xl border border-white/20 shadow-xl">

              <h3 className="text-3xl font-bold">
                AI
              </h3>

              <p className="text-blue-100">
                Smart Matching
              </p>

            </div>

            <div className="bg-white/10 backdrop-blur-md px-6 py-4 rounded-2xl border border-white/20 shadow-xl">

              <h3 className="text-3xl font-bold">
                FAISS
              </h3>

              <p className="text-blue-100">
                Fast Similarity Search
              </p>

            </div>

            <div className="bg-white/10 backdrop-blur-md px-6 py-4 rounded-2xl border border-white/20 shadow-xl">

              <h3 className="text-3xl font-bold">
                Analytics
              </h3>

              <p className="text-blue-100">
                Curriculum Insights
              </p>

            </div>

          </div>

        </div>

      </div>

      {/* MAIN CONTENT */}

      <div className="max-w-7xl mx-auto px-6 py-10">

        <UploadBox setData={setData} />

        {/* FEATURE CARDS */}

        <div className="grid md:grid-cols-3 gap-6 my-12">

          <div className="bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition duration-300 border border-gray-100">

            <div className="text-5xl mb-4">
              📊
            </div>

            <h2 className="text-2xl font-bold mb-3">
              Alignment Analysis
            </h2>

            <p className="text-gray-600 leading-relaxed">

              Compare curriculum content directly against
              real-world industry job requirements.

            </p>

          </div>

          <div className="bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition duration-300 border border-gray-100">

            <div className="text-5xl mb-4">
              🧠
            </div>

            <h2 className="text-2xl font-bold mb-3">
              Skill Gap Detection
            </h2>

            <p className="text-gray-600 leading-relaxed">

              Automatically identify missing skills needed
              for modern industry demands.

            </p>

          </div>

          <div className="bg-white rounded-3xl p-8 shadow-lg hover:shadow-2xl transition duration-300 border border-gray-100">

            <div className="text-5xl mb-4">
              🚀
            </div>

            <h2 className="text-2xl font-bold mb-3">
              Intelligent Recommendations
            </h2>

            <p className="text-gray-600 leading-relaxed">

              Generate actionable recommendations for
              curriculum improvement and enhancement.

            </p>

          </div>

        </div>

        {/* RESULTS */}

        {data && (

          <>
            <AnalyticsCards analytics={data.analytics} />

            <Charts analytics={data.analytics} />

            <ResultsTable results={data.results} />
          </>

        )}

      </div>

    </div>
  );
}
