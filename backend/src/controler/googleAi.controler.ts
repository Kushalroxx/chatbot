import { Request,Response } from "express"
import { model } from "../googleAi/model";

export const googleAiControler = async(req:Request, res:Response)=>{
    const {question} = req.body
    console.log(question);
    const json = await model.generateContent(question)
    res.json(json)
}