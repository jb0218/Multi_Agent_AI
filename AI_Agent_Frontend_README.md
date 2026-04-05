# 🚀 AI Agent Frontend

A modern, high-performance frontend for an AI-powered agent system built using Next.js, TypeScript, Tailwind CSS, and Zustand.

---

## 📌 Features

- Real-time chat interface  
- Fast rendering with Next.js  
- Modern UI with Tailwind CSS  
- State management using Zustand  
- Backend integration (FastAPI)  
- Message history  
- Typing indicator  
- Responsive design  

---

## 🏗️ Tech Stack

- Next.js  
- TypeScript  
- Tailwind CSS  
- Zustand  
- Axios / Fetch API  

---

## 📂 Project Structure

src/
├── app/
│   ├── layout.tsx  
│   └── page.tsx  
├── components/
│   └── chat/
│       ├── ChatLayout.tsx  
│       ├── ChatInput.tsx  
│       ├── MessageBubble.tsx  
│       └── TypingIndicator.tsx  
├── store/
│   └── useChatStore.ts  
├── lib/
│   └── api.ts  
├── types/
│   └── chat.ts  

---

## ⚙️ Setup

1. Install:
npm install

2. Create .env.local:
NEXT_PUBLIC_API_URL=http://localhost:8000

3. Run:
npm run dev

4. Open:
http://localhost:3000

---

## 🔌 API

POST /api/chat

Request:
{
  "message": "Hello",
  "thread_id": "123"
}

Response:
{
  "response": "AI reply",
  "thread_id": "123"
}

---

## ⚠️ Issues

- Check backend is running  
- Fix CORS  
- Restart dev server if errors  

---

## 👨‍💻 Author

Jatin Bhagtani

---

## ⭐ Support

Star the repo if useful!
