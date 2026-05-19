import axios from "axios";

const API = axios.create({
  baseURL: "https://curriculum-alignment-ai.onrender.com/api"
});

export const uploadCurriculum = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await API.post("/upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });

    return response.data;

  } catch (error) {
    console.error("Upload failed:", error);
    throw error;
  }
};