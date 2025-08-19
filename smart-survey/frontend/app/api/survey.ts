import { API_URL } from "../../config";
import axios from "axios";

export const getSurveys = async () => {
  const res = await axios.get(`${API_URL}/api/surveys`);
  return res.data;
};
