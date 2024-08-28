import { GoogleGenerativeAI } from "@google/generative-ai";
import "dotenv/config"

const genAi = new GoogleGenerativeAI(process.env.GOOGLE_AI_KEY||"")
export const model = genAi.getGenerativeModel({model: "gemini-1.5-flash"})
