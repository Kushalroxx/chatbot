import { NextFunction, Request, Response } from "express"
import jwt, { JwtPayload } from "jsonwebtoken"

export const authMiddlewere = (req:Request,res:Response,next:NextFunction)=>{
    const {token}:{token:string} = req.body
    if (!token) {
        return res.status(401).json({message:"please provide a token"})
    }
    const data = jwt.verify(token,process.env.JWTKEY||"")
    if(!data){
        return res.status(401).json({message:"invalid token provided please login again first"})
    }else{
        // @ts-ignore
        req.email = data.email
        // @ts-ignore
        req.id = data.id
        next()
    }
}