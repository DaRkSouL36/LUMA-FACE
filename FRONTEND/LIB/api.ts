import axios, { AxiosError } from "axios";
import { EnhancementResponse, ApiError } from "@/TYPES/api";

// 1. CREATE AXIOS INSTANCE
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 60000, // 60 SECONDS TIMEOUT FOR HEAVY INFERENCE
  headers: {
    Accept: "application/json",
  },
});

// 2. ERROR PARSER UTILITY
// EXTRACTS READABLE ERROR MESSAGES FROM BACKEND RESPONSES
export const getErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>;
    if (axiosError.response?.data?.detail) {
      return axiosError.response.data.detail.toUpperCase();
    }
    if (axiosError.message) {
      return axiosError.message.toUpperCase();
    }
  }
  return "AN UNEXPECTED ERROR OCCURRED".toUpperCase();
};

// 3. API METHODS
export const enhanceImage = async (
  file: File,
): Promise<EnhancementResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  // OPTIONAL: ADD UPSCALE FACTOR IF WE WANT TO MAKE IT CONFIGURABLE LATER
  // formData.append('upscale_factor', '2')

  try {
    const response = await api.post<EnhancementResponse>(
      "/images/enhance",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        // OPTIONAL: TRACK UPLOAD PROGRESS HERE IF NEEDED
      },
    );
    return response.data;
  } catch (error) {
    throw error; // RE-THROW TO BE CAUGHT BY THE COMPONENT
  }
};
