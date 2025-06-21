import { TConversation } from "@/types/chat";
import { formData_post, TApiResponse } from "./serviceConfig";
import Services from "./serviceUrls";
import { getAudioFileExtension } from "@/systems/mimeTypes";

export interface TEnquiryAgentRequest {
  conversation: TConversation;
  audio_blob: Blob | null;
}
export interface TEnquiryAgentResponse {
  conversation: TConversation;
  audio_base64: string;
  end_conversation: boolean;
}

export interface TLeadfinderAgentRequest {
  customer_id: string;
  conversation: TConversation;
  audio_blob: Blob | null;
}
export interface TLeadfinderAgentResponse {
  customer_id: string;
  conversation: TConversation;
  audio_base64: string;
  end_conversation: boolean;
}

async function enquiryAgent(
  data: TEnquiryAgentRequest,
): Promise<TApiResponse<TEnquiryAgentResponse>> {
  const formData = new FormData();
  formData.append("conversation", JSON.stringify(data.conversation));

  if (data.audio_blob && data.audio_blob.size < 50 * 1024 * 1024) {
    // 50MB in bytes
    // Determine the file extension based on the MIME type

    const extension = getAudioFileExtension(data.audio_blob.type);

    formData.append("audio", data.audio_blob, `recording${extension}`);
  }

  return formData_post(Services.enquiryAgent, formData);
}

async function leadfinderAgent(
  data: TLeadfinderAgentRequest,
): Promise<TApiResponse<TLeadfinderAgentResponse>> {
  const formData = new FormData();
  formData.append("conversation", JSON.stringify(data.conversation));
  formData.append("customer_id", data.customer_id);

  if (data.audio_blob && data.audio_blob.size < 50 * 1024 * 1024) {
    // 50MB in bytes
    // Determine the file extension based on the MIME type

    const extension = getAudioFileExtension(data.audio_blob.type);

    formData.append("audio", data.audio_blob, `recording${extension}`);
  }

  return formData_post(Services.leadfinderAgent, formData);
}

const AIAgentService = {
  enquiryAgent,
  leadfinderAgent,
};

export default AIAgentService;
