export interface TChat {
  role: "assistant" | "tool" | "user";
  content: string;
}

export type TConversation = TChat[];
