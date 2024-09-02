import nodemailer from "nodemailer"
import "dotenv/config"

const transporter = nodemailer.createTransport({
    service:"Gmail",
    auth:{
        user:process.env.EMAIL,
        pass:process.env.PASSWORD
    }
})
export const sendMail = async(email:string,
    subject:string,
    body?:string,
    html?:string
)=>{
    try {
        const info = await transporter.sendMail({
            from:`Electron <${process.env.EMAIL}`,
            to:email,
            subject:subject,
            text:body,
            html:html,
        })
        return info
    } catch (error) {
        console.log(error)
    }
}