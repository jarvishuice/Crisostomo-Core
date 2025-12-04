import { useState } from "react";
import { registerRequest } from "../api/register.api";

export const useRegister = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const register = async (formData: any) => {
        try {
            setLoading(true);
            setError(null);

            const response = await registerRequest(formData);
            return response;
        } catch (err: any) {
            setError(err.message);
            return null;
        } finally {
            setLoading(false);
        }
    };

    return { register, loading, error };
};
