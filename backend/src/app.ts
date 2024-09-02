import express from "express"
import { chatRouter } from "./routes/chatbot.route"
import { loginRouter } from "./routes/user.route"
import bodyParser from "body-parser"
import { authMiddlewere } from "./middlewere/auth.middlewere"
import { historyRouter } from "./routes/history.route"

const app = express()

app.use(bodyParser.urlencoded({extended:true}))
app.use(bodyParser.json())
 
app.use("/history",authMiddlewere,historyRouter)
app.use("/chatbot",chatRouter)
app.use("/login",loginRouter)

export {app}