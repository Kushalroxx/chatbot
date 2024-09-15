import { Request, Response } from "express"
import otpGenerator from'otp-generator'
import { sendMail } from "../utils/nodemailer/mail"
import { prisma } from "../../dataBase/db"
import jwt from "jsonwebtoken"
import {z} from "zod"

let otpStore :{[email:string]:{otp:string,expiry:number}} = {}
const emailSchema = z.string().email()
const otpSchema = z.string().min(6).max(6)
export const sendOtp = async(req:Request, res:Response)=>{
    const email = req.body.email
    if(!email||emailSchema.safeParse(email).success===false){
        return res.status(401).json({message:"email is a non empty field or enter a valid email"})
    }
    const otp = otpGenerator.generate(6,{lowerCaseAlphabets:false,upperCaseAlphabets:false,specialChars:false})
    otpStore[email] ={
        otp:otp,
        expiry:Date.now() + 5 * 60 * 1000 
    } 
    try {
        await sendMail(email, "Confirm Email Address", "this is your otp to login in Newtron",`<h2>Hey there your otp to login in Newtron is</h2> <h1>${otp}</h1>`)
        return res.status(200).json({message:`otp sent to the email ${email}`})
    } catch (error) {
        delete otpStore[email]
        return res.status(500).json({message:"something went wrong while sending email"})
     
    }
}

export const verifyOtp = async(req:Request, res:Response)=>{
    const {email, otp}:{email:string,otp:string} = req.body
       
    if(!otp||!email||emailSchema.safeParse(email).success===false||otpSchema.safeParse(otp).success===false){
        return res.status(401).json({message:"email and otp are non empty field"})
    }
    const storedOtp = otpStore[email]

    if (!storedOtp) {
        return res.status(400).json({ message: 'OTP not found or expired' });
    }

    if (storedOtp.otp !== otp) {
        return res.status(400).json({ message: 'Invalid OTP' });
    }
    if(Date.now()>storedOtp.expiry){
        delete otpStore[email]; 
        return res.status(400).json({ message: 'OTP expired' });
    }
    delete otpStore[email]; 
    try {
        await prisma.$transaction(async(tx)=>{
            let user = await tx.user.findUnique({where:{email:email}})
            if(!user){
                user = await tx.user.create({
                    data:{
                        email:email
                    }
                })
            }
            const token = jwt.sign({
                email:user?.email,
                id:user?.id
            },process.env.JWTKEY||"your jwt key")
            return res.status(200).json({
                token:token,
                message: 'OTP verified successfully' });
        })
        
    } catch (error) {
        res.status(500).json({message:"some thing went wrong while saving user to db"})
    }
}