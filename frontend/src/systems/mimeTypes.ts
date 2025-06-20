function getSupportedMimeType() {
  const mimeTypes = [
    "audio/webm;codecs=opus", // Best quality & compression
    "audio/webm", // Fallback WebM
    "audio/mp3", // Works on Safari
    "audio/wav", // Large file size, but widely supported
  ];

  return mimeTypes.find((type) => MediaRecorder.isTypeSupported(type)) || "";
}

function getAudioFileExtension(mimeType: string): string {
  const mimeTypeToExtension: Record<string, string> = {
    "audio/wav": ".wav",
    "audio/mpeg": ".mp3",
    "audio/ogg": ".ogg",
    "audio/webm": ".webm",
    "audio/flac": ".flac",
  };

  // Normalize MIME type (ignore parameters like codecs)
  const baseMimeType = mimeType.split(";")[0];

  return mimeTypeToExtension[baseMimeType] || ".bin"; // Default to .bin if unknown
}

function getAudioMimeType(filename: string): string {
  const split = filename.split(".");
  const ext = split[split.length - 1].toLowerCase();
  const mimeTypes: Record<string, string> = {
    wav: "audio/wav",
    mp3: "audio/mpeg",
    ogg: "audio/ogg",
    webm: "audio/webm",
    flac: "audio/flac",
  };

  return mimeTypes[ext] || "audio/wav";
}

export { getSupportedMimeType, getAudioFileExtension, getAudioMimeType };
