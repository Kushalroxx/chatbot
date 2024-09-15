import express from "express";
import { historyControler } from "../controler/history.controler";

const historyRouter = express()

historyRouter.route("/").post(historyControler)

export {historyRouter}