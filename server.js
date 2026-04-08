require("dotenv").config();

const express = require("express");
const cors = require("cors");
const { GoogleGenerativeAI } = require("@google/generative-ai");

const app = express();

app.use(cors()); // ✅ IMPORTANT
app.use(express.json());

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: "models/gemini-2.5-flash" });

// ---------------- GLOBAL CHAT ----------------
const globalChat = model.startChat({
  history: [
    {
      role: "user",
      parts: [{ text: "You are a helpful assistant chatbot." }],
    },
  ],
});

app.post("/chat", async (req, res) => {
  console.log("🔥 /chat hit");

  try {
    const result = await globalChat.sendMessage(req.body.message);
    res.json({ reply: result.response.text() });
  } catch (err) {
    console.error("❌ CHAT ERROR:", err);
    res.json({ reply: "Error: " + err.message });
  }
});

// ---------------- CASE CHAT ----------------
app.post("/case-chat", async (req, res) => {
  console.log("🔥 /case-chat hit");

  try {
    const { question, context } = req.body;

    console.log("QUESTION:", question);

    const prompt = `
You are a legal assistant.

Context:
${context}

Question:
${question}

Answer clearly in simple terms:
`;

    const result = await model.generateContent(prompt);

    console.log("✅ Gemini responded");

    res.json({ answer: result.response.text() });

  } catch (err) {
    console.error("❌ ERROR:", err);
    res.json({ answer: "Error generating answer" });
  }
});

app.listen(3000, () => {
  console.log("🚀 Node running on http://127.0.0.1:3000");
});