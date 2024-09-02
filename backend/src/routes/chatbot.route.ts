import express from "express"
import { googleAiControler } from "../controler/googleAi.controler"

const chatRouter = express()

chatRouter.route("/").post(googleAiControler)
export {chatRouter}