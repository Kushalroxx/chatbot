import { Request,Response } from "express"
import { model } from "../utils/googleAi/model";

export const googleAiControler = async(req:Request, res:Response)=>{
    const question = req.body.question
    if(!question){
        return res.status(401).json({message:"question is a non empty field"})
    }
    
    try {
        const json = await model.generateContent(question)  
        return res.status(200).json(json.response.text())
    } catch (error) {
        return res.status(500).json({message:"something went wrong while generating"})
    }
}