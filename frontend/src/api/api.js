import axios from "axios";

const API = axios.create({
  baseURL: "https://curriculum-alignment-ai.onrender.com/api"
});

export const uploadCurriculum = async (file) => {

  const formData = new FormData();

  formData.append("file", file);

  return await API.post("/upload/", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
};