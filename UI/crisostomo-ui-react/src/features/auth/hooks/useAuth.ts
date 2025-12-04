import { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { loginRequest } from "../api/login.api";


export const useAuth = () => {
    const { login: saveToken } = useContext(AuthContext);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const login = async (username: string, password: string) => {
        try {
            setLoading(true);
            setError(null);

            const token = await loginRequest(username, password);
            saveToken(token);

            return true;
        } catch (err: any) {
            setError(err.message);
            return false;
        } finally {
            setLoading(false);
        }
    };

    return { login, loading, error };
};
