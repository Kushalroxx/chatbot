import express from "express"
import { googleAiControler } from "../controler/googleAi.controler"

const router = express()

router.route("/").post(googleAiControler)
export {router}