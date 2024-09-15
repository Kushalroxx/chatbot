import { Request, Response } from "express";
import { prisma } from "../../dataBase/db";
declare global {
    namespace Express {
      interface Request {
        email?: string; 
        id?: string;
      }
    }
  }

export const historyControler = async(req:Request,res:Response)=>{
    if(!req.id||!req.email){
        return res.status(401).json({message:"please login first"})
    }
   try {
    const data = await prisma.history.findMany({
     where:{
         userId:req.id
     }
    })
    if(!data){
        return res.status(200).json({message:"no history found"})
    }
    const newData = data.map(e=>{
      return e.question
    })
    return res.status(200).json({data:newData,message:"success!! fetched history data"})

   } catch (error) {
    return res.status(500).json({message:"something went wrong while fetching history"})
   }
}