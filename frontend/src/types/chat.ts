export interface TChat {
  role: "assistant" | "tool" | "user" | "system";
  name?: string;
  content: string;
}

export type TConversation = TChat[];
