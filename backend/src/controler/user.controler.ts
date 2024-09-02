import { Request, Response } from "express"
import otpGenerator from'otp-generator'
import { sendMail } from "../utils/nodemailer/mail"
import { prisma } from "../../prisma/db"
import jwt from "jsonwebtoken"

let otpStore :{[email:string]:{otp:string,expiry:number}} = {}

export const sendOtp = async(req:Request, res:Response)=>{
    const email = req.body.email
    if(!email){
        return res.status(401).json({message:"email is a non empty field"})
    }
    const otp = otpGenerator.generate(6,{lowerCaseAlphabets:false,upperCaseAlphabets:false,specialChars:false})
    otpStore[email] ={
        otp:otp,
        expiry:Date.now() + 5 * 60 * 1000 
    } 
    const info = await sendMail(email, "Confirm Email Address",`<h2>hi there your otp to login in Newtron is</h2> <h1>${otp}</h1>`)
    if(!info){
        return res.status(500).json({message:"something went wrong while sending email"})
    }
    return res.status(200).json({message:`otp sent to the email ${email}`})
}

export const verifyOtp = async(req:Request, res:Response)=>{
    const {email, otp}:{email:string,otp:string} = req.body
    if(!otp||!email){
        return res.status(403).json({message:"email and otp are non empty field"})
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
        prisma.$transaction(async(tx)=>{
            const user = await prisma.user.findUnique({where:{email:email}})
            if(!user){
                await prisma.user.create({
                    data:{
                        email:email
                    }
                })
            }
        })
        
    } catch (error) {
        res.status(500).json({message:"some thing went wrong while saving user to db"})
    }
    const token = jwt.sign({email:email},process.env.JWTKEY||"")
    return res.status(200).json({
        token:token,
        message: 'OTP verified successfully' });
}