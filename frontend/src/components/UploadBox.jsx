import { useState } from "react";
import { uploadCurriculum } from "../api/api";

export default function UploadBox({ setData }) {

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {

    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    setLoading(true);

    try {

      const response = await uploadCurriculum(file);

      console.log(response.data);

      setData(response.data);

    } catch (error) {

      console.error(error);

      if (error.response) {

        alert(error.response.data.error || "Upload failed");

      } else {

        alert("Server connection failed");

      }

    }

    setLoading(false);
  };

  return (

    <div className="bg-white rounded-3xl shadow-xl p-10 border border-gray-100">

      <div className="text-center mb-8">

        <h2 className="text-3xl font-bold text-gray-800 mb-3">

          Upload Curriculum Dataset

        </h2>

        <p className="text-gray-500">

          Upload your curriculum CSV file for intelligent alignment analysis.

        </p>

      </div>

      <div className="border-2 border-dashed border-blue-300 rounded-2xl p-10 text-center bg-blue-50 hover:bg-blue-100 transition duration-300">

        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
          className="block mx-auto mb-5"
        />

        {file && (

          <p className="text-blue-700 font-medium mb-4">

            Selected:
            {" "}
            {file.name}

          </p>

        )}

        <button
          onClick={handleUpload}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-800 transition duration-300 text-white px-8 py-3 rounded-xl text-lg font-semibold shadow-lg hover:scale-105"
        >

          {loading
            ? "Analyzing Curriculum..."
            : "Upload & Analyze"}

        </button>

      </div>

    </div>
  );
}
