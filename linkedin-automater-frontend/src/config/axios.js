import axios from 'axios';

if (!process.env.REACT_APP_API_URL) {
    throw new Error('REACT_APP_API_URL environment variable is not set');
}

const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    withCredentials: true
});

export default axiosInstance; 