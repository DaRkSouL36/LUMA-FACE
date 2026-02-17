import axios, { AxiosError } from "axios";
import { EnhancementResponse, ApiError } from "@/TYPES/api";

// 1. CREATE AXIOS INSTANCE
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 300000, // INCREASED TO 5 MINUTES (300,000 MS)
  headers: {
    Accept: "application/json",
  },
});

// 2. ERROR PARSER UTILITY
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

  try {
    const response = await api.post<EnhancementResponse>(
      "/images/enhance",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      },
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};
