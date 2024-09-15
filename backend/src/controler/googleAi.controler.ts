import { Request,Response } from "express"
import { model } from "../utils/googleAi/model";
import { prisma } from "../../dataBase/db";

export const googleAiControler = async(req:Request, res:Response)=>{
    const question = req.body.question
    if(!question||!req.id){
        return res.status(401).json({message:"please login first and provide a question"})
    }
    
    try {
        const json = await model.generateContent(question) 
        await prisma.history.create({
            data:{
                question:question,
                answer:json.response.text(),
                userId:req.id
            }
        })
        return res.status(200).json(json.response.text())
    } catch (error) {
        return res.status(500).json({message:"something went wrong while generating"})
    }
}