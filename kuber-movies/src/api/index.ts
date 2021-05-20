import axios from "axios"

const api = axios.create({
    baseURL:"http://172.23.0.3:5000"
})

export default api;
