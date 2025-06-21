import asyncio
import edge_tts
import io


async def synthesize_text_to_memory(text):
    communicate = edge_tts.Communicate(
        text, "en-IN-NeerjaNeural", rate="+30%", pitch="-10Hz"
    )
    stream = io.BytesIO()

    print(f"Synthesizing audio from '{text}'...")
    async for chunk in communicate.stream():
        if chunk.get("type") == "audio" and "data" in chunk:
            stream.write(chunk["data"])

    stream.seek(0)
    print("done")
    return stream


def synthesize_speech(text) -> bytes:
    return asyncio.run(synthesize_text_to_memory(text)).read()
