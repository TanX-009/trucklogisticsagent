async function playAudioAndWait(src) {
  const audio = document.getElementById("audio");
  audio.src = src;
  await audio.play();
  return new Promise((resolve) => {
    audio.onended = resolve;
  });
}

async function recordUserResponse(durationSec = 4) {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mediaRecorder = new MediaRecorder(stream);
  const chunks = [];

  mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
  mediaRecorder.start();

  return new Promise((resolve) => {
    setTimeout(() => {
      mediaRecorder.stop();
      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("audio", blob, "user.wav");
        const res = await fetch("/transcribe", {
          method: "POST",
          body: formData,
        });
        const data = await res.json();
        resolve(data.text);
      };
    }, durationSec * 1000);
  });
}

async function getAgentResponse(step, userResponse = "") {
  const res = await fetch("/next-agent-step", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ step, user_response: userResponse }),
  });
  return await res.json(); // returns {text, audio}
}

async function startCall() {
  // Step 1: Agent asks for truck code
  const initial = await getAgentResponse(1);
  await playAudioAndWait(initial.audio);

  // Step 2: Listen to user
  const userText = await recordUserResponse();
  console.log("User:", userText);

  // Step 3: Agent replies to truck code
  const final = await getAgentResponse(2, userText);
  await playAudioAndWait(final.audio);
}
