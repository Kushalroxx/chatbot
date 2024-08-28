import { app } from "./app";
import "dotenv/config"

app.listen(process.env.PORT,()=>{
    console.log("app is listning on port 3000");
})
