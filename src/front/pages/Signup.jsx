import { useState } from 'react';
import { useNavigate } from 'react-router-dom'


export default function SignUp () {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const handleSubmit = async (evt) => {
        evt.preventDefault()
        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/signup`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email,
                    password 
                })
            })

            if (!response.ok) {
                throw new Error('Error signing up')
            }

            const data = await response.json()

            sessionStorage.setItem("token", data.access_token)

            navigate('/private')


        } catch (err) {
            console.log(err)
        }
    }


    return (
        <>  
            <h1>SignUp</h1>
            <form onSubmit={handleSubmit}>
                Email: <input type="email" onChange={
                    (evt) => {
                        setEmail(evt.target.value)
                    }
                }  />
                Password: <input type="password" onChange={
                    (evt) => {
                        setPassword(evt.target.value)
                    }
                } />
                <input type="submit" value="Signup" />
            </form>
        </>
        
    )
}