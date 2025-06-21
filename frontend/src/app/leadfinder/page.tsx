"use client";
import { useEffect, useRef, useState } from "react";
import styles from "./styles.module.css";
import { TConversation } from "@/types/chat";
import AIAgentService from "@/services/aiagent";
import { getSupportedMimeType } from "@/systems/mimeTypes";

export default function Leadfinder() {
  const [hasStarted, setHasStarted] = useState(false);
  const customer_id = useRef<string>("");
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

        const response = await AIAgentService.leadfinderAgent({
          customer_id: customer_id.current,
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
    const response = await AIAgentService.leadfinderAgent({
      customer_id: "",
      conversation: [],
      audio_blob: null,
    });

    if (response.success) {
      setConversation(response.data.conversation);
      customer_id.current = response.data.customer_id;
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
    <div className={styles.page}>
      <div style={{ marginTop: "1rem" }}>
        {conversation.map((chat, index) => (
          <div key={index}>
            <strong>{chat.role}</strong>: {chat.content}
          </div>
        ))}
      </div>
      {!hasStarted ? (
        <button onClick={handleStart}>
          Start Leadfinder Agent Call Simulation
        </button>
      ) : isRecording ? (
        <button onClick={stopRecording} disabled={!isRecording}>
          Stop Recording
        </button>
      ) : null}
    </div>
  );
}
