import express from "express"
import { router } from "./routes/chatbot.route"

const app = express()

app.use(express.json())

app.use("/chatbot",router)


export {app}