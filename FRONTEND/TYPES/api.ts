export interface EnhancementMetrics {
  psnr: number;
  ssim: number;
  lpips: number;
  identity_score: number;
}

export interface EnhancementResponse {
  success: boolean;
  message: string;
  image_base64: string; 
  metrics: EnhancementMetrics;
  processing_time_ms: number;
}

export interface ApiError {
  detail: string;
}