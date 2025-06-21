"use client";
import { useEffect, useRef, useState } from "react";
import styles from "../chat.module.css";
import { TConversation } from "@/types/chat";
import AIAgentService from "@/services/aiagent";
import { getSupportedMimeType } from "@/systems/mimeTypes";
import { LuBot, LuUser } from "react-icons/lu";

export default function Enquiry() {
  const [hasStarted, setHasStarted] = useState(false);
  const [conversation, setConversation] = useState<TConversation>([]);
  const conversationRef = useRef<TConversation>(conversation);
  const [isRecording, setIsRecording] = useState(false);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const recordedChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    const mimeType = getSupportedMimeType();
    if (!mimeType) {
      console.error("No supported audio format available");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType, // Efficient format
        audioBitsPerSecond: 32000, // Lower bitrate for optimized size
      });
      mediaRecorderRef.current = mediaRecorder;
      recordedChunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) recordedChunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(recordedChunksRef.current, {
          type: mimeType,
        });

        const response = await AIAgentService.enquiryAgent({
          conversation: conversationRef.current,
          audio_blob: audioBlob,
        }); // pass FormData directly

        if (response.success) {
          setConversation(response.data.conversation);
          playBase64Audio(response.data.audio_base64, () => {
            if (!response.data.end_conversation) {
              startRecording();
            }
          });
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  const playBase64Audio = (base64: string, onEnd: () => void) => {
    if (!base64) return;
    const audio = new Audio("data:audio/mp3;base64," + base64);
    audio.play();
    audio.onended = onEnd;
  };

  const handleStart = async () => {
    setHasStarted(true);
    const response = await AIAgentService.enquiryAgent({
      conversation: [],
      audio_blob: null,
    });

    if (response.success) {
      setConversation(response.data.conversation);
      playBase64Audio(response.data.audio_base64, () => {
        if (!response.data.end_conversation) {
          startRecording();
        }
      });
    }
  };

  useEffect(() => {
    conversationRef.current = conversation;
  }, [conversation]);

  return (
    <div className={`${styles.agent} disf fldc aic`}>
      <div className={`${styles.chatcontainer}`}>
        {conversation.map((chat, index) => {
          if (chat.role === "assistant" || chat.role === "user")
            return (
              <div
                className={`${styles.chat} disf aic ${chat.role === "assistant" ? "jcfs" : "jcfe"}`}
                key={index}
              >
                <div
                  className={`disf fldc ${chat.role === "assistant" ? "aifs" : "aife"}`}
                >
                  <strong className={styles.icon}>
                    {chat.role === "assistant" ? <LuBot /> : <LuUser />}
                  </strong>
                  <div
                    className={`${chat.role === "assistant" ? styles.left : styles.right}`}
                  >
                    {chat.content}
                  </div>
                </div>
              </div>
            );
        })}
      </div>
      {!hasStarted ? (
        <button onClick={handleStart}>
          Start Enquiry Agent Call Simulation
        </button>
      ) : isRecording ? (
        <button onClick={stopRecording} disabled={!isRecording}>
          Stop Recording
        </button>
      ) : null}
    </div>
  );
}
