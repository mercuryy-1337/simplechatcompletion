"use client";
import { useState } from "react";
import Image from "next/image";

export default function Home() {
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState<{ role: string; content: string }[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!message) return;
    setIsLoading(true);

    // Add user's message and a placeholder for the assistant's response
    setChatLog((prev) => [
      ...prev,
      { role: "user", content: message },
      { role: "assistant", content: "..." },
    ]);
    setMessage("");

    try {
      const response = await fetch("http://localhost:5151/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      if (data.reply) {
        setChatLog((prev) => {
          const newLog = [...prev];
          newLog[newLog.length - 1] = { role: "assistant", content: data.reply };
          return newLog;
        });
      } else {
        alert("Error: " + data.error);
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-black text-white">
      <header className="text-2xl font-bold mb-4">Chat with GPT-4</header>

      <main className="w-full max-w-2xl flex flex-col gap-4 bg-gray-800 p-6 rounded-lg shadow-md">
        <div className="flex-1 overflow-y-auto max-h-[400px] space-y-4">
          {chatLog.map((entry, index) => (
            <div
              key={index}
              className={`flex items-center p-3 rounded-lg ${
                entry.role === "user" 
                  ? "bg-blue-600 text-white self-end"
                  : "bg-gray-700 text-white self-start"
              }`}
            >
              {entry.role === "user" ? (
                <Image
                  src="/user-icon.svg"
                  alt="User icon"
                  width={24}
                  height={24}
                  className="mr-2"
                />
              ) : (
                <Image
                  src="/assistant-icon.svg"
                  alt="Assistant icon"
                  width={24}
                  height={24}
                  className="mr-2"
                />
              )}
              <div>{entry.content}</div>
            </div>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <input
            type="text"
            className="flex-1 px-4 py-2 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-700 text-white"
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading}
            className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition disabled:opacity-50"
          >
            {isLoading ? "Sending..." : "Send"}
          </button>
        </div>
      </main>

      <footer className="mt-8 text-sm text-gray-400">
        Powered by Next.js and Flask
      </footer>
    </div>
  );
}
