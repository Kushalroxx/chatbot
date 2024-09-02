import express from "express";
import { sendOtp, verifyOtp } from "../controler/user.controler";

const loginRouter = express()

loginRouter.route("/").post(sendOtp)
loginRouter.route("/verify").post(verifyOtp)

export { loginRouter }
