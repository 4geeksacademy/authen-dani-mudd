import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Private () {
    const navigate = useNavigate()

    useEffect(() => {
        const token = sessionStorage.getItem("token")

        if (!token) {
            navigate('/login')
        }
    }, [])

    return (
        <h1>Super Secret Content, If not authorized. GO AWAY!</h1>
    )
}